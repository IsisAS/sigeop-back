from datetime import datetime
from typing import Any
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from src.common.repository import AbstractRepository
from src.modules.missao.missao_model import MissaoModel
from src.modules.missao.missao_schema import MissaoCreateDTO, MissaoUpdateDTO
from src.modules.missao.missao_encarregado.missao_encarregado_model import MissaoEncarregadoModel
from src.modules.missao.missao_fonte_humana.missao_fonte_humana_model import MissaoFonteHumanaModel
from src.modules.missao.missao_tipo.missao_tipo_model import MissaoTipoModel
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel
from src.modules.missao.missao_status.missao_status_model import MissaoStatusModel
from src.modules.plano.plano_model import PlanoModel
from src.modules.plano.plano_missao.plano_missao_model import PlanoMissaoModel
from src.modules.fonte_humana.fonte_humana_model import FonteHumanaModel
from src.modules.caso.caso.caso_model import CasoModel
from src.modules.operacao.operacao_model import OperacaoModel
from src.core.errors.errors import NotFoundError, ConflictError

def _derivar_tip_papel(enc_dto) -> str: 
    if enc_dto.tip_papel:
        return enc_dto.tip_papel
    return "ENCARREGADO_TITULAR" if enc_dto.flg_titular else "ENCARREGADO_SUPLENTE"

