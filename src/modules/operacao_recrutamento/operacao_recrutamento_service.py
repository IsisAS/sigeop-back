from src.modules.operacao_recrutamento.operacao_recrutamento_repository import (OperacaoRecrutamentoRepository,)
from src.modules.operacao_recrutamento.operacao_recrutamento_schema import (OperacaoRecrutamentoReadDTO,)


class OperacaoRecrutamentoService:

    def __init__(self, repository: OperacaoRecrutamentoRepository) -> None:
        self.repository = repository

    def listar(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[OperacaoRecrutamentoReadDTO]:
        rows = self.repository.listar(limit=limit, offset=offset)
        return [OperacaoRecrutamentoReadDTO.model_validate(row) for row in rows]

