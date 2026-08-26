from sqlalchemy.orm import Session

from src.common.router import CrudRouter
from src.modules.operacao.operacao_tipo.operacao_tipo_repository import OperacaoTipoRepository
from src.modules.operacao.operacao_tipo.operacao_tipo_schema import OperacaoTipoCreateDTO, OperacaoTipoReadDTO, OperacaoTipoUpdateDTO
from src.modules.operacao.operacao_tipo.operacao_tipo_service import OperacaoTipoService


def get_operacao_tipo_service(db: Session) -> OperacaoTipoService:
    return OperacaoTipoService(OperacaoTipoRepository(db))

crud = CrudRouter(
    prefix="/operacao/tipo",
    tags=["Operacao Tipo"],
    create_dto=OperacaoTipoCreateDTO,
    update_dto=OperacaoTipoUpdateDTO,
    read_dto= OperacaoTipoReadDTO,
    get_service=get_operacao_tipo_service,
    id_param="cod_operacao_tipo",
    id_description="ID do Operacao caso",
    operations={'list'}
)

router = crud.router
