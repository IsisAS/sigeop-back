from __future__ import annotations

from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import select 

from src.common.repository import AbstractRepository
from src.core.errors.errors import NotFoundError
from src.modules.demanda.demanda_model import DemandaModel
from src.modules.demanda.demanda_schema import DemandaCreateDTO, DemandaUpdateDTO
from src.modules.demanda.demanda_local.demanda_local_model import DemandaLocalModel
from src.modules.demanda.evento_tipo.evento_tipo_model import EventoTipoModel
from src.modules.operacao.operacao_model import OperacaoModel
from src.modules.pais.pais_model import PaisModel 
from src.modules.uf.uf_model import UfModel 
from src.modules.municipio.municipio_model import MunicipioModel 

class DemandaRepository(AbstractRepository[DemandaModel, DemandaCreateDTO, DemandaUpdateDTO]):
    model = DemandaModel
    
    def _fetch_full(self, cod_demanda: int) -> dict | None: 
        row = (
            self.db.query(DemandaModel, OperacaoModel.nom_operacao, EventoTipoModel.dsc_evento_tipo)
            .outerjoin(OperacaoModel, OperacaoModel.cod_operacao == DemandaModel.cod_operacao)
            .join(EventoTipoModel, EventoTipoModel.cod_evento_tipo == DemandaModel.cod_tipo_evento_demanda)
            .filter(DemandaModel.cod_demanda == cod_demanda)
            .first()
        )
        if not row:
            return None
        
        demanda, nom_op, dsc_ev = row
        locais = self._fetch_locais(cod_demanda)
        return self._to_dict(demanda, nom_op, dsc_ev, locais)
    
    def _fetch_locais(self, cod_demanda: int) -> list[dict]:
        rows = (
            self.db.query(DemandaLocalModel, PaisModel.nom_pais, UfModel.nom_uf, MunicipioModel.nom_municipio)
            .join(PaisModel, PaisModel.cod_pais == DemandaLocalModel.cod_pais)
            .outerjoin(UfModel, UfModel.cod_uf == DemandaLocalModel.cod_uf)
            .outerjoin(MunicipioModel, MunicipioModel.cod_municipio == DemandaLocalModel.cod_municipio)
            .filter(DemandaLocalModel.cod_demanda == cod_demanda, DemandaLocalModel.flg_reg_excluido == False)
            .all()
        )
        return [
            {
                "cod_local_demanda": l.cod_local_demanda,
                "cod_demanda":l.cod_demanda,
                "cod_pais": l.cod_pais,
                "nom_pais": nom_pais,
                "cod_uf": l.cod_uf,
                "nom_uf": nom_uf,
                "cod_municipio": l.cod_municipio,
                "nom_municipio": nom_municipio,
                "dsc_local_demanda": l.dsc_local_demanda,
            }
            for l, nom_pais, nom_uf, nom_municipio in rows 
        ]
        
    def _to_dict(self, d: DemandaModel, nom_op: str, dsc_ev: str, locais: list) -> dict: 
        return {
            "cod_demanda": d.cod_demanda,
            "cod_operacao": d.cod_operacao,
            "nom_operacao": nom_op,
            "cod_tipo_evento_demanda": d.cod_tipo_evento_demanda,
            "dsc_evento_tipo": dsc_ev,
            "dsc_atividade": d.dsc_atividade,
            "dsc_responsavel": d.dsc_responsavel,
            "dat_inicio_evento": d.dat_inicio_evento,
            "dat_fim_evento": d.dat_fim_evento,
            "flg_reg_excluido": d.flg_reg_excluido,
            "cif_usuario_inc": d.cif_usuario_inc,
            "cif_usuario_alt": d.cif_usuario_alt,
            "dat_hor_inclusao": d.dat_hor_inclusao,
            "dat_hor_alteracao": d.dat_hor_alteracao,
            "locais": locais,
        }    
        
    def create(self, dto: DemandaCreateDTO) -> model:
        data = dto.model_dump(exclude={"local"}, exclude_unset=True)
        obj = self.model(**data) 
        self.db.add(obj)
        self.db.flush()
        return obj

    def list(self, *, limit: int = 50, offset: int = 0) -> list[DemandaModel]:
        stmt = (
            select(self.model)
            .where(self.model.flg_reg_excluido == False)
            .limit(limit)
            .offset(offset)
        )
        return self.db.execute(stmt).scalars().all()

    def get_by_operacao_id(self, cod_operacao: int, limit: int = 50, offset: int = 0) -> list[DemandaModel]:
        stmt = (
            select(self.model)
            .where(
                self.model.cod_operacao == cod_operacao,
                self.model.flg_reg_excluido == False,
            )
            .limit(limit)
            .offset(offset)
        )

        return self.db.execute(stmt).scalars().all()


    def delete(self, cod_demanda: int, dsc_justificativa_exclusao: str | None = None) -> None:
        demanda = self.get(cod_demanda)
        demanda.flg_reg_excluido = True
        demanda.dsc_justificativa_exclusao = dsc_justificativa_exclusao
        demanda.dat_hor_alteracao = datetime.utcnow()
        for local in demanda.demanda_local:
            local.flg_reg_excluido = True
        self.db.flush()

    def commit(self) -> None:
        self.db.commit()

    def rollback(self):
        self.db.rollback()

