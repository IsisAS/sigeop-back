from src.common.repository import AbstractRepository
from src.modules.pedido.status.status_model import StatusModel
from src.modules.pedido.status.status_schema import StatusCreateDTO, StatusUpdateDTO


class StatusRepository(AbstractRepository[StatusModel, StatusCreateDTO, StatusUpdateDTO]):
    model = StatusModel
