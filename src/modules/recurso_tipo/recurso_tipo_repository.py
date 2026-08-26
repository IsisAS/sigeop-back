from sqlalchemy.orm import Session
from typing import Any
from sqlalchemy import MetaData, Table, select
from src.common.repository import AbstractRepository
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel
from src.modules.recurso_tipo.recurso_tipo_schema import RecursoTipoCreateDTO, RecursoTipoUpdateDTO


class RecursoTipoRepository(AbstractRepository[RecursoTipoModel, RecursoTipoCreateDTO, RecursoTipoUpdateDTO]):
    model = RecursoTipoModel  