class MissaoRepository(AbstractRepository[MissaoModel, MissaoCreateDTO, MissaoUpdateDTO]):
    model = MissaoModel

    def list(self, *, limit: int = 50, offset: int = 0):
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.tipo),
                joinedload(self.model.recurso_tipo),
                joinedload(self.model.status),
                joinedload(self.model.encarregados),
                joinedload(self.model.fontes_humanas).joinedload(MissaoFonteHumanaModel.fonte_humana),
            )
            .outerjoin(MissaoTipoModel, self.model.cod_missao_tipo == MissaoTipoModel.cod_missao_tipo)
            .outerjoin(RecursoTipoModel, self.model.cod_recurso_tipo == RecursoTipoModel.cod_recurso_tipo)
            .outerjoin(MissaoStatusModel, self.model.cod_missao_status == MissaoStatusModel.cod_missao_status)
            .filter(self.model.flg_reg_excluido.is_(False))
        )
        
        stmt = stmt.order_by(self.model.cod_missao.desc()).limit(limit).offset(offset)
        return self.db.execute(stmt).unique().scalars().all()

    def list_por_tipo(
        self,
        *,
        cod_missao_tipo: int,
        cod_recurso_tipo: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ):
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.tipo),
                joinedload(self.model.recurso_tipo),
                joinedload(self.model.status),
                joinedload(self.model.encarregados),
                joinedload(self.model.fontes_humanas).joinedload(MissaoFonteHumanaModel.fonte_humana),
                joinedload(self.model.caso),
                joinedload(self.model.operacao),
            )
            .outerjoin(CasoModel, self.model.cod_caso == CasoModel.cod_caso)
            .outerjoin(OperacaoModel, self.model.cod_operacao == OperacaoModel.cod_operacao)
            .filter(
                self.model.cod_missao_tipo == cod_missao_tipo,
                self.model.flg_reg_excluido.is_(False),
            )
        )
        if cod_recurso_tipo is not None:
            stmt = stmt.filter(self.model.cod_recurso_tipo == cod_recurso_tipo)
        stmt = stmt.order_by(self.model.cod_missao.desc()).limit(limit).offset(offset)
        return self.db.execute(stmt).unique().scalars().all()
    
    def list_por_caso(self, *, cod_caso: int):
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.tipo),
                joinedload(self.model.recurso_tipo),
                joinedload(self.model.status),
                joinedload(self.model.encarregados),
                joinedload(self.model.fontes_humanas).joinedload(MissaoFonteHumanaModel.fonte_humana),
            )
            .filter(
                self.model.cod_caso == cod_caso,
                self.model.flg_reg_excluido.is_(False),
            )
            .order_by(self.model.cod_missao.desc())
        )
        return self.db.execute(stmt).unique().scalars().all()

    def get(self, entity_id: Any) -> dict[str, Any]:
        result = self.get_by_id(entity_id)
        if not result:
            raise NotFoundError(f"Missão({entity_id}) não encontrada.")
        return result

    def get_by_id(self, cod_missao: int) -> dict[str, Any] | None:
        result = (
            self.db.query(
                self.model,
                MissaoTipoModel.dsc_missao_tipo,
                RecursoTipoModel.sig_recurso_tipo,
                RecursoTipoModel.dsc_recurso_tipo,
                MissaoStatusModel.dsc_missao_status
            )
            .join(
                MissaoTipoModel,
                MissaoTipoModel.cod_missao_tipo == self.model.cod_missao_tipo
            )
            .outerjoin(
                RecursoTipoModel,
                RecursoTipoModel.cod_recurso_tipo == self.model.cod_recurso_tipo
            )
            .outerjoin(
                MissaoStatusModel,
                MissaoStatusModel.cod_missao_status == self.model.cod_missao_status
            )
            .filter(
                self.model.cod_missao == cod_missao,
                self.model.flg_reg_excluido.is_(False),
            )
            .first()
        )

        if not result:
            return None

        obj, dsc_tipo, sig_recurso_tipo, dsc_recurso_tipo, dsc_status = result
        
        missao_dict = {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
        missao_dict["dsc_missao_tipo"] = dsc_tipo
        missao_dict["sig_recurso_tipo"] = sig_recurso_tipo
        missao_dict["dsc_recurso_tipo"] = dsc_recurso_tipo
        missao_dict["dsc_missao_status"] = dsc_status

        encarregados = (
            self.db.query(MissaoEncarregadoModel)
            .filter(
                MissaoEncarregadoModel.cod_missao == cod_missao,
                MissaoEncarregadoModel.flg_reg_excluido.is_(False),
            )
            .all()
        )
        nom_encarregado_titular = None

        missao_dict["encarregados"] = encarregados
        missao_dict["nom_encarregado_titular"] = nom_encarregado_titular

        fontes_humanas = (
            self.db.query(
                MissaoFonteHumanaModel,
                FonteHumanaModel.sig_fonte_humana,
            )
            .outerjoin(
                FonteHumanaModel,
                FonteHumanaModel.cod_fonte_humana == MissaoFonteHumanaModel.cod_fonte_humana,
            )
            .filter(MissaoFonteHumanaModel.cod_missao == cod_missao)
            .all()
        )
        missao_dict["fontes_humanas"] = [
            {
                "cod_missao": fonte.cod_missao,
                "cod_fonte_humana": fonte.cod_fonte_humana,
                "sig_fonte_humana": sig_fonte_humana,
                "descricao": sig_fonte_humana,
                "flg_ativo": True,
                "flg_reg_excluido": fonte.flg_reg_excluido,
                "cif_usuario_inc": fonte.cif_usuario_inc,
                "cif_usuario_alt": fonte.cif_usuario_alt,
            }
            for fonte, sig_fonte_humana in fontes_humanas
        ]

        return missao_dict

    def create(self, obj_in: MissaoCreateDTO) -> dict[str, Any]:
        """Cria nova missão"""
        encarregados_dtos = obj_in.encarregados or []
        fontes_humanas_dtos = obj_in.fontes_humanas or []

        ativos = [e for e in encarregados_dtos if not e.flg_reg_excluido]
        if not ativos:
            raise ConflictError("Não é permitido salvar a missão sem ao menos um encarregado selecionado.")

        for enc in ativos:
            if enc.dat_fim and enc.dat_fim < enc.dat_inicio:
                raise ConflictError("A data fim do encarregado deve ser maior ou igual à data início.")

        titulares = [e for e in ativos if e.flg_titular]
        if len(titulares) != 1:
            raise ConflictError("Para registrar uma missão é necessário haver exatamente um encarregado titular.")

        missao_data = obj_in.model_dump(exclude={"encarregados", "fontes_humanas"})
        db_obj = self.model(**missao_data)
        self.db.add(db_obj)
        self.db.flush()

        for enc_dto in encarregados_dtos:
            enc = MissaoEncarregadoModel(
                cod_missao=db_obj.cod_missao,
                cod_agente=enc_dto.cod_agente,
                flg_titular=enc_dto.flg_titular,
                tip_papel=enc_dto.tip_papel or self._papel(enc_dto.flg_titular),
                dat_inicio=enc_dto.dat_inicio,
                dat_fim=enc_dto.dat_fim,
                flg_reg_excluido=enc_dto.flg_reg_excluido,
                cif_usuario_inc=enc_dto.cif_usuario_inc,
                cif_usuario_alt=enc_dto.cif_usuario_alt,
            )
            self.db.add(enc)

        for fh_dto in fontes_humanas_dtos:
            fh = MissaoFonteHumanaModel(
                cod_missao=db_obj.cod_missao,
                cod_fonte_humana=fh_dto.cod_fonte_humana,
                flg_reg_excluido=fh_dto.flg_reg_excluido,
                cif_usuario_inc=fh_dto.cif_usuario_inc,
                cif_usuario_alt=fh_dto.cif_usuario_alt,
            )
            self.db.add(fh)

        self.db.commit()
        return self.get_by_id(db_obj.cod_missao)

    def update(self, entity_id: Any, obj_in: MissaoUpdateDTO) -> dict[str, Any]:
        """Atualiza missão"""
        db_obj = (
            self.db.query(self.model)
            .filter(self.model.cod_missao == entity_id)
            .first()
        )

        if not db_obj:
            raise NotFoundError(f"Missão({entity_id}) não encontrada.")

        encarregados_dtos = obj_in.encarregados or []
        fontes_humanas_dtos = obj_in.fontes_humanas or []

        if not encarregados_dtos:
            raise ConflictError("A lista de encarregados não pode ser vazia.")

        ativos = [e for e in encarregados_dtos if not e.flg_reg_excluido]
        titulares = [e for e in ativos if e.flg_titular]

        if len(titulares) > 1:
            raise ConflictError("Apenas um titular permitido")
        if ativos and not titulares:
            raise ConflictError("Precisa de um titular ativo")

        for enc in encarregados_dtos:
            if enc.dat_fim and enc.dat_inicio and enc.dat_fim < enc.dat_inicio:
                raise ConflictError("Data fim não pode ser menor que data início")

        update_data = obj_in.model_dump(exclude={"encarregados", "fontes_humanas"}, exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db_obj.dat_hor_alteracao = datetime.utcnow()

        vinculos_existentes = (
            self.db.query(MissaoEncarregadoModel)
            .filter(MissaoEncarregadoModel.cod_missao == entity_id)
            .all()
        )

        enc_map = {e.cod_agente: e for e in encarregados_dtos}

        for v in vinculos_existentes:
            if v.cod_agente in enc_map:
                dto = enc_map[v.cod_agente]
                v.flg_titular = dto.flg_titular
                v.tip_papel = dto.tip_papel or self._papel(dto.flg_titular)
                v.flg_reg_excluido = dto.flg_reg_excluido
                v.dat_inicio = dto.dat_inicio
                v.dat_fim = dto.dat_fim
                v.cif_usuario_alt = dto.cif_usuario_alt
                v.dat_hor_alteracao = datetime.utcnow()
                del enc_map[v.cod_agente]
            else:
                v.flg_reg_excluido = True
                v.cif_usuario_alt = obj_in.cif_usuario_alt
                v.dat_hor_alteracao = datetime.utcnow()

        for dto in enc_map.values():
            novo = MissaoEncarregadoModel(
                cod_missao=entity_id,
                cod_agente=dto.cod_agente,
                flg_titular=dto.flg_titular,
                tip_papel=dto.tip_papel or self._papel(dto.flg_titular),
                dat_inicio=dto.dat_inicio,
                dat_fim=dto.dat_fim,
                flg_reg_excluido=dto.flg_reg_excluido,
                cif_usuario_inc=dto.cif_usuario_inc,
                cif_usuario_alt=dto.cif_usuario_alt,
            )
            self.db.add(novo)
            
        if fontes_humanas_dtos is not None: 
            fontes_existentes = (
                self.db.query(MissaoFonteHumanaModel)
                .filter(MissaoFonteHumanaModel.cod_missao == entity_id)
                .all()
            )
            
            fh_map = {e.cod_fonte_humana: e for e in fontes_humanas_dtos}
            
            for fh in fontes_existentes:
                if fh.cod_fonte_humana in fh_map:
                    dto = fh_map[fh.cod_fonte_humana]
                    fh.flg_reg_excluido = dto.flg_reg_excluido
                    fh.cif_usuario_alt = dto.cif_usuario_alt
                    fh.dat_hor_alteracao = datetime.utcnow()
                    del fh_map[fh.cod_fonte_humana]
                else:
                    fh.flg_reg_excluido = True
                    fh.cif_usuario_alt = obj_in.cif_usuario_alt
                    fh.dat_hor_alteracao = datetime.utcnow()

            for dto in fh_map.values():
                novo = MissaoFonteHumanaModel(
                    cod_missao=entity_id,
                    cod_fonte_humana=dto.cod_fonte_humana,
                    flg_reg_excluido=dto.flg_reg_excluido,
                    cif_usuario_inc=dto.cif_usuario_inc,
                    cif_usuario_alt=dto.cif_usuario_alt,
                )
                self.db.add(novo)

        self.db.commit()
        return self.get_by_id(entity_id)

    def soft_delete(self, entity_id: int, *, justificativa: str, cif_usuario_alt: int) -> None:
        justificativa = justificativa.strip()
        if not justificativa:
            raise ConflictError("A justificativa da exclusão é obrigatória.")

        db_obj = self.db.query(self.model).filter(
            self.model.cod_missao == entity_id,
            self.model.flg_reg_excluido.is_(False),
        ).first()
        if not db_obj:
            raise NotFoundError(f"Missão({entity_id}) não encontrada.")

        planos = (
            self.db.query(PlanoModel.num_plano)
            .join(PlanoMissaoModel, PlanoMissaoModel.cod_plano == PlanoModel.cod_plano)
            .filter(
                PlanoMissaoModel.cod_missao == entity_id,
                PlanoMissaoModel.flg_reg_excluido.is_(False),
                PlanoModel.flg_reg_excluido.is_(False),
            )
            .order_by(PlanoModel.num_plano)
            .all()
        )
        if planos:
            numeros = ", ".join(str(item[0]) for item in planos)
            raise ConflictError(
                f"Exclusão não permitida pois esta Missão está vinculada a: Plano Nº {numeros}"
            )

        db_obj.flg_reg_excluido = True
        db_obj.dsc_justificativa_exclusao = justificativa
        db_obj.cif_usuario_alt = cif_usuario_alt
        db_obj.dat_hor_alteracao = datetime.utcnow()
        self.db.commit()

    @staticmethod
    def _papel(flg_titular: bool) -> str:
        return "ENCARREGADO_TITULAR" if flg_titular else "ENCARREGADO_SUPLENTE"
