from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.modules.plano.plano_caso.plano_caso_schema import (
    PlanoCasoCreateDTO,
    PlanoCasoReadDTO,
    PlanoCasoUpdateDTO,
)
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository
from src.modules.plano.plano_repository import PlanoRepository
from src.modules.plano.plano_schema import PlanoReadDTO
from src.modules.plano.plano_caso.plano_caso_service import PlanoCasoService


def get_plano_caso_service(db: Session) -> PlanoCasoService:
    return PlanoCasoService(
        db,
        PlanoRepository(db),
        PlanoLocalRepository(db),
    )


router = APIRouter(prefix="/plano-caso", tags=["Plano Caso"])


@router.get("/caso/{cod_caso}", response_model=List[PlanoReadDTO])
def list_by_caso(
    cod_caso: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    service = get_plano_caso_service(db)
    return service.list_by_caso(
        cod_caso=cod_caso,
        limit=limit,
        offset=offset,
    )


@router.get("/{cod_plano}", response_model=PlanoReadDTO)
def get_by_id(
    cod_plano: int,
    db: Session = Depends(get_db),
):
    service = get_plano_caso_service(db)
    return service.get(cod_plano)


@router.post("", response_model=PlanoCasoReadDTO)
def create(
    payload: PlanoCasoCreateDTO,
    db: Session = Depends(get_db),
):
    service = get_plano_caso_service(db)
    return service.create(payload)


@router.put("/{cod_plano}", response_model=PlanoCasoReadDTO)
def update(
    cod_plano: int,
    payload: PlanoCasoUpdateDTO,
    db: Session = Depends(get_db),
):
    service = get_plano_caso_service(db)
    return service.update(cod_plano, payload)