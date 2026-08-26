from src.common.repository import AbstractRepository
from src.modules.caso.caso_encarregado.caso_encarregado_model import CasoEncarregadoModel
from src.modules.caso.caso_encarregado.caso_encarregado_schema import CasoEncarregadoCreateDTO, CasoEncarregadoUpdateDTO
from sqlalchemy import select, func
from typing import Tuple

class CasoEncarregadoRepository(AbstractRepository[CasoEncarregadoModel, CasoEncarregadoCreateDTO, CasoEncarregadoUpdateDTO]):
    model = CasoEncarregadoModel

    def _obter_models_de_dtos(self, casos_encarregados_dto: list[CasoEncarregadoCreateDTO]) -> list[CasoEncarregadoModel]:
        casos_encarregados_model: list[CasoEncarregadoModel] = []
        for encarregado_dto in casos_encarregados_dto:
            data = encarregado_dto.model_dump()
            obj = self.model(**data)
            casos_encarregados_model.append(obj)
        return casos_encarregados_model

    def create(self, casos_encarregados_dto: list[CasoEncarregadoCreateDTO]) -> list[CasoEncarregadoModel]:
        models = self._obter_models_de_dtos(casos_encarregados_dto)
        self.db.add_all(models)
        self.db.flush()
        return models

    def obter_encarregados_associados_a_caso(self, caso_id: int) -> list[CasoEncarregadoModel]:
        query_encarregados = select(self.model).where(self.model.cod_caso == caso_id)
        
        encarregados = self.db.execute(query_encarregados).scalars().all()
        
        for encarregado_model in encarregados:
            setattr(encarregado_model, "nom_agente", None)
            
        return list(encarregados)
    
    def _obter_encarregados_a_serem_salvos_e_atualizados(
        self,
        casos_encarregados_por_id: dict,
        casos_encarregados_dto: list[CasoEncarregadoUpdateDTO], 
        ) -> Tuple[list[CasoEncarregadoCreateDTO], list[CasoEncarregadoUpdateDTO]]:

        encarregados_para_criar = []
        encarregados_para_atualizar = []

        for encarregado_dto in casos_encarregados_dto:
            cod_agente = encarregado_dto.cod_agente
            encarregado_model = casos_encarregados_por_id.get(cod_agente)
            if encarregado_model != None:
                encarregados_para_atualizar.append(encarregado_dto)
                continue
            
            encarregado_para_criar = CasoEncarregadoCreateDTO.from_update_dto(encarregado_dto)
            encarregados_para_criar.append(encarregado_para_criar)
        
        return encarregados_para_criar, encarregados_para_atualizar
    
    def _atualizar_encarregados(
        self, 
        encarregados_por_id, 
        encarregados_para_criar, 
        encarregados_para_atualizar) -> list[CasoEncarregadoModel]:

        encarregados_criados = self.create(encarregados_para_criar)
        encarregados = []
        encarregados.extend(encarregados_criados)
        for encarregado_para_atualizar in encarregados_para_atualizar:
            cod_agente = encarregado_para_atualizar.cod_agente
            model = encarregados_por_id.get(cod_agente)

            obj_atualizado = self.update_sem_commit(model, encarregado_para_atualizar)
            encarregados.append(obj_atualizado)
        
        return encarregados

    def atualizar_encarregados_associadoas_a_caso(
        self, 
        cod_caso: int, 
        casos_encarregados_dto: list[CasoEncarregadoUpdateDTO]
        ) -> list[CasoEncarregadoModel]:
        encarregados_do_caso = self.obter_encarregados_associados_a_caso(cod_caso)
        encarregados_por_id = {c.cod_agente: c for c in encarregados_do_caso}
        encarregados_para_criar, encarregados_para_atualizar = self._obter_encarregados_a_serem_salvos_e_atualizados(
            encarregados_por_id, 
            casos_encarregados_dto, 
            )
        
        encarregados = self._atualizar_encarregados(
            encarregados_por_id, 
            encarregados_para_criar, 
            encarregados_para_atualizar
            )
        
        return encarregados
    
    def update_sem_commit(self, obj: CasoEncarregadoModel, dto: CasoEncarregadoUpdateDTO) -> CasoEncarregadoModel:
        cod_caso_encarregado = obj.cod_caso_encarregado
        dto.cod_caso_encarregado = cod_caso_encarregado

        data = dto.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(obj, k, v)

        self.db.add(obj)
        self.db.flush()
        return obj

    def obter_qtde_encarregados_ativos_associados_a_caso(self, cod_caso: int) -> int:
        query_encarregados = (
            select(func.count())
            .select_from(self.model)
            .where(
                self.model.flg_reg_excluido == False,
                self.model.cod_caso == cod_caso
            )
        )

        qtde_encarregados = self.db.execute(query_encarregados).scalar_one()
        return qtde_encarregados