from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.pedido.analista.analista_model import AnalistaModel
from src.modules.pedido.analista.analista_repository import AnalistaRepository
from src.modules.pedido.analista.analista_schema import AnalistaCreateDTO, AnalistaReadDTO, AnalistaUpdateDTO


class AnalistaService(AbstractService[AnalistaModel, AnalistaCreateDTO, AnalistaReadDTO, AnalistaUpdateDTO]):
    read_dto = AnalistaReadDTO

    def __init__(self, repo: AnalistaRepository):
        self.repository = repo