from fastapi import Depends, Response, status
from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.core.deps import get_db
from src.modules.missao.missao_encarregado.missao_encarregado_repository import MissaoEncarregadoRepository 
from src.modules.missao.missao_fonte_humana.missao_fonte_humana_repository import MissaoFonteHumanaRepository
from src.modules.missao.missao_repository import MissaoRepository
from src.modules.missao.missao_schema import MissaoCreateDTO, MissaoDeleteDTO, MissaoReadDTO, MissaoUpdateDTO
from src.modules.missao.missao_service import MissaoService


def get_missao_service(db: Session = Depends(get_db)) -> MissaoService:
    return MissaoService(MissaoRepository(db))


crud = CrudRouter(
    prefix="/missao",
    tags=["Missão"],
    create_dto=MissaoCreateDTO,
    update_dto=MissaoUpdateDTO,
    read_dto=MissaoReadDTO,
    get_service=get_missao_service,
    id_param="cod_missao",
    id_description="ID da missão",
    operations={"create", "list", "get", "update"}
)

router = crud.router

@router.get("/por-caso/{cod_caso}", response_model=list[MissaoReadDTO])
def list_por_caso(
    cod_caso: int,
    service: MissaoService = Depends(get_missao_service),
):
    return service.list_por_caso(cod_caso=cod_caso)

@router.get("/por-tipo/{cod_missao_tipo}", response_model=list[MissaoReadDTO])
def list_por_tipo(
    cod_missao_tipo: int,
    cod_recurso_tipo: int | None = None,
    limit: int = 50,
    offset: int = 0,
    service: MissaoService = Depends(get_missao_service),
):
    return service.list_por_tipo(
        cod_missao_tipo=cod_missao_tipo,
        cod_recurso_tipo=cod_recurso_tipo,
        limit=limit,
        offset=offset,
    )


@router.patch("/exclusao/{cod_missao}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_missao(
    cod_missao: int,
    payload: MissaoDeleteDTO,
    service: MissaoService = Depends(get_missao_service),
) -> Response:
    service.soft_delete(
        cod_missao,
        justificativa=payload.justificativa,
        cif_usuario_alt=payload.cif_usuario_alt,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
