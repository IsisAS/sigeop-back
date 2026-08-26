from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.modules.pais.pais_schema import PaisReadDTO, PaisUpdateDTO, PaisCreateDTO
from src.modules.pais.pais_repository import PaisRepository
from src.modules.pais.pais_service import PaisService

def get_pais_service(db: Session) -> PaisService:
    return PaisService(
        PaisRepository(db),
    )

crud = CrudRouter(
    prefix="/pais",
    tags=["Pais"],
    create_dto=PaisCreateDTO,
    update_dto=PaisUpdateDTO,
    read_dto= PaisReadDTO,
    get_service=get_pais_service,
    id_param="cod_pais",
    id_description="ID do pais",
    operations={'list', 'get', 'create'}
)

router = crud.router
