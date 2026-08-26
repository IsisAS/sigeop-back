from sqlalchemy.orm import Session
from src.common.router import CrudRouter
from src.modules.operacao.operacao_status.operacao_status_repository import OperacaoStatusRepository
from src.modules.operacao.operacao_status.operacao_status_schema import OperacaoStatusCreateDTO, OperacaoStatusReadDTO, OperacaoStatusUpdateDTO
from src.modules.operacao.operacao_status.operacao_status_service import OperacaoStatusService


def get_operacao_status_service(db: Session) -> OperacaoStatusService:
    return OperacaoStatusService(OperacaoStatusRepository(db))

crud = CrudRouter(
    prefix="/operacao/status",
    tags=["Operacao Status"],
    create_dto=OperacaoStatusCreateDTO,
    update_dto=OperacaoStatusUpdateDTO,
    read_dto= OperacaoStatusReadDTO,
    get_service=get_operacao_status_service,
    id_param="cod_operacao_status",
    id_description="ID do Operacao caso",
    operations={'list'}
)

router = crud.router
