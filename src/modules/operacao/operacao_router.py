from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, Query, Body, Path

from src.core.deps import get_db
from src.common.router import CrudRouter
from src.modules.operacao.operacao_repository import OperacaoRepository
from src.modules.operacao.operacao_schema import OperacaoCreateDTO, OperacaoReadDTO, OperacaoUpdateDTO, GridMissaoDTO, GridPlanoDTO, OperacaoInteligenciaProtecaoGridDTO, OperacaoDeleteDTO
from src.modules.operacao.operacao_service import OperacaoService
from src.modules.pedido.pedido_schema import PedidoReadDTO

def get_operacao_service(db: Session) -> OperacaoService:
    return OperacaoService(OperacaoRepository(db))

crud = CrudRouter(
    prefix="/operacao",
    tags=["Operacao"],
    create_dto=OperacaoCreateDTO,
    update_dto=OperacaoUpdateDTO,
    read_dto= OperacaoReadDTO,
    get_service=get_operacao_service,
    id_param="cod_operacao",
    id_description="ID da Operacao",
    operations={"list", "get", "create", "update"}
)

specific_router = APIRouter(
    prefix="/operacao",
    tags=["Operacao"],
)

@specific_router.get("/inteligencia-protecao", response_model=List[OperacaoInteligenciaProtecaoGridDTO])
def listar_inteligencia_protecao(
    limit: int = Query(10000, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    service = get_operacao_service(db)
    return service.listar_inteligencia_protecao(limit=limit, offset=offset)

@specific_router.get("/caso/{caso_id}", response_model=List[OperacaoReadDTO])
def get_operacao_by_caso_id(
    caso_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    service = get_operacao_service(db)
    return service.get_by_caso(caso_id)

@specific_router.get("/{cod_operacao}/missoes", response_model=List[GridMissaoDTO])
def get_missoes_da_operacao(cod_operacao: int, db: Session = Depends(get_db)):
    """Retorna as missões vinculadas à operação para a grid."""
    service = get_operacao_service(db)
    return service.listar_missoes_por_operacao(cod_operacao)

@specific_router.get("/{cod_operacao}/planos", response_model=List[GridPlanoDTO])
def get_planos_da_operacao(cod_operacao: int, db: Session = Depends(get_db)):
    """Retorna os planos vinculados à operação para a grid."""
    service = get_operacao_service(db)
    return service.listar_planos_por_operacao(cod_operacao)

@specific_router.get("/{cod_operacao}/pedidos", response_model=List[PedidoReadDTO])
def get_pedidos_da_operacao(cod_operacao: int, db: Session = Depends(get_db)):
    """Retorna os pedidos vinculados à operação para a grid."""
    service = get_operacao_service(db)
    return service.listar_pedidos_por_operacao(cod_operacao)

@specific_router.delete("/{cod_operacao}", status_code=204)
def delete_operacao(
    cod_operacao: int = Path(..., description="ID da Operação"),
    payload: OperacaoDeleteDTO = Body(..., description="Dados para exclusão"),
    db: Session = Depends(get_db),
):
    service = get_operacao_service(db)
    service.delete(cod_operacao, dsc_justificativa_exclusao=payload.dsc_justificativa_exclusao)
    return None

router = APIRouter()
router.include_router(specific_router)
router.include_router(crud.router)
