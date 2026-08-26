from typing import Any
from src.common.repository import AbstractRepository
from src.modules.operacao.operacao_encarregado.operacao_encarregado_model import OperacaoEncarregadoModel
from src.modules.operacao.operacao_encarregado.operacao_encarregado_schema import OperacaoEncarregadoCreateDTO, OperacaoEncarregadoUpdateDTO

class OperacaoEncarregadoRepository(AbstractRepository[OperacaoEncarregadoModel, OperacaoEncarregadoCreateDTO, OperacaoEncarregadoUpdateDTO]):
    model = OperacaoEncarregadoModel  

    def create(self, operacao_encarregados_data: list[dict]) -> list[OperacaoEncarregadoModel]:
        models = []
        for data in operacao_encarregados_data:
            obj = self.model(**data)
            models.append(obj)
        
        return operacao_encarregados_model

    def create(self, operacao_encarregados_data: list[OperacaoEncarregadoModel]) -> list[model]:
        models = []
        for data in operacao_encarregados_data:
            obj = self.model(**data)
            models.append(obj)

        self.db.add_all(models)
        return models
    

