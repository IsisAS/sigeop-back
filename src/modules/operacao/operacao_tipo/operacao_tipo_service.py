from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.operacao.operacao_tipo.operacao_tipo_model import OperacaoTipoModel
from src.modules.operacao.operacao_tipo.operacao_tipo_repository import OperacaoTipoRepository
from src.modules.operacao.operacao_tipo.operacao_tipo_schema import OperacaoTipoCreateDTO, OperacaoTipoReadDTO, OperacaoTipoUpdateDTO


class OperacaoTipoService(AbstractService[OperacaoTipoModel, OperacaoTipoCreateDTO, OperacaoTipoReadDTO, OperacaoTipoUpdateDTO]):
    read_dto = OperacaoTipoReadDTO

    def __init__(self, repo: OperacaoTipoRepository):
        self.repository = repo