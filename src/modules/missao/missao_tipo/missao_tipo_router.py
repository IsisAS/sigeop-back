from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.core.deps import get_db
from src.modules.missao.missao_tipo.missao_tipo_repository import MissaoTipoRepository
from src.modules.missao.missao_tipo.missao_tipo_schema import MissaoTipoCreateDTO, MissaoTipoReadDTO, MissaoTipoUpdateDTO
from src.modules.missao.missao_tipo.missao_tipo_service import MissaoTipoService
from fastapi import Depends
# from src.app_auth import APP_PERMISSIONS
# from src.core.auth.authorization import crud_permission_dependencies

def get_missao_tipo_service(db: Session = Depends(get_db)) -> MissaoTipoService:
    return MissaoTipoService(MissaoTipoRepository(db))


crud = CrudRouter(
    prefix="/missao/tipo",
    tags=["Missão Tipo"],
    create_dto=MissaoTipoCreateDTO,
    update_dto=MissaoTipoUpdateDTO,
    read_dto=MissaoTipoReadDTO,
    get_service=get_missao_tipo_service,
    id_param="cod_missao_tipo",
    id_description="ID do tipo de missão",
    operations={"list"},
    # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.missao),
)

router = crud.router
