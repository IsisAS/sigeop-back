from fastapi import Depends
from sqlalchemy.orm import Session

from src.common.router import CrudRouter
from src.core.deps import get_db 
from src.modules.papel.papel_repository import PapelRepository
from src.modules.papel.papel_schema import PapelCreateDTO, PapelReadDTO, PapelUpdateDTO 
from src.modules.papel.papel_service import PapelService 

def get_papel_service(db: Session = Depends(get_db)) -> PapelService:
    return PapelService(PapelRepository(db))

crud = CrudRouter(
    prefix="/papel",
    tags=["Papel"],
    create_dto=PapelCreateDTO,
    update_dto=PapelUpdateDTO,
    read_dto=PapelReadDTO,
    get_service=get_papel_service,
    id_param="cod_papel",
    id_description="ID do papel",
    operations={"list", "get", "create", "update"},
)

router = crud.router