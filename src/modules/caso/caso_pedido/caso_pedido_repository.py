from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.errors.errors import ConflictError
from src.modules.caso.caso_pedido.caso_pedido_model import CasoPedidoModel


class CasoPedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_caso(self, cod_caso: int) -> list[CasoPedidoModel]:
        return self.db.execute(
            select(CasoPedidoModel).where(CasoPedidoModel.cod_caso == cod_caso)
        ).scalars().all()

    def listar_por_pedido(self, cod_pedido: int) -> list[CasoPedidoModel]:
        return self.db.execute(
            select(CasoPedidoModel).where(CasoPedidoModel.cod_pedido == cod_pedido)
        ).scalars().all()

    def listar_cod_casos_ativos_por_pedido(self, cod_pedido: int) -> list[int]:
        return list(self.db.execute(
            select(CasoPedidoModel.cod_caso)
            .where(
                CasoPedidoModel.cod_pedido == cod_pedido,
                CasoPedidoModel.flg_reg_excluido == False,
            )
            .order_by(CasoPedidoModel.cod_caso)
        ).scalars().all())

    def sincronizar_por_caso(
        self,
        *,
        cod_caso: int,
        cod_pedidos: list[int],
        cif_usuario: int,
    ) -> None:
        cod_pedidos_set = set(self._normalizar_ids(
            cod_pedidos,
            "O mesmo pedido não pode ser vinculado mais de uma vez ao caso",
        ))
        existentes_map = {v.cod_pedido: v for v in self.listar_por_caso(cod_caso)}

        for cod_pedido in cod_pedidos_set:
            vinculo = existentes_map.get(cod_pedido)
            if vinculo:
                self._reativar_se_necessario(vinculo, cif_usuario)
                continue

            self.db.add(CasoPedidoModel(
                cod_caso=cod_caso,
                cod_pedido=cod_pedido,
                flg_reg_excluido=False,
                cif_usuario_inc=cif_usuario,
                cif_usuario_alt=cif_usuario,
            ))

        self._excluir_removidos(existentes_map, cod_pedidos_set, cif_usuario)

    def sincronizar_por_pedido(
        self,
        *,
        cod_pedido: int,
        cod_casos: list[int],
        cif_usuario: int,
    ) -> None:
        cod_casos_set = set(self._normalizar_ids(
            cod_casos,
            "O mesmo caso não pode ser vinculado mais de uma vez ao pedido",
        ))
        existentes_map = {v.cod_caso: v for v in self.listar_por_pedido(cod_pedido)}

        for cod_caso in cod_casos_set:
            vinculo = existentes_map.get(cod_caso)
            if vinculo:
                self._reativar_se_necessario(vinculo, cif_usuario)
                continue

            self.db.add(CasoPedidoModel(
                cod_caso=cod_caso,
                cod_pedido=cod_pedido,
                flg_reg_excluido=False,
                cif_usuario_inc=cif_usuario,
                cif_usuario_alt=cif_usuario,
            ))

        self._excluir_removidos(existentes_map, cod_casos_set, cif_usuario)

    def _normalizar_ids(self, ids: list[int], mensagem_duplicidade: str) -> list[int]:
        normalizados = [int(item_id) for item_id in ids]
        if len(normalizados) != len(set(normalizados)):
            raise ConflictError(mensagem_duplicidade)
        return normalizados

    def _reativar_se_necessario(self, vinculo: CasoPedidoModel, cif_usuario: int) -> None:
        if not vinculo.flg_reg_excluido:
            return

        vinculo.flg_reg_excluido = False
        vinculo.cif_usuario_alt = cif_usuario
        vinculo.dat_hor_alteracao = datetime.utcnow()
        self.db.add(vinculo)

    def _excluir_removidos(
        self,
        existentes_map: dict[int, CasoPedidoModel],
        ids_mantidos: set[int],
        cif_usuario: int,
    ) -> None:
        for item_id, vinculo in existentes_map.items():
            if item_id in ids_mantidos or vinculo.flg_reg_excluido:
                continue

            vinculo.flg_reg_excluido = True
            vinculo.cif_usuario_alt = cif_usuario
            vinculo.dat_hor_alteracao = datetime.utcnow()
            self.db.add(vinculo)
