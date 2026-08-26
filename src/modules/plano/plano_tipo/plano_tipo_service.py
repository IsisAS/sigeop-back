from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.plano.plano_tipo.plano_tipo_model import PlanoTipoModel
from src.modules.plano.plano_tipo.plano_tipo_schema import PlanoTipoReadDTO, PlanoTipoUpdateDTO, PlanoTipoCreateDTO
from src.modules.plano.plano_tipo.plano_tipo_repository import PlanoTipoRepository

class PlanoTipoService(AbstractService[PlanoTipoModel, PlanoTipoCreateDTO, PlanoTipoReadDTO, PlanoTipoUpdateDTO]):
    read_dto = PlanoTipoReadDTO

    def __init__(self, repo: PlanoTipoRepository):
        self.repository = repo