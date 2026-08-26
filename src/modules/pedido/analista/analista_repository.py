from sqlalchemy import select, delete
from typing import Any

from src.common.repository import AbstractRepository
from src.modules.pedido.analista.analista_model import AnalistaModel
from src.modules.pedido.analista.analista_schema import AnalistaCreateDTO, AnalistaUpdateDTO


class AnalistaRepository(AbstractRepository[AnalistaModel, AnalistaCreateDTO, AnalistaUpdateDTO]):
    model = AnalistaModel