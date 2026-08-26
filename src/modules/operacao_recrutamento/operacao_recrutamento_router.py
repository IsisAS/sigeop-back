from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.core.deps import get_db
from src.modules.operacao_recrutamento.operacao_recrutamento_repository import (OperacaoRecrutamentoRepository,)
from src.modules.operacao_recrutamento.operacao_recrutamento_schema import (OperacaoRecrutamentoReadDTO,)
from src.modules.operacao_recrutamento.operacao_recrutamento_service import (OperacaoRecrutamentoService,)

def get_operacao_recrutamento_service(db: Session = Depends(get_db)) -> OperacaoRecrutamentoService:
    return OperacaoRecrutamentoService(OperacaoRecrutamentoRepository(db))


specific_routes = APIRouter(prefix="/operacao-recrutamento", tags=["Operação de Recrutamento"])


@specific_routes.get("", response_model=List[OperacaoRecrutamentoReadDTO])
def listar_operacoes_recrutamento(
    limit: int = Query(50, ge=1, le=100, description="Máximo de registros por página"),
    offset: int = Query(0, ge=0, description="Número de registros a pular"),
    service: OperacaoRecrutamentoService = Depends(get_operacao_recrutamento_service),
):
    """
    Regras aplicadas:
    somente operações do tipo 'Ampliação de recursos operacionais'
            com recurso tipo 'Agente não-orgânico'.
    campo `pode_editar` = False quando há caso vinculado.
    campo `encarregado_cif` traz apenas o CIF do titular ativo.
    """
    return service.listar(limit=limit, offset=offset)

router = APIRouter()
router.include_router(specific_routes)