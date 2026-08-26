from src.common.service import AbstractService
from typing import List
from src.modules.plano.plano_model import PlanoModel
from src.modules.plano.plano_repository import PlanoRepository
from src.modules.plano.plano_schema import PlanoCreateDTO, PlanoReadDTO, PlanoUpdateDTO
from src.core.errors.errors import NotFoundError
from src.modules.plano.plano_equipe.plano_equipe_schema import PlanoEquipeCreateDTO, PlanoEquipeUpdateDTO
from src.modules.plano.plano_equipe.plano_equipe_repository import PlanoEquipeRepository
from src.modules.plano.plano_local.plano_local_schema import PlanoLocalCreateDTO, PlanoLocalUpdateDTO
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository


class PlanoService(AbstractService[PlanoModel, PlanoCreateDTO, PlanoUpdateDTO, PlanoReadDTO]):
    read_dto = PlanoReadDTO

    def __init__(
        self, 
        repository: PlanoRepository,
        plano_equipe_repository: PlanoEquipeRepository,
        plano_local_repository: PlanoLocalRepository
        ):
        self.repository = repository
        self.plano_equipe_repository = plano_equipe_repository
        self.plano_local_repository = plano_local_repository


    def list(self, *, limit: int = 50, offset: int = 0) -> list[PlanoReadDTO]:
        plano_list = self.repository.list(limit = limit, offset = offset)
        return [PlanoReadDTO.from_model(item) for item in plano_list]

    def create(self, dto: PlanoCreateDTO) -> PlanoReadDTO:
        try:
            equipes = dto.plano_equipe
            locais = dto.local
            plano_model = self.repository.create(dto)

            if plano_model:
                for equipe in equipes:
                    equipe_plano_create = PlanoEquipeCreateDTO(
                        cod_plano = plano_model.cod_plano,
                        cod_agente = equipe.cod_agente,
                        cod_papel = equipe.cod_papel,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                    self.plano_equipe_repository.create(equipe_plano_create)

                for local in locais:
                    local_plano_create = PlanoLocalCreateDTO(
                        cod_plano = plano_model.cod_plano,
                        cod_pais = local.cod_pais,
                        cod_uf = local.cod_uf,
                        cod_municipio = local.cod_municipio,
                        dsc_local = local.dsc_local,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                    self.plano_local_repository.create(local_plano_create)
                
            self.repository.commit()
            return self.read_dto.from_model(plano_model)

        except Exception:
            self.repository.rollback()
            raise

    def get(self, entity_id: str) -> PlanoReadDTO:
        plano_list = self.repository.get(entity_id)

        return PlanoReadDTO.from_model(plano_list)

    def update(self, cod_plano: str, dto: PlanoUpdateDTO) -> PlanoReadDTO:
        equipes = dto.plano_equipe
        locais = dto.local
        plano_model = self.repository.update(cod_plano, dto)

        if not plano_model:
            raise NotFoundError("Plano não encontrado")

        self._sync_equipes(plano_model.cod_plano, equipes)
        self._sync_locais(plano_model.cod_plano, locais)

        self.repository.commit()
        return PlanoReadDTO.from_model(plano_model)

    def _sync_equipes(self, cod_plano: int, equipes_dto:list):
        equipes_banco = self.plano_equipe_repository.get_by_plano_id(cod_plano)

        ids_banco = { equipe.cod_plano_equipe for equipe in equipes_banco }

        ids_recebidos = {equipe.cod_plano_equipe for equipe in equipes_dto if equipe.cod_plano_equipe is not None}

        ids_para_remover = ids_banco - ids_recebidos

        for cod_plano_equipe in ids_para_remover:
            self.plano_equipe_repository.delete(cod_plano_equipe)

        for equipe in equipes_dto:
            if equipe.cod_plano_equipe:
                self.plano_equipe_repository.update(
                    equipe.cod_plano_equipe,
                    PlanoEquipeUpdateDTO(
                        cod_plano = cod_plano,
                        cod_agente = equipe.cod_agente,
                        cod_papel = equipe.cod_papel,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                )
            else:
                self.plano_equipe_repository.create(
                    PlanoEquipeCreateDTO(
                        cod_plano = cod_plano,
                        cod_agente = equipe.cod_agente,
                        cod_papel = equipe.cod_papel,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                )

    def _sync_locais(self, cod_plano: int, locais_dto:list):
        locais_banco = self.plano_local_repository.get_by_plano_id(cod_plano)

        ids_banco = { local.cod_plano_local for local in locais_banco }

        ids_recebidos = {local.cod_plano_local for local in locais_dto if local.cod_plano_local is not None}

        ids_para_remover = ids_banco - ids_recebidos

        for cod_plano_local in ids_para_remover:
            self.plano_local_repository.delete(cod_plano_local)

        for local in locais_dto:
            if local.cod_plano_local:
                self.plano_local_repository.update(
                    local.cod_plano_local,
                    PlanoLocalUpdateDTO(
                        cod_plano = cod_plano,
                        cod_pais = local.cod_pais,
                        cod_uf = local.cod_uf,
                        cod_municipio = local.cod_municipio,
                        dsc_local = local.dsc_local,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                )
            else:
                self.plano_local_repository.create(
                    PlanoLocalCreateDTO(
                        cod_plano = cod_plano,
                        cod_pais = local.cod_pais,
                        cod_uf = local.cod_uf,
                        cod_municipio = local.cod_municipio,
                        dsc_local = local.dsc_local,
                        cif_usuario_inc = 1,
                        cif_usuario_alt = 1
                    )
                )

    def get_by_caso_id(self, cod_caso: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        plano_model_list = self.repository.get_by_caso_id(
            cod_caso=cod_caso,
            limit=limit,
            offset=offset
        )
        return [self.read_dto.from_model(item) for item in plano_model_list]

    def get_by_operacao_id(self, cod_operacao: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        plano_model_list = self.repository.get_by_operacao_id(
            cod_operacao=cod_operacao,
            limit=limit,
            offset=offset
        )
        return [self.read_dto.from_model(item) for item in plano_model_list]

    def get_by_missao_id(self, cod_missao: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        plano_model_list = self.repository.get_by_missao_id(
            cod_missao=cod_missao,
            limit=limit,
            offset=offset
        )
        return [self.read_dto.from_model(item) for item in plano_model_list]
