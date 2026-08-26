from sqlalchemy.orm import Session
from typing import Any
from sqlalchemy import MetaData, Table, select
from src.common.repository import AbstractRepository
from src.modules.operacao.operacao_tipo.operacao_tipo_model import OperacaoTipoModel
from src.modules.operacao.operacao_tipo.operacao_tipo_schema import OperacaoTipoCreateDTO, OperacaoTipoUpdateDTO


class OperacaoTipoRepository(AbstractRepository[OperacaoTipoModel, OperacaoTipoCreateDTO, OperacaoTipoUpdateDTO]):
    model = OperacaoTipoModel  
