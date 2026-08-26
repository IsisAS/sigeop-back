from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.plano.plano_status.plano_status_repository import PlanoStatusRepository
from src.modules.plano.plano_status.plano_status_model import PlanoStatusModel
from src.modules.plano.plano_status.plano_status_schema import PlanoStatusUpdateDTO, PlanoStatusCreateDTO, PlanoStatusReadDTO

class PlanoStatusService(AbstractService[PlanoStatusModel, PlanoStatusCreateDTO, PlanoStatusReadDTO, PlanoStatusUpdateDTO]):
    read_dto = PlanoStatusReadDTO

    def __init__(self, repo: PlanoStatusRepository):
        self.repository = repo