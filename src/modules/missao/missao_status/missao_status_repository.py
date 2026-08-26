from sqlalchemy.orm import Session
from typing import Any
from src.common.repository import AbstractRepository
from src.modules.missao.missao_status.missao_status_model import MissaoStatusModel
from src.modules.missao.missao_status.missao_status_schema import MissaoStatusCreateDTO, MissaoStatusUpdateDTO


class MissaoStatusRepository(AbstractRepository[MissaoStatusModel, MissaoStatusCreateDTO, MissaoStatusUpdateDTO]):
    model = MissaoStatusModel
