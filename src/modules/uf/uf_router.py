from typing import List
from src.core.deps import get_db
from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from fastapi import APIRouter, Depends, Query
from src.modules.uf.uf_schema import UfReadDTO, UfUpdateDTO, UfCreateDTO
from src.modules.uf.uf_repository import UfRepository
from src.modules.uf.uf_service import UfService

def get_uf_service(db: Session) -> UfService:
    return UfService(
        UfRepository(db),
    )

crud = CrudRouter(
    prefix="/uf",
    tags=["Uf"],
    create_dto=UfCreateDTO,
    update_dto=UfUpdateDTO,
    read_dto= UfReadDTO,
    get_service=get_uf_service,
    id_param="cod_uf",
    id_description="ID do uf",
    operations={'list', 'get', 'create'}
)

router = crud.router

@router.get("/pais/{cod_pais}", response_model=List[UfReadDTO])
def get_uf_by_pais_id(
    cod_pais: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retorna todos as UF de um pais"""
    service = get_uf_service(db)
    return service.get_by_pais_id(
        cod_pais=cod_pais,
        limit=limit,
        offset=offset
    )