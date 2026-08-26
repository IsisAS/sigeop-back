from typing import List
from src.core.deps import get_db
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.modules.plano.plano_schema import PlanoReadDTO, PlanoUpdateDTO, PlanoCreateDTO
from src.modules.plano.plano_repository import PlanoRepository
from src.modules.plano.plano_service import PlanoService
from src.modules.plano.plano_equipe.plano_equipe_repository import PlanoEquipeRepository
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository

def get_plano_service(db: Session) -> PlanoService:
    return PlanoService(
        PlanoRepository(db),
        PlanoEquipeRepository(db),
        PlanoLocalRepository(db)
        )

crud = CrudRouter(
    prefix="/plano",
    tags=["Plano"],
    create_dto=PlanoCreateDTO,
    update_dto=PlanoUpdateDTO,
    read_dto= PlanoReadDTO,
    get_service=get_plano_service,
    id_param="cod_plano",
    id_description="ID do plano",
    operations={"list", "get", "create", "update"}
)

router = crud.router

@router.get("/caso/{cod_caso}", response_model=List[PlanoReadDTO])
def get_plano_by_caso_id(
    cod_caso:int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retorna todos os planos vinculados a um caso"""
    service = get_plano_service(db)
    return service.get_by_caso_id(
        cod_caso=cod_caso,
        limit=limit,
        offset=offset
    )

@router.get("/operacao/{cod_operacao}", response_model=List[PlanoReadDTO])
def get_plano_by_caso_id(
    cod_operacao:int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retorna todos os planos vinculados a um caso"""
    service = get_plano_service(db)
    return service.get_by_operacao_id(
        cod_operacao=cod_operacao,
        limit=limit,
        offset=offset
    )


@router.get("/missao/{cod_missao}", response_model=List[PlanoReadDTO])
def get_plano_by_caso_id(
    cod_missao:int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retorna todos os planos vinculados a um caso"""
    service = get_plano_service(db)
    return service.get_by_missao_id(
        cod_missao=cod_missao,
        limit=limit,
        offset=offset
    )