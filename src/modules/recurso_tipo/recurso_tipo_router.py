from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.modules.recurso_tipo.recurso_tipo_repository import RecursoTipoRepository
from src.modules.recurso_tipo.recurso_tipo_schema import RecursoTipoCreateDTO, RecursoTipoReadDTO, RecursoTipoUpdateDTO
from src.modules.recurso_tipo.recurso_tipo_service import RecursoTipoService


def get_recurso_tipo_service(db: Session) -> RecursoTipoService:
    return RecursoTipoService(RecursoTipoRepository(db))

crud = CrudRouter(
    prefix="/recurso/tipo",
    tags=["Recurso Tipo"],
    create_dto=RecursoTipoCreateDTO,
    update_dto=RecursoTipoUpdateDTO,
    read_dto= RecursoTipoReadDTO,
    get_service=get_recurso_tipo_service,
    id_param="cod_recurso_tipo",
    id_description="ID do Recurso caso",
    operations={'list'}
)

router = crud.router
