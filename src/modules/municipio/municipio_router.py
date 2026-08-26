from typing import List
from src.core.deps import get_db
from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from fastapi import APIRouter, Depends, Query
from src.modules.municipio.municipio_schema import MunicipioReadDTO, MunicipioUpdateDTO, MunicipioCreateDTO
from src.modules.municipio.municipio_repository import MunicipioRepository
from src.modules.municipio.municipio_service import MunicipioService

def get_municipio_service(db: Session) -> MunicipioService:
    return MunicipioService(
        MunicipioRepository(db),
    )

crud = CrudRouter(
    prefix="/municipio",
    tags=["Municipio"],
    create_dto=MunicipioCreateDTO,
    update_dto=MunicipioUpdateDTO,
    read_dto= MunicipioReadDTO,
    get_service=get_municipio_service,
    id_param="cod_municipio",
    id_description="ID do municipio",
    operations={'list', 'get', 'create'}
)

router = crud.router

@router.get("/uf/{cod_uf}", response_model=List[MunicipioReadDTO])
def get_municipios_by_uf_id(
    cod_uf: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retorna todos as UF de um pais"""
    service = get_municipio_service(db)
    return service.get_by_uf_id(
        cod_uf=cod_uf,
        limit=limit,
        offset=offset
    )