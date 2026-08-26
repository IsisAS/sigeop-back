from sqlalchemy.orm import Session

from src.common.router import CrudRouter
from src.modules.pedido.status.status_repository import StatusRepository
from src.modules.pedido.status.status_schema import StatusCreateDTO, StatusReadDTO, StatusUpdateDTO
from src.modules.pedido.status.status_service import StatusService
# # from src.app_auth import APP_PERMISSIONS
# # from src.core.auth.authorization import crud_permission_dependencies


def get_status_service(db: Session) -> StatusService:
    return StatusService(StatusRepository(db))

crud = CrudRouter(
    prefix="/pedido/status",
    tags=["PedidoStatus"],
    create_dto=StatusCreateDTO,
    update_dto=StatusUpdateDTO,
    read_dto= StatusReadDTO,
    get_service=get_status_service,
    id_param="cod_pedido_status",
    id_description="ID do status do pedido",
    operations={"list"},
    # # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.pedido),
)

router = crud.router
