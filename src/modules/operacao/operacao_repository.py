from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from src.common.repository import AbstractRepository
from src.modules.operacao.operacao_model import OperacaoModel
from src.modules.operacao.operacao_schema import OperacaoCreateDTO, OperacaoUpdateDTO
from src.modules.operacao.operacao_encarregado.operacao_encarregado_model import OperacaoEncarregadoModel
from src.modules.operacao.operacao_encarregado.operacao_encarregado_repository import OperacaoEncarregadoRepository
from src.modules.operacao.operacao_tipo.operacao_tipo_model import OperacaoTipoModel
from src.modules.operacao.operacao_status.operacao_status_model import OperacaoStatusModel
from src.modules.missao.missao_model import MissaoModel
from src.modules.plano.plano_model import PlanoModel
from src.modules.plano.plano_operacao.plano_operacao_model import PlanoOperacaoModel
from src.modules.caso.caso.caso_model import CasoModel
from src.modules.operacao.operacao_pedido.operacao_pedido_model import OperacaoPedidoModel
from src.modules.pedido.pedido_model import PedidoModel
from src.core.errors.errors import NotFoundError

class OperacaoRepository(AbstractRepository[OperacaoModel, OperacaoCreateDTO, OperacaoUpdateDTO]):
    model = OperacaoModel

    def get(self, id: Any) -> dict[str, Any]:
        result = self.get_by_id(id)
        if not result:
            raise NotFoundError(f"Operação({id}) não encontrada.")
        return result

    def create(self, obj_in: OperacaoCreateDTO) -> dict[str, Any]:
        encarregados_dtos = obj_in.encarregados or []

        if not encarregados_dtos:
            raise ValueError("A lista de encarregados não pode ser vazia.")

        if sum(1 for enc in encarregados_dtos if enc.flg_titular and not enc.flg_reg_excluido) != 1:
            raise ValueError("A operação deve ter exatamente um encarregado titular ativo.")

        cod_pedido = obj_in.cod_pedido
        operacao_data = obj_in.model_dump(exclude={"encarregados", "cod_pedido"})
        db_obj = self.model(**operacao_data)

        self.db.add(db_obj)
        self.db.flush()

        encarregados_data = []
        for enc_dto in encarregados_dtos:
            data = enc_dto.model_dump()
            data["cod_operacao"] = db_obj.cod_operacao
            encarregados_data.append(data)

        enc_repo = OperacaoEncarregadoRepository(self.db)
        enc_repo.create(encarregados_data)
        self._sync_pedido(db_obj.cod_operacao, cod_pedido, obj_in.cif_usuario_inc, obj_in.cif_usuario_alt)

        self.db.commit()
    
        return self.get_by_id(db_obj.cod_operacao)
    
    def commit(self) -> None:
        self.db.commit()

    def get(self, id: Any) -> dict[str, Any]:
        result = self.get_by_id(id)
        if not result:
            raise NotFoundError(f"Operação({id}) não encontrada.")
        return result

    def get_by_id(self, cod_operacao: int) -> dict[str, Any] | None:
        result = (
            self.db.query(
                self.model,
                OperacaoTipoModel.dsc_operacao_tipo,
                OperacaoStatusModel.dsc_operacao_status
            )
            .join(OperacaoTipoModel, OperacaoTipoModel.cod_operacao_tipo == self.model.cod_operacao_tipo)
            .join(OperacaoStatusModel, OperacaoStatusModel.cod_operacao_status == self.model.cod_operacao_status)
            .filter(self.model.cod_operacao == cod_operacao)
            .first()
        )

        if not result:
            return None

        obj, dsc_tipo, dsc_status = result
        
        operacao_dict = {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
        operacao_dict["dsc_operacao_tipo"] = dsc_tipo
        operacao_dict["dsc_operacao_status"] = dsc_status

        encarregados = (
            self.db.query(OperacaoEncarregadoModel)
            .filter(
                OperacaoEncarregadoModel.cod_operacao == cod_operacao,
            )
            .all()
        )

        operacao_dict["encarregados"] = encarregados
        operacao_dict["cod_pedido"] = self._get_cod_pedido(cod_operacao)

        return operacao_dict

    def update(self, entity_id: Any, obj_in: OperacaoUpdateDTO) -> dict[str, Any]:
        db_obj = (
            self.db.query(self.model)
            .filter(self.model.cod_operacao == entity_id)
            .first()
        )

        if not db_obj:
            return None

        encarregados_dtos = obj_in.encarregados or []

        if not encarregados_dtos:
            raise ValueError("A lista de encarregados não pode ser vazia.")

        if sum(1 for enc in encarregados_dtos if enc.flg_titular and not enc.flg_reg_excluido) != 1:
            raise ValueError("A operação deve ter exatamente um encarregado titular ativo.")

        vinculos_existentes = (
            self.db.query(OperacaoEncarregadoModel)
            .filter(OperacaoEncarregadoModel.cod_operacao == entity_id)
            .all()
        )

        enc_map = {e.cod_agente: e for e in encarregados_dtos}
        enc_repo = OperacaoEncarregadoRepository(self.db)

        for v in vinculos_existentes:
            if v.cod_agente in enc_map:
                dto = enc_map[v.cod_agente]
                v.flg_titular = dto.flg_titular
                v.flg_reg_excluido = dto.flg_reg_excluido
                v.dat_inicio = dto.dat_inicio
                v.dat_fim = dto.dat_fim
                v.cif_usuario_alt = dto.cif_usuario_alt
                del enc_map[v.cod_agente]
            else:
                v.flg_reg_excluido = True

        novos_encarregados_data = []
        for dto in enc_map.values():
            data = dto.model_dump()
            data["cod_operacao"] = entity_id
            novos_encarregados_data.append(data)
        
        if novos_encarregados_data:
            enc_repo.create(novos_encarregados_data)

        update_data = obj_in.model_dump(exclude={"cod_operacao", "encarregados", "cod_pedido"}, exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db_obj.dat_hor_alteracao = datetime.utcnow()
        self._sync_pedido(entity_id, obj_in.cod_pedido, db_obj.cif_usuario_inc, obj_in.cif_usuario_alt)

        self.db.commit()
        return self.get_by_id(entity_id)

    def _get_cod_pedido(self, cod_operacao: int) -> int | None:
        vinculo = (
            self.db.query(OperacaoPedidoModel)
            .filter(
                OperacaoPedidoModel.cod_operacao == cod_operacao,
                OperacaoPedidoModel.flg_reg_excluido == False,
            )
            .first()
        )
        return vinculo.cod_pedido if vinculo else None

    def _sync_pedido(
        self,
        cod_operacao: int,
        cod_pedido: int | None,
        cif_usuario_inc: int,
        cif_usuario_alt: int,
    ) -> None:
        vinculos = (
            self.db.query(OperacaoPedidoModel)
            .filter(OperacaoPedidoModel.cod_operacao == cod_operacao)
            .all()
        )
        agora = datetime.utcnow()

        if cod_pedido is None:
            for vinculo in vinculos:
                vinculo.flg_reg_excluido = True
                vinculo.cif_usuario_alt = cif_usuario_alt
                vinculo.dat_hor_alteracao = agora
            return

        for vinculo in vinculos:
            if vinculo.cod_pedido == cod_pedido:
                vinculo.flg_reg_excluido = False
                vinculo.cif_usuario_alt = cif_usuario_alt
                vinculo.dat_hor_alteracao = agora
            else:
                vinculo.flg_reg_excluido = True
                vinculo.cif_usuario_alt = cif_usuario_alt
                vinculo.dat_hor_alteracao = agora

        if any(vinculo.cod_pedido == cod_pedido for vinculo in vinculos):
            return

        self.db.add(
            OperacaoPedidoModel(
                cod_operacao=cod_operacao,
                cod_pedido=cod_pedido,
                flg_reg_excluido=False,
                cif_usuario_inc=cif_usuario_inc,
                cif_usuario_alt=cif_usuario_alt,
                dat_hor_inclusao=agora,
                dat_hor_alteracao=agora,
            )
        )

    def get_operacao_by_caso_id(self, cod_caso: int):
        stmt = select(self.model).where(
            self.model.cod_caso == cod_caso
        )

        return self.db.execute(stmt).scalars().all()

    def listar_inteligencia_protecao(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        stmt = (
            select(
                self.model,
                OperacaoStatusModel.dsc_operacao_status,
                CasoModel.nom_caso,
            )
            .outerjoin(
                OperacaoStatusModel,
                OperacaoStatusModel.cod_operacao_status == self.model.cod_operacao_status,
            )
            .outerjoin(
                CasoModel,
                CasoModel.cod_caso == self.model.cod_caso,
            )
            .where(
                and_(
                    self.model.cod_operacao_tipo == 6,
                    self.model.flg_reg_excluido == False,
                )
            )
            .order_by(self.model.cod_operacao)
            .limit(limit)
            .offset(offset)
        )

        rows = self.db.execute(stmt).all()
        result = []
        for operacao, dsc_status, nom_caso in rows:
            titular = (
                self.db.query(OperacaoEncarregadoModel)
                .filter(
                    OperacaoEncarregadoModel.cod_operacao == operacao.cod_operacao,
                    OperacaoEncarregadoModel.flg_titular == True,
                    OperacaoEncarregadoModel.flg_reg_excluido == False,
                )
                .first()
            )

            result.append({
                "cod_operacao": operacao.cod_operacao,
                "nom_operacao": operacao.nom_operacao,
                "cod_caso": operacao.cod_caso,
                "nom_caso": nom_caso,
                "encarregado_cif": titular.cod_agente if titular else None,
                "dsc_operacao_status": dsc_status,
            })

        return result

    def listar_missoes_por_operacao(self, cod_operacao: int) -> list[MissaoModel]:
        stmt = select(MissaoModel).where(
            MissaoModel.cod_operacao == cod_operacao,
            MissaoModel.flg_reg_excluido == False
        )
        return self.db.execute(stmt).scalars().all()

    def listar_planos_por_caso(self, cod_caso: int) -> list[PlanoModel]:
        """Compatibilidade: a v1.9 não possui mais vínculo N:N de planos em caso."""
        return []

    def listar_planos_por_operacao(self, cod_operacao: int) -> list[PlanoModel]:
        stmt = (
            select(PlanoModel)
            .join(
                PlanoOperacaoModel,
                PlanoOperacaoModel.cod_plano == PlanoModel.cod_plano,
            )
            .where(
                PlanoOperacaoModel.cod_operacao == cod_operacao,
                PlanoModel.flg_reg_excluido == False,
            )
        )

        return self.db.execute(stmt).scalars().all()

    def listar_pedidos_por_operacao(self, cod_operacao: int) -> list[PedidoModel]:
        stmt = (
            select(PedidoModel)
            .join(
                OperacaoPedidoModel,
                OperacaoPedidoModel.cod_pedido == PedidoModel.cod_pedido,
            )
            .where(
                OperacaoPedidoModel.cod_operacao == cod_operacao,
                OperacaoPedidoModel.flg_reg_excluido == False,
                PedidoModel.flg_reg_excluido == False,
            )
        )

        return self.db.execute(stmt).scalars().all()

    def delete(self, cod_operacao: int, dsc_justificativa_exclusao: str) -> None:
        db_obj = (
            self.db.query(self.model)
            .filter(self.model.cod_operacao == cod_operacao)
            .first()
        )
        if not db_obj:
            raise NotFoundError(f"Operação({cod_operacao}) não encontrada.")

        justificativa = (dsc_justificativa_exclusao or "").strip()
        if not justificativa:
            raise ValueError("A justificativa de exclusão é obrigatória.")

        db_obj.flg_reg_excluido = True
        db_obj.dsc_justificativa_exclusao = justificativa
        db_obj.dat_hor_alteracao = datetime.utcnow()

        for enc in db_obj.encarregados:
            enc.flg_reg_excluido = True
            enc.dat_hor_alteracao = datetime.utcnow()

        for pedido in db_obj.pedidos:
            pedido.flg_reg_excluido = True
            pedido.dat_hor_alteracao = datetime.utcnow()

        vinculos_plano = (
            self.db.query(PlanoOperacaoModel)
            .filter(PlanoOperacaoModel.cod_operacao == cod_operacao)
            .all()
        )
        for vp in vinculos_plano:
            vp.flg_reg_excluido = True
            vp.dat_hor_alteracao = datetime.utcnow()

        self.db.flush()
 
