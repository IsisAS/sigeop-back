from fastapi import APIRouter

from fastapi import APIRouter

from src.modules.health.health_router import router as health_router
from src.modules.pedido.status.status_router import router as status_router
from src.modules.pedido.pedido_router import router as pedido_router
from src.modules.ciclo.ciclo_router import router as ciclo_router
from src.modules.pedido.analista.analista_router import router as analista_router
from src.modules.caso.caso_status.caso_status_router import router as caso_status_router
from src.modules.caso.caso.caso_router import router as caso_router
from src.modules.operacao.operacao_tipo.operacao_tipo_router import router as operacao_tipo_router
from src.modules.operacao.operacao_status.operacao_status_router import router as operacao_status_router
from src.modules.operacao.operacao_router import router as operacao_router
from src.modules.missao.missao_router import router as missao_router
from src.modules.missao.missao_tipo.missao_tipo_router import router as missao_tipo_router
from src.modules.missao.missao_status.missao_status_router import router as missao_status_router
from src.modules.recurso_tipo.recurso_tipo_router import router as recurso_tipo_router
from src.modules.fonte_humana.fonte_humana_router import router as fonte_humana_router
from src.modules.papel.papel_router import router as papel_router
from src.modules.ppi.ppi_router import router as ppi_router
from src.modules.plano.plano_tipo.plano_tipo_router import router as plano_tipo_router
from src.modules.plano.plano_status.plano_status_router import router as plano_status_router
from src.modules.plano.plano_router import router as plano_router
from src.modules.plano.plano_missao.plano_missao_router import router as plano_missao_router
from src.modules.plano.plano_operacao.plano_operacao_router import router as plano_operacao_router
from src.modules.plano.plano_local.plano_local_router import router as plano_local_router
from src.modules.ciclo.ciclo_router import router as ciclo_router
from src.modules.uf.uf_router import router as uf_router
from src.modules.municipio.municipio_router import router as municipio_router
from src.modules.pais.pais_router import router as pais_router
from src.modules.ppi.ppi_router import router as ppi_router
from src.modules.recurso_tipo.recurso_tipo_router import router as recurso_tipo_router
from src.modules.demanda.demanda_router import router as demanda_router
from src.modules.demanda.evento_tipo.evento_tipo_router import router as evento_tipo_router
from src.modules.operacao_recrutamento.operacao_recrutamento_router import router as operacao_recrutamento_router
from src.modules.plano.plano_caso.plano_caso_router import router as plano_caso_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(status_router)
api_router.include_router(pedido_router)
api_router.include_router(analista_router)
api_router.include_router(ciclo_router)
api_router.include_router(caso_status_router)
api_router.include_router(caso_router)
api_router.include_router(operacao_tipo_router)
api_router.include_router(operacao_status_router)
api_router.include_router(operacao_router)
api_router.include_router(missao_tipo_router)
api_router.include_router(missao_status_router)
api_router.include_router(recurso_tipo_router)
api_router.include_router(missao_router)
api_router.include_router(fonte_humana_router)
api_router.include_router(papel_router)
api_router.include_router(ppi_router)
api_router.include_router(ciclo_router)
api_router.include_router(plano_tipo_router)
api_router.include_router(plano_status_router)
api_router.include_router(pais_router)
api_router.include_router(municipio_router)
api_router.include_router(uf_router)
api_router.include_router(plano_router)
api_router.include_router(demanda_router)
api_router.include_router(plano_operacao_router)
api_router.include_router(plano_local_router)
api_router.include_router(plano_missao_router)
api_router.include_router(evento_tipo_router)
api_router.include_router(operacao_recrutamento_router)
api_router.include_router(plano_caso_router)
