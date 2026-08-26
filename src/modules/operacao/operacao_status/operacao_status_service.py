from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.operacao.operacao_status.operacao_status_model import OperacaoStatusModel
from src.modules.operacao.operacao_status.operacao_status_repository import OperacaoStatusRepository
from src.modules.operacao.operacao_status.operacao_status_schema import OperacaoStatusCreateDTO, OperacaoStatusReadDTO, OperacaoStatusUpdateDTO


class OperacaoStatusService(AbstractService[OperacaoStatusModel, OperacaoStatusCreateDTO, OperacaoStatusReadDTO, OperacaoStatusUpdateDTO]):
    read_dto = OperacaoStatusReadDTO

    def __init__(self, repo: OperacaoStatusRepository):
        self.repository = repo