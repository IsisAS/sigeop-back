from src.common.service import AbstractService
from src.core.errors.errors import ConflictError
from src.modules.caso.caso_status.caso_status_model import CasoStatusModel
from src.modules.caso.caso_status.caso_status_repository import CasoStatusRepository
from src.modules.caso.caso_status.caso_status_schema import CasoStatusCreateDTO, CasoStatusUpdateDTO, CasoStatusReadDTO

class CasoStatusService(AbstractService[CasoStatusModel, CasoStatusCreateDTO, CasoStatusReadDTO, CasoStatusUpdateDTO]):
    read_dto = CasoStatusReadDTO

    def __init__(self, repo: CasoStatusRepository):
        self.repository = repo