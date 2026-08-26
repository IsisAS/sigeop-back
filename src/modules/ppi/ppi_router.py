from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from fastapi import APIRouter, Depends, Query
from src.core.deps import get_db
from src.modules.ppi.ppi_schema import PPIReadDTO, PPIUpdateDTO, PPICreateDTO
from src.modules.ppi.ppi_repository import PPIRepository
from src.modules.ppi.ppi_service import PPIService

def get_ppi_service(db: Session) -> PPIService:
    return PPIService(PPIRepository(db))

crud = CrudRouter(
    prefix="/ppi",
    tags=["PPI"],
    create_dto=PPICreateDTO,
    update_dto=PPIUpdateDTO,
    read_dto= PPIReadDTO,
    get_service=get_ppi_service,
    id_param="cod_ppi",
    id_description="ID do ppi",
    operations={'list', 'get', 'update', 'create'}
)

router = crud.router

@router.put("/status/{cod_ppi}", response_model=PPIReadDTO)
def alterar_status_ppi(
    cod_ppi: int,
    status: bool,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    service = get_ppi_service(db)
    return service.alterar_status_ppi(cod_ppi, status)