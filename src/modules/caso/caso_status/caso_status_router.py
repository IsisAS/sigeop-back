from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.modules.caso.caso_status.caso_status_repository import CasoStatusRepository
from src.modules.caso.caso_status.caso_status_schema import CasoStatusCreateDTO, CasoStatusUpdateDTO, CasoStatusReadDTO
from src.modules.caso.caso_status.caso_status_service import CasoStatusService

def get_caso_status_service(db: Session) -> CasoStatusService:
    return CasoStatusService(CasoStatusRepository(db))

crud = CrudRouter(
    prefix="/caso/status",
    tags=["Caso Status"],
    create_dto=CasoStatusCreateDTO,
    update_dto=CasoStatusUpdateDTO,
    read_dto= CasoStatusReadDTO,
    get_service=get_caso_status_service,
    id_param="cod_caso_status",
    id_description="ID do caso status",
    operations={'list'}
)

router = crud.router
