from sqlalchemy.orm import Session

from src.common.router import CrudRouter
from src.modules.pedido.analista.analista_repository import AnalistaRepository
from src.modules.pedido.analista.analista_schema import AnalistaCreateDTO, AnalistaReadDTO, AnalistaUpdateDTO
from src.modules.pedido.analista.analista_service import AnalistaService
# # from src.app_auth import APP_PERMISSIONS
# # from src.core.auth.authorization import crud_permission_dependencies


def get_analista_service(db: Session) -> AnalistaService:
    return AnalistaService(AnalistaRepository(db))

crud = CrudRouter(
    prefix="/pedido/analista",
    tags=["Analista"],
    create_dto=AnalistaCreateDTO,
    update_dto=AnalistaUpdateDTO,
    read_dto= AnalistaReadDTO,
    get_service=get_analista_service,
    id_param="cod_pedido_analista",
    id_description="ID do analista do pedido",
    operations={"create", "list"},
    # # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.pedidoAnalista),
)

router = crud.router
