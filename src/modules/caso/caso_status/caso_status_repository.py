from src.common.repository import AbstractRepository
from src.modules.caso.caso_status.caso_status_model import CasoStatusModel
from src.modules.caso.caso_status.caso_status_schema import CasoStatusCreateDTO, CasoStatusUpdateDTO

class CasoStatusRepository(AbstractRepository[CasoStatusModel, CasoStatusCreateDTO, CasoStatusUpdateDTO]):
    model = CasoStatusModel
