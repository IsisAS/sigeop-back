from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel
from src.modules.recurso_tipo.recurso_tipo_repository import RecursoTipoRepository
from src.modules.recurso_tipo.recurso_tipo_schema import RecursoTipoCreateDTO, RecursoTipoReadDTO, RecursoTipoUpdateDTO


class RecursoTipoService(AbstractService[RecursoTipoModel, RecursoTipoCreateDTO, RecursoTipoReadDTO, RecursoTipoUpdateDTO]):
    read_dto = RecursoTipoReadDTO

    def __init__(self, repo: RecursoTipoRepository):
        self.repository = repo