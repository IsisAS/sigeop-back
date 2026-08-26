from sqlalchemy.orm import Session
from typing import Any
from src.common.repository import AbstractRepository
from src.modules.missao.missao_tipo.missao_tipo_model import MissaoTipoModel
from src.modules.missao.missao_tipo.missao_tipo_schema import MissaoTipoCreateDTO, MissaoTipoUpdateDTO


class MissaoTipoRepository(AbstractRepository[MissaoTipoModel, MissaoTipoCreateDTO, MissaoTipoUpdateDTO]):
    model = MissaoTipoModel
