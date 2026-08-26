from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.core.deps import get_db
from src.modules.missao.missao_status.missao_status_repository import MissaoStatusRepository
from src.modules.missao.missao_status.missao_status_schema import MissaoStatusCreateDTO, MissaoStatusReadDTO, MissaoStatusUpdateDTO
from src.modules.missao.missao_status.missao_status_service import MissaoStatusService
from fastapi import Depends
# from src.app_auth import APP_PERMISSIONS
# from src.core.auth.authorization import crud_permission_dependencies


def get_missao_status_service(db: Session = Depends(get_db)) -> MissaoStatusService:
    return MissaoStatusService(MissaoStatusRepository(db))


crud = CrudRouter(
    prefix="/missao/status",
    tags=["Missão Status"],
    create_dto=MissaoStatusCreateDTO,
    update_dto=MissaoStatusUpdateDTO,
    read_dto=MissaoStatusReadDTO,
    get_service=get_missao_status_service,
    id_param="cod_missao_status",
    id_description="ID do status de missão",
    operations={"list"},
    # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.missao),
)

router = crud.router
