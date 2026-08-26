from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from typing import List

from src.core.deps import get_db
from src.common.router import CrudRouter
from src.modules.caso.caso.caso_schema import CasoCreateDTO, CasoUpdateDTO, CasoReadDTO, ListarCasoDto, EncarregadoDto, GridOperacaoDTO, GridMissaoDTO, GridPlanoDTO
from src.modules.caso.caso.caso_repository import CasoRepository
from src.modules.caso.caso_status.caso_status_repository import CasoStatusRepository
from src.modules.caso.caso.caso_service import CasoService
from src.modules.caso.caso_encarregado.caso_encarregado_repository import CasoEncarregadoRepository
from src.modules.pedido.pedido_repository import PedidoRepository
from src.modules.pedido.pedido_schema import PedidoReadDTO
from src.modules.pedido.pedido_repository import PedidoRepository

def get_caso_service(db: Session) -> CasoService:
    return CasoService(
        repository=CasoRepository(db), 
        caso_encarregado_repository=CasoEncarregadoRepository(db),
        caso_status_repository=CasoStatusRepository(db),
        pedido_repository=PedidoRepository(db)
    )

crud = CrudRouter(
    prefix="/caso",
    tags=["Caso"],
    create_dto=CasoCreateDTO,
    update_dto=CasoUpdateDTO,
    read_dto= CasoReadDTO,
    get_service=get_caso_service,
    id_param="cod_caso",
    id_description="ID do caso",
    exclude={"list", "delete"}
)

router = crud.router

@router.get("/pedido-abertura/{cod_pedido_abertura}", response_model=List[CasoReadDTO])
def get_casos_by_pedido_abertura(
    cod_pedido_abertura: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retorna todos os casos relacionados a um pedido de abertura"""
    service = get_caso_service(db)
    return service.get_by_pedido_abertura(
        cod_pedido_abertura=cod_pedido_abertura,
        limit=limit,
        offset=offset
    )

@router.get("/encarregados/{cod_caso}", response_model=List[EncarregadoDto])
def get_encarregados_do_caso(
    cod_caso: int,
    db: Session = Depends(get_db)
):
    """Retorna todos os encarregados de um caso"""
    service = get_caso_service(db)
    return service.obter_encarregados_por_caso(cod_caso=cod_caso)

@router.get("/pedidos/disponiveis", response_model=List[PedidoReadDTO])
def get_pedidos_disponiveis(db: Session = Depends(get_db)):
    """Retorna todos os pedidos vigentes e abertos que não estão vinculados a nenhum caso."""
    service = get_caso_service(db)
    return service.listar_pedidos_disponiveis()

@router.get("/pedidos/{cod_caso}", response_model=List[PedidoReadDTO])
def get_pedidos_do_caso(
    cod_caso: int,
    db: Session = Depends(get_db)
):
    """Retorna todos os pedidos associados ao caso (vigentes e expirados), ordenados do mais recente para o mais antigo"""
    service = get_caso_service(db)
    return service.listar_pedidos_por_caso(cod_caso=cod_caso)

@router.get("", response_model=List[ListarCasoDto])
def get_casos(
    filtro: str | int = None,
    limit: int = 5,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Retorna todos os casos"""
    service = get_caso_service(db)
    return service.listar_casos(
        filtro=filtro,
        limit=limit,
        offset=offset
    )

@router.get("/{cod_caso}/missoes", response_model=List[GridMissaoDTO])
def get_missoes_do_caso(cod_caso: int, db: Session = Depends(get_db)):
    """Retorna as missões vinculadas ao caso para a grid."""
    service = get_caso_service(db)
    return service.listar_missoes_por_caso(cod_caso)

@router.get("/{cod_caso}/planos", response_model=List[GridPlanoDTO])
def get_planos_do_caso(cod_caso: int, db: Session = Depends(get_db)):
    """Retorna os planos vinculados ao caso para a grid."""
    service = get_caso_service(db)
    return service.listar_planos_por_caso(cod_caso)