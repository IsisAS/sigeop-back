from fastapi import APIRouter, Depends, Query, Body, Path
from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.core.deps import get_db
from src.modules.demanda.demanda_repository import DemandaRepository
from src.modules.demanda.demanda_schema import (
    DemandaCreateDTO,
    DemandaReadDTO,
    DemandaUpdateDTO,
    DemandaDeleteDTO,
)
from src.modules.demanda.demanda_service import DemandaService
from src.modules.demanda.demanda_local.demanda_local_repository import DemandaLocalRepository
# from src.app_auth import APP_PERMISSIONS
# from src.core.auth.authorization import crud_permission_dependencies

def get_demanda_service(db: Session = Depends(get_db)) -> DemandaService:
    return DemandaService(
        DemandaRepository(db),
        DemandaLocalRepository(db)
        )


crud = CrudRouter[DemandaCreateDTO, DemandaUpdateDTO, DemandaReadDTO, DemandaService](
    prefix="/demanda",
    tags=["Demanda"],
    create_dto=DemandaCreateDTO,
    update_dto=DemandaUpdateDTO,
    read_dto=DemandaReadDTO,
    get_service=get_demanda_service,
    id_param="cod_demanda",
    id_description="ID da demanda",
    operations={"create", "list", "get", "update"},
    # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.demanda),
)

specific_router = APIRouter(prefix="/demanda", tags=["Demanda"])

@specific_router.get("/operacao/{cod_operacao}", response_model=list[DemandaReadDTO])
def get_demandas_by_operacao_id(
    cod_operacao: int,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    service: DemandaService = Depends(get_demanda_service),
):
    return service.get_by_operacao_id(cod_operacao, limit=limit, offset=offset)

@specific_router.delete("/{cod_demanda}", status_code=204)
def delete_demanda(
    cod_demanda: int = Path(..., description="ID da demanda"),
    payload: DemandaDeleteDTO = Body(..., description="Dados para exclusão"),
    service: DemandaService = Depends(get_demanda_service),
):
    service.delete(cod_demanda, dsc_justificativa_exclusao=payload.dsc_justificativa_exclusao)
    return None

router = APIRouter()
router.include_router(specific_router)
router.include_router(crud.router)
