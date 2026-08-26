from typing import List

from sqlalchemy import Integer, String, and_, or_, select
from sqlalchemy.inspection import inspect

from src.common.repository import AbstractRepository
from src.modules.caso.caso.caso_model import CasoModel
from src.modules.caso.caso.caso_schema import CasoCreateDTO, CasoUpdateDTO
from src.modules.caso.caso_pedido.caso_pedido_model import CasoPedidoModel
from src.modules.caso.caso_pedido.caso_pedido_repository import CasoPedidoRepository
from src.modules.missao.missao_model import MissaoModel
from src.modules.pedido.pedido_model import PedidoModel
from src.modules.plano.plano_model import PlanoModel


class CasoRepository(AbstractRepository[CasoModel, CasoCreateDTO, CasoUpdateDTO]):
    model = CasoModel

    def create(self, dto: CasoCreateDTO) -> model:
        data = dto.model_dump()
        obj = self.model(**data)
        self.db.add(obj)
        self.db.flush()
        return obj

    def update(self, caso_id: int, dto: CasoUpdateDTO) -> model:
        obj = self.get(caso_id)

        data = dto.model_dump(exclude={"pedidos_vinculados"}, exclude_unset=True)
        for k, v in data.items():
            setattr(obj, k, v)

        self.db.add(obj)
        self.db.flush()
        return obj

    def sincronizar_pedidos_vinculados(self, cod_caso: int, pedidos_ids: list[int], cif_usuario: int):
        CasoPedidoRepository(self.db).sincronizar_por_caso(
            cod_caso=cod_caso,
            cod_pedidos=pedidos_ids,
            cif_usuario=cif_usuario,
        )

    def get_by_pedido_abertura(self, cod_pedido_abertura: int, *, limit: int = 50, offset: int = 0) -> List[CasoModel]:
        """Retorna todos os casos relacionados ao cod_pedido_abertura"""
        stmt = select(CasoModel).where(
            CasoModel.cod_pedido_abertura == cod_pedido_abertura
        ).order_by(CasoModel.cod_caso.desc()).limit(limit).offset(offset)
        return self.db.execute(stmt).scalars().all()

    def _try_parse_int(self, valor) -> int | None:
        try:
            valor_int = int(valor)
        except (ValueError, TypeError):
            return None

        min_int32 = 2**31
        max_int32 = 2**31 - 1
        if min_int32 <= valor_int <= max_int32:
            return valor_int

        return None

    def listar_com_filtro(self, filtro: str | int, limit: int = 50, offset: int = 0) -> List[CasoModel]:
        stmt = select(self.model)

        mapper = inspect(self.model)
        condicoes = []

        filtro_int = self._try_parse_int(filtro)

        for coluna in mapper.columns:
            if coluna.foreign_keys:
                continue

            if isinstance(coluna.type, String) and filtro is not None:
                condicoes.append(coluna.ilike(f"%{filtro}%"))

            elif isinstance(coluna.type, Integer) and filtro_int is not None:
                condicoes.append(coluna == filtro_int)

        if condicoes:
            stmt = stmt.where(or_(*condicoes))

        stmt = stmt.order_by(self.model.cod_caso.desc()).limit(limit).offset(offset)

        return self.db.execute(stmt).scalars().all()

    def listar_pedidos_disponiveis(self) -> list[PedidoModel]:
        """
        Retorna pedidos elegiveis para vinculo: nao excluidos, nao vinculados
        como pedido de abertura de nenhum caso, e nao vinculados ativamente
        via tb_caso_pedido (flg_reg_excluido = False).
        """
        subq_pedidos_vinculados = select(CasoPedidoModel.cod_pedido).where(
            CasoPedidoModel.flg_reg_excluido == False
        )

        subq_pedidos_abertura = select(self.model.cod_pedido_abertura)

        stmt = select(PedidoModel).where(
            and_(
                PedidoModel.flg_reg_excluido == False,
                PedidoModel.cod_pedido.notin_(subq_pedidos_vinculados),
                PedidoModel.cod_pedido.notin_(subq_pedidos_abertura),
            )
        )
        return self.db.execute(stmt).scalars().all()

    def listar_pedidos_vinculados_nn(self, cod_caso: int) -> list[PedidoModel]:
        """Busca os pedidos vinculados ativos via tb_caso_pedido"""
        stmt = select(PedidoModel).join(
            CasoPedidoModel, PedidoModel.cod_pedido == CasoPedidoModel.cod_pedido
        ).where(
            CasoPedidoModel.cod_caso == cod_caso,
            CasoPedidoModel.flg_reg_excluido == False,
            PedidoModel.flg_reg_excluido == False,
        )
        return self.db.execute(stmt).scalars().all()

    def listar_missoes_por_caso(self, cod_caso: int) -> list[MissaoModel]:
        stmt = select(MissaoModel).where(
            MissaoModel.cod_caso == cod_caso,
            MissaoModel.flg_reg_excluido == False
        )
        return self.db.execute(stmt).scalars().all()

    def listar_planos_por_caso(self, cod_caso: int) -> list[PlanoModel]:
        """Compatibilidade: a v1.9 nao possui mais vinculo N:N de planos em caso."""
        return []
