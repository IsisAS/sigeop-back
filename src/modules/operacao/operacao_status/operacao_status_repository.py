from sqlalchemy.orm import Session
from typing import Any
from sqlalchemy import MetaData, Table, select
from src.common.repository import AbstractRepository
from src.modules.operacao.operacao_status.operacao_status_model import OperacaoStatusModel
from src.modules.operacao.operacao_status.operacao_status_schema import OperacaoStatusCreateDTO, OperacaoStatusUpdateDTO


class OperacaoStatusRepository(AbstractRepository[OperacaoStatusModel, OperacaoStatusCreateDTO, OperacaoStatusUpdateDTO]):
    model = OperacaoStatusModel  
