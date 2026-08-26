from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.modules.plano.plano_tipo.plano_tipo_schema import PlanoTipoReadDTO, PlanoTipoUpdateDTO, PlanoTipoCreateDTO
from src.modules.plano.plano_tipo.plano_tipo_repository import PlanoTipoRepository
from src.modules.plano.plano_tipo.plano_tipo_service import PlanoTipoService

def get_plano_tipo_service(db: Session) -> PlanoTipoService:
    return PlanoTipoService(PlanoTipoRepository(db))

crud = CrudRouter(
    prefix="/plano/tipo",
    tags=["Plano Tipo"],
    create_dto=PlanoTipoCreateDTO,
    update_dto=PlanoTipoUpdateDTO,
    read_dto= PlanoTipoReadDTO,
    get_service=get_plano_tipo_service,
    id_param="cod_plano_tipo",
    id_description="ID do plano tipo",
    operations={'list'}
)

router = crud.router
