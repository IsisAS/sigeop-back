from fastapi import APIRouter, Depends, Path, Query
from src.cache.redis import CacheService
from src.core.deps import get_cache
from src.integrations.ciclo.ciclo_client import CicloClient
from src.modules.ciclo.ciclo_service import CicloService

router = APIRouter(prefix="/ciclo", tags=["Ciclo"])


def get_ciclo_service(cache: CacheService = Depends(get_cache)) -> CicloService:
    return CicloService(client=CicloClient(), cache=cache)


# ---------- Unidades ----------
@router.post("/sync/unidades")
def sync_unidades(service: CicloService = Depends(get_ciclo_service)):
    data = service.sync_unidades()
    return {"status": "synced", "data": data}

@router.get("/unidades_analise")
def get_unidades_analise(
    codigo: int | None = Query(None, description="Código da unidade"),
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_unidades(codigo=codigo)

@router.get("/superintendencia")
def get_superintendencias(
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_superintendencias()

@router.get("/unidades_destinatarias")
def get_unidades_destinatarias(
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_unidades_destinatarias()

@router.get("/unidades_ppi")
def get_unidades_ppi(
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_unidades_ppi()

@router.get("/unidades")
def get_unidades_by_codigo(
    codigo: int | None = Query(None, description="Código da unidade"),
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_unidades(codigo=codigo)

@router.get("/unidade/hierarquia")
def get_unidade_hierarquia_by_codigo(
    codigo: int | None = Query(None, description="Código da unidade"),
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_unidade_hierarquia(codigo=codigo)


# ---------- Servidores ----------
@router.post("/sync/servidores")
def sync_servidores(service: CicloService = Depends(get_ciclo_service)):
    data = service.sync_servidores()
    return {"status": "synced", "data": data}


@router.get("/servidores/unidade/{codigo}")
def get_servidores_by_unidade(
    codigo: int = Path(..., description="Código da unidade"),
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_servidores_by_unidade(codigo)

@router.get("/servidor/{cod_agente}")
def get_servidores_by_unidade(
    cod_agente: int = Path(..., description="Código do agente"),
    service: CicloService = Depends(get_ciclo_service),
):
    return service.get_servidor_by_cif(cod_agente)