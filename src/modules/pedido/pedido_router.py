from fastapi import Depends, Body, status
from sqlalchemy.orm import Session
from typing import List
from src.common.router import CrudRouter
from src.cache.redis import CacheService
from src.core.deps import get_db, get_cache
from src.integrations.ciclo.ciclo_client import CicloClient
from src.modules.ciclo.ciclo_service import CicloService
from src.modules.pedido.pedido_repository import PedidoRepository
from src.modules.pedido.pedido_schema import PedidoCreateDTO, PedidoReadDTO, PedidoUpdateDTO, PedidoElegivelDTO
from src.modules.pedido.pedido_service import PedidoService
# from src.app_auth import APP_PERMISSIONS
# from src.core.auth.authorization import crud_permission_dependencies
from fastapi import APIRouter, Query
from src.modules.pedido.pedido_schema import JustificacaoExclusaoDTO

def get_pedido_service(db: Session = Depends(get_db), cache: CacheService = Depends(get_cache)) -> PedidoService:
    ciclo_service = CicloService(client=CicloClient(), cache=cache)
    return PedidoService(PedidoRepository(db), ciclo_service)


specific_routes = APIRouter(prefix="/pedido", tags=["Pedido"])

@specific_routes.get("/elegiveis-para-caso", response_model=List[PedidoElegivelDTO])
def get_pedidos_elegiveis_para_caso(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    cod_caso: int | None = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna pedidos elegíveis para associação a um caso.
    
    Critérios de elegibilidade:
    - Pedidos que NÃO têm Caso já associado
    - Com vigência DIFERENTE do ano atual (vigência diferente ano_corrente)
    - E fora da vigência (vigência < ano_corrente)
    - Status = "Aberto"
    
    Retorna em formato: "Nº SEI / Ano / Unidade Análise – Assunto"
    Ordenado por número SEI
    """
    service = get_pedido_service(db)
    return service.get_pedidos_elegiveis_para_caso(
        limit=limit,
        offset=offset,
        cod_caso=cod_caso,
    )


@specific_routes.get("/complementares/{cod_pedido_original}", response_model=List[PedidoReadDTO])
def get_pedidos_complementares(
    cod_pedido_original: int,
    db: Session = Depends(get_db)
):
    """Retorna todos os pedidos complementares (filhos) vinculados ao ID original fornecido"""
    service = get_pedido_service(db)
    return service.get_complementares(cod_pedido_original)

@specific_routes.patch("/{cod_pedido}/excluir", status_code=204)
def patch_soft_delete(
    cod_pedido: int,
    payload: JustificacaoExclusaoDTO = Body(...),
    db: Session = Depends(get_db),
):
    """Executa exclusão lógica do pedido gravando justificativa."""
    service = get_pedido_service(db)
    service.soft_delete(cod_pedido=cod_pedido, justificativa=payload.dsc_justificativa_exclusao, cif_usuario_alt=payload.cif_usuario_alt)
    return None

@specific_routes.get("/{cod_pedido}/vinculos")
def verificar_vinculos(
    cod_pedido: int,
    db: Session = Depends(get_db),):
    """Retorna os vínculos de pedido"""
    service = get_pedido_service(db)
    return service.verificar_vinculos(cod_pedido)

crud = CrudRouter(
    prefix="/pedido",
    tags=["Pedido"],
    create_dto=PedidoCreateDTO,
    update_dto=PedidoUpdateDTO,
    read_dto= PedidoReadDTO,
    get_service=get_pedido_service,
    id_param="cod_pedido",
    id_description="ID do pedido",
    operations={"list", "get", "create", "update"},
    # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.pedido),
)

router = APIRouter()
router.include_router(specific_routes)
router.include_router(crud.router)