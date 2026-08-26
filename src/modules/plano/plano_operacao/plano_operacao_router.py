from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db
from src.modules.plano.plano_operacao.plano_operacao_schema import (
    PlanoOperacaoCreateDTO,
    PlanoOperacaoReadDTO,
    PlanoOperacaoUpdateDTO,
)
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository
from src.modules.plano.plano_repository import PlanoRepository
from src.modules.plano.plano_schema import PlanoReadDTO
from src.modules.plano.plano_operacao.plano_operacao_service import PlanoOperacaoService


def get_plano_operacao_service(db: Session) -> PlanoOperacaoService:
    return PlanoOperacaoService(
        db,
        PlanoRepository(db),
        PlanoLocalRepository(db),
    )


router = APIRouter(prefix="/plano-operacao", tags=["Plano Operação"])


@router.get("/operacao/{cod_operacao}", response_model=List[PlanoReadDTO])
def list_by_operacao(
    cod_operacao: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    service = get_plano_operacao_service(db)
    return service.list_by_operacao(
        cod_operacao=cod_operacao,
        limit=limit,
        offset=offset,
    )


@router.get("/{cod_plano}", response_model=PlanoReadDTO)
def get_by_id(
    cod_plano: int,
    db: Session = Depends(get_db),
):
    service = get_plano_operacao_service(db)
    return service.get(cod_plano)


@router.post("", response_model=PlanoOperacaoReadDTO)
def create(
    payload: PlanoOperacaoCreateDTO,
    db: Session = Depends(get_db),
):
    service = get_plano_operacao_service(db)
    return service.create(payload)


@router.put("/{cod_plano}", response_model=PlanoOperacaoReadDTO)
def update(
    cod_plano: int,
    payload: PlanoOperacaoUpdateDTO,
    db: Session = Depends(get_db),
):
    service = get_plano_operacao_service(db)
    return service.update(cod_plano, payload)
