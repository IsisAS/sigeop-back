from src.common.repository import AbstractRepository
from src.modules.plano.plano_status.plano_status_model import PlanoStatusModel
from src.modules.plano.plano_status.plano_status_schema import PlanoStatusUpdateDTO, PlanoStatusCreateDTO

class PlanoStatusRepository(AbstractRepository[PlanoStatusModel, PlanoStatusCreateDTO, PlanoStatusUpdateDTO]):
    model = PlanoStatusModel
