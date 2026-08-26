from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.modules.plano.plano_status.plano_status_service import PlanoStatusService
from src.modules.plano.plano_status.plano_status_repository import PlanoStatusRepository
from src.modules.plano.plano_status.plano_status_schema import PlanoStatusUpdateDTO, PlanoStatusCreateDTO, PlanoStatusReadDTO


def get_plano_status_service(db: Session) -> PlanoStatusService:
    return PlanoStatusService(PlanoStatusRepository(db))

crud = CrudRouter(
    prefix="/plano/status",
    tags=["Plano Status"],
    create_dto=PlanoStatusCreateDTO,
    update_dto=PlanoStatusUpdateDTO,
    read_dto= PlanoStatusReadDTO,
    get_service=get_plano_status_service,
    id_param="cod_plano_status",
    id_description="ID do plano status",
    operations={'list'}
)

router = crud.router
