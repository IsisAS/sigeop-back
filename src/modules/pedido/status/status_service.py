from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.pedido.status.status_model import StatusModel
from src.modules.pedido.status.status_repository import StatusRepository
from src.modules.pedido.status.status_schema import StatusCreateDTO, StatusReadDTO, StatusUpdateDTO


class StatusService(AbstractService[StatusModel, StatusCreateDTO, StatusReadDTO, StatusUpdateDTO]):
    read_dto = StatusReadDTO

    def __init__(self, repo: StatusRepository):
        self.repository = repo