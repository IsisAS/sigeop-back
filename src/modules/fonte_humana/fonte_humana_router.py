from sqlalchemy.orm import Session

from src.common.router import CrudRouter
from src.modules.fonte_humana.fonte_humana_repository import FonteHumanaRepository
from src.modules.fonte_humana.fonte_humana_schema import (
    FonteHumanaCreateDTO,
    FonteHumanaReadDTO,
    FonteHumanaUpdateDTO,
)
from src.modules.fonte_humana.fonte_humana_service import FonteHumanaService


def get_fonte_humana_service(db: Session) -> FonteHumanaService:
    return FonteHumanaService(FonteHumanaRepository(db))

crud = CrudRouter(
    prefix="/fonte-humana",
    tags=["Fonte Humana"],
    create_dto=FonteHumanaCreateDTO,
    update_dto=FonteHumanaUpdateDTO,
    read_dto=FonteHumanaReadDTO,
    get_service=get_fonte_humana_service,
    id_param="cod_fonte_humana",
    id_description="ID da fonte humana",
    operations={"list"}
)

router = crud.router