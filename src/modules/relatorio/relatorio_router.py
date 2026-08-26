from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.common.router import CrudRouter
from src.core.deps import get_db
from src.modules.relatorio.relatorio_repository import RelatorioRepository
from src.modules.relatorio.relatorio_schema import (
    RelatorioCreateDTO,
    RelatorioPedidoResumoDTO,
    RelatorioReadDTO,
    RelatorioStatusDTO,
    RelatorioTipoDTO,
    RelatorioUpdateDTO,
)
from src.modules.relatorio.relatorio_service import RelatorioService
# from src.app_auth import APP_PERMISSIONS
# from src.core.auth.authorization import crud_permission_dependencies


def get_relatorio_service(db: Session = Depends(get_db)) -> RelatorioService:
    return RelatorioService(RelatorioRepository(db))


specific_router = APIRouter(prefix="/relatorio", tags=["Relatório"])


@specific_router.get("/tipos", response_model=list[RelatorioTipoDTO])
def listar_tipos(service: RelatorioService = Depends(get_relatorio_service)):
    return service.list_tipos()


@specific_router.get("/status", response_model=list[RelatorioStatusDTO])
def listar_status(service: RelatorioService = Depends(get_relatorio_service)):
    return service.list_status()


@specific_router.get("/pedidos-elegiveis", response_model=list[RelatorioPedidoResumoDTO])
def listar_pedidos_elegiveis(service: RelatorioService = Depends(get_relatorio_service)):
    return service.list_pedidos_elegiveis()


crud = CrudRouter(
    prefix="/relatorio",
    tags=["Relatório"],
    create_dto=RelatorioCreateDTO,
    update_dto=RelatorioUpdateDTO,
    read_dto=RelatorioReadDTO,
    get_service=get_relatorio_service,
    id_param="cod_relatorio",
    id_description="ID do relatório",
    operations={"create", "list", "get", "update"},
    # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.relatorio),
)

router = APIRouter()
router.include_router(specific_router)
router.include_router(crud.router)
