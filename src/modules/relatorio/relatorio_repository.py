from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload, selectinload

from src.common.repository import AbstractRepository
from src.modules.pedido.pedido_model import PedidoModel
from src.modules.pedido.status.status_model import StatusModel
from src.modules.relatorio.relatorio_model import (
    RelatorioDifusaoModel,
    RelatorioModel,
    RelatorioPedidoModel,
    RelatorioStatusModel,
    RelatorioTipoModel,
)
from src.modules.relatorio.relatorio_schema import RelatorioCreateDTO, RelatorioUpdateDTO


class RelatorioRepository(AbstractRepository[RelatorioModel, RelatorioCreateDTO, RelatorioUpdateDTO]):
    model = RelatorioModel

    def __init__(self, db: Session):
        super().__init__(db)

    def _base_query(self):
        return select(RelatorioModel).options(
            joinedload(RelatorioModel.tipo),
            joinedload(RelatorioModel.status),
            selectinload(RelatorioModel.difusoes),
            selectinload(RelatorioModel.pedidos)
            .joinedload(RelatorioPedidoModel.pedido)
            .joinedload(PedidoModel.pedido_status),
        )

    def get(self, entity_id: int) -> RelatorioModel:
        item = self.db.execute(
            self._base_query().where(RelatorioModel.cod_relatorio == entity_id)
        ).scalar_one_or_none()
        if item is None:
            return super().get(entity_id)
        return item

    def list(self, *, limit: int = 50, offset: int = 0) -> list[RelatorioModel]:
        stmt = (
            self._base_query()
            .join(RelatorioStatusModel, RelatorioStatusModel.cod_relatorio_status == RelatorioModel.cod_relatorio_status)
            .where(RelatorioModel.flg_reg_excluido.is_(False))
            .order_by(RelatorioStatusModel.num_ordem, RelatorioModel.dat_hor_inclusao.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.execute(stmt).scalars().all())

    def create(self, dto: RelatorioCreateDTO) -> RelatorioModel:
        data = dto.model_dump(exclude={"pedidos", "difusoes"})
        item = RelatorioModel(**data)
        self.db.add(item)
        try:
            self.db.flush()
            self._sync_relacoes(item, dto.pedidos, dto.difusoes)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return self.get(item.cod_relatorio)

    def update(self, entity_id: int, dto: RelatorioUpdateDTO) -> RelatorioModel:
        item = self.get(entity_id)
        data = dto.model_dump(exclude={"pedidos", "difusoes"})
        for field, value in data.items():
            setattr(item, field, value)

        try:
            self._sync_relacoes(item, dto.pedidos, dto.difusoes)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return self.get(entity_id)

    def _sync_relacoes(self, item, pedidos, difusoes) -> None:
        self.db.execute(
            delete(RelatorioPedidoModel).where(
                RelatorioPedidoModel.cod_relatorio == item.cod_relatorio
            )
        )
        self.db.execute(
            delete(RelatorioDifusaoModel).where(
                RelatorioDifusaoModel.cod_relatorio == item.cod_relatorio
            )
        )

        now = datetime.now(timezone.utc).astimezone()
        for cod_pedido in dict.fromkeys(pedidos):
            self.db.add(
                RelatorioPedidoModel(
                    cod_relatorio=item.cod_relatorio,
                    cod_pedido=cod_pedido,
                    flg_reg_excluido=False,
                    cif_usuario_inc=item.cif_usuario_inc,
                    cif_usuario_alt=item.cif_usuario_alt,
                    dat_hor_inclusao=now,
                    dat_hor_alteracao=now,
                )
            )

        for difusao in difusoes:
            self.db.add(
                RelatorioDifusaoModel(
                    cod_relatorio=item.cod_relatorio,
                    **difusao.model_dump(),
                    dsc_destinatario_externo=None,
                    flg_reg_excluido=False,
                    cif_usuario_inc=item.cif_usuario_inc,
                    cif_usuario_alt=item.cif_usuario_alt,
                    dat_hor_inclusao=now,
                    dat_hor_alteracao=now,
                )
            )
        self.db.flush()

    def list_tipos_permitidos(self) -> list[RelatorioTipoModel]:
        stmt = (
            select(RelatorioTipoModel)
            .where(
                RelatorioTipoModel.sig_relatorio_tipo.in_(("RDI", "RELINT")),
                RelatorioTipoModel.flg_ativo.is_(True),
                RelatorioTipoModel.flg_reg_excluido.is_(False),
            )
            .order_by(RelatorioTipoModel.sig_relatorio_tipo)
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_status(self) -> list[RelatorioStatusModel]:
        stmt = (
            select(RelatorioStatusModel)
            .where(
                RelatorioStatusModel.flg_ativo.is_(True),
                RelatorioStatusModel.flg_reg_excluido.is_(False),
            )
            .order_by(RelatorioStatusModel.num_ordem)
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_pedidos_elegiveis(self, ano: int) -> list[tuple[PedidoModel, str | None]]:
        stmt = (
            select(PedidoModel, StatusModel.dsc_pedido_status)
            .join(StatusModel, StatusModel.cod_pedido_status == PedidoModel.cod_pedido_status)
            .where(
                PedidoModel.flg_reg_excluido.is_(False),
                PedidoModel.num_ano == ano,
                StatusModel.sig_pedido_status == "ABERTO",
                StatusModel.flg_reg_excluido.is_(False),
            )
            .order_by(PedidoModel.num_pedido)
        )
        return list(self.db.execute(stmt).all())

    def codigos_pedidos_elegiveis(self, ano: int) -> set[int]:
        stmt = (
            select(PedidoModel.cod_pedido)
            .join(StatusModel, StatusModel.cod_pedido_status == PedidoModel.cod_pedido_status)
            .where(
                PedidoModel.flg_reg_excluido.is_(False),
                PedidoModel.num_ano == ano,
                StatusModel.sig_pedido_status == "ABERTO",
                StatusModel.flg_reg_excluido.is_(False),
            )
        )
        return set(self.db.scalars(stmt).all())

    def codigos_pedidos_associados(self, cod_relatorio: int) -> set[int]:
        stmt = select(RelatorioPedidoModel.cod_pedido).where(
            RelatorioPedidoModel.cod_relatorio == cod_relatorio,
            RelatorioPedidoModel.flg_reg_excluido.is_(False),
        )
        return set(self.db.scalars(stmt).all())

    def tipo_permitido(self, cod_relatorio_tipo: int) -> bool:
        stmt = select(RelatorioTipoModel.cod_relatorio_tipo).where(
            RelatorioTipoModel.cod_relatorio_tipo == cod_relatorio_tipo,
            RelatorioTipoModel.sig_relatorio_tipo.in_(("RDI", "RELINT")),
            RelatorioTipoModel.flg_ativo.is_(True),
            RelatorioTipoModel.flg_reg_excluido.is_(False),
        )
        return self.db.scalar(stmt) is not None

    def status_valido(self, cod_relatorio_status: int) -> bool:
        stmt = select(RelatorioStatusModel.cod_relatorio_status).where(
            RelatorioStatusModel.cod_relatorio_status == cod_relatorio_status,
            RelatorioStatusModel.flg_ativo.is_(True),
            RelatorioStatusModel.flg_reg_excluido.is_(False),
        )
        return self.db.scalar(stmt) is not None
