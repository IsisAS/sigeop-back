from typing import List
from src.common.service import AbstractService
from src.modules.demanda.demanda_model import DemandaModel
from src.modules.demanda.demanda_repository import DemandaRepository
from src.modules.demanda.demanda_schema import (
    DemandaCreateDTO,
    DemandaReadDTO,
    DemandaUpdateDTO,
)
from src.core.errors.errors import NotFoundError, ConflictError
from src.modules.demanda.demanda_local.demanda_local_repository import DemandaLocalRepository
from src.modules.demanda.demanda_local.demanda_local_schema import DemandaLocalCreateDTO, DemandaLocalUpdateDTO
from src.modules.operacao.operacao_model import OperacaoModel

class DemandaService(AbstractService[DemandaModel, DemandaCreateDTO, DemandaReadDTO, DemandaUpdateDTO]):
    read_dto = DemandaReadDTO

    def __init__(
        self, 
        repository: DemandaRepository,
        demanda_local_repository: DemandaLocalRepository
        ):
        self.repository = repository
        self.demanda_local_repository = demanda_local_repository

    def create(self, dto: DemandaCreateDTO) -> DemandaReadDTO:
        try:
            locais = dto.local or []
            demanda_model = self.repository.create(dto)

            if demanda_model:
                for local in locais:
                    demanda_local_create = DemandaLocalCreateDTO(
                        cod_demanda = demanda_model.cod_demanda,
                        cod_pais = local.cod_pais,
                        cod_uf = local.cod_uf,
                        cod_municipio = local.cod_municipio,
                        dsc_local_demanda = local.dsc_local_demanda,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                    self.demanda_local_repository.create(demanda_local_create)
                
                self.repository.commit()
                return self.read_dto.from_model(demanda_model)

        except Exception:
            self.repository.rollback()
            raise
        
    def list(self, *, limit: int = 50, offset: int = 0) -> List[DemandaReadDTO]:
        demanda_list = self.repository.list(limit = limit, offset = offset)
        return [DemandaReadDTO.from_model(item) for item in demanda_list] 
    
    def get(self, cod_demanda: int) -> DemandaReadDTO:
        item = self.repository.get(cod_demanda)
        return DemandaReadDTO.from_model(item)

    def get_by_operacao_id(
        self,
        cod_operacao: int,
        limit: int = 50,
        offset: int = 0,
    ) -> List[DemandaReadDTO]:
        demanda_list = self.repository.get_by_operacao_id(cod_operacao, limit=limit, offset=offset)
        return [DemandaReadDTO.from_model(item) for item in demanda_list]
    
    def update(self, cod_demanda: int, dto: DemandaUpdateDTO) -> DemandaReadDTO:
        locais = dto.local or []
        demanda_model = self.repository.update(cod_demanda, dto)
           
        self._sync_locais(demanda_model.cod_demanda, locais)

        self.repository.commit()
        return DemandaReadDTO.from_model(demanda_model)

     
        
    def _sync_locais(self, cod_demanda: int, locais_dto:list):
        locais_banco = self.demanda_local_repository.get_by_demanda_id(cod_demanda)

        ids_banco = { local.cod_local_demanda for local in locais_banco }

        ids_recebidos = {local.cod_local_demanda for local in locais_dto if local.cod_local_demanda is not None}

        ids_para_remover = ids_banco - ids_recebidos

        for cod_local_demanda in ids_para_remover:
            self.demanda_local_repository.delete(cod_local_demanda)
            
        for local in locais_dto:
            if local.cod_local_demanda:
                self.demanda_local_repository.update(
                    local.cod_local_demanda,
                    DemandaLocalUpdateDTO(
                        cod_demanda = cod_demanda,
                        cod_pais = local.cod_pais,
                        cod_uf = local.cod_uf,
                        cod_municipio = local.cod_municipio,
                        dsc_local_demanda = local.dsc_local_demanda,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                )
            else:
                self.demanda_local_repository.create(
                    DemandaLocalCreateDTO(
                        cod_demanda = cod_demanda,
                        cod_pais = local.cod_pais,
                        cod_uf = local.cod_uf,
                        cod_municipio = local.cod_municipio,
                        dsc_local_demanda = local.dsc_local_demanda,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                )

    def delete(self, cod_demanda: int, dsc_justificativa_exclusao: str) -> None:
        demanda = self.repository.get(cod_demanda)

        if demanda.cod_operacao is not None:
            operacao_tipo = (
                self.repository.db.query(OperacaoModel.cod_operacao_tipo)
                .filter(OperacaoModel.cod_operacao == demanda.cod_operacao)
                .scalar()
            )
            COD_OPERACAO_TIPO_INTELIGENCIA_PROTECAO = 6
            if operacao_tipo == COD_OPERACAO_TIPO_INTELIGENCIA_PROTECAO:
                raise ConflictError(
                    "A Demanda está vinculada a uma Operação de Inteligência de Proteção e não pode ser excluída."
                )

        try:
            self.repository.delete(
                cod_demanda,
                dsc_justificativa_exclusao=dsc_justificativa_exclusao,
            )
            self.repository.commit()
        except Exception:
            self.repository.rollback()
            raise
