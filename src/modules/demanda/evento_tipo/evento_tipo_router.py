from fastapi import Depends
from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.core.deps import get_db
from src.modules.demanda.evento_tipo.evento_tipo_repository import EventoTipoRepository
from src.modules.demanda.evento_tipo.evento_tipo_schema import EventoTipoCreateDTO, EventoTipoReadDTO, EventoTipoUpdateDTO
from src.modules.demanda.evento_tipo.evento_tipo_service import EventoTipoService
# from src.app_auth import APP_PERMISSIONS
# from src.core.auth.authorization import crud_permission_dependencies

def get_evento_tipo_service(db: Session = Depends(get_db)) -> EventoTipoService:
    return EventoTipoService(EventoTipoRepository(db))


crud = CrudRouter[EventoTipoCreateDTO, EventoTipoUpdateDTO, EventoTipoReadDTO, EventoTipoService](
    prefix="/evento-tipo",
    tags=["EventoTipo"],
    create_dto=EventoTipoCreateDTO,
    update_dto=EventoTipoUpdateDTO,
    read_dto=EventoTipoReadDTO,
    get_service=get_evento_tipo_service,
    id_param="cod_evento_tipo",
    id_description="ID do tipo de evento",
    operations={"list"},
    # route_dependencies=crud_permission_dependencies(APP_PERMISSIONS.evento),
)

router = crud.router
