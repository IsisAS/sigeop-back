from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository
from src.modules.plano.plano_missao.plano_missao_schema import (
    PlanoMissaoCreateDTO,
    PlanoMissaoReadDTO,
    PlanoMissaoUpdateDTO,
)
from src.modules.plano.plano_missao.plano_missao_service import PlanoMissaoService
from src.modules.plano.plano_repository import PlanoRepository
from src.modules.plano.plano_schema import PlanoReadDTO


def get_plano_missao_service(db: Session) -> PlanoMissaoService:
    return PlanoMissaoService(
        db,
        PlanoRepository(db),
        PlanoLocalRepository(db),
    )


router = APIRouter(prefix="/plano-missao", tags=["Plano Missão"])

@router.get("/missao/{cod_missao}", response_model=List[PlanoReadDTO])
def list_by_missao(
    cod_missao: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    service = get_plano_missao_service(db)
    return service.list_by_missao(
        cod_missao=cod_missao,
        limit=limit,
        offset=offset,
    )


@router.get("/{cod_plano}", response_model=PlanoReadDTO)
def get_by_id(
    cod_plano: int,
    db: Session = Depends(get_db),
):
    service = get_plano_missao_service(db)
    return service.get(cod_plano)


@router.post("", response_model=PlanoMissaoReadDTO)
def create(
    payload: PlanoMissaoCreateDTO,
    db: Session = Depends(get_db),
):
    service = get_plano_missao_service(db)
    return service.create(payload)


@router.put("/{cod_plano}", response_model=PlanoMissaoReadDTO)
def update(
    cod_plano: int,
    payload: PlanoMissaoUpdateDTO,
    db: Session = Depends(get_db),
):
    service = get_plano_missao_service(db)
    return service.update(cod_plano, payload)
