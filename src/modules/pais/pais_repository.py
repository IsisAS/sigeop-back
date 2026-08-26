from src.common.repository import AbstractRepository
from src.modules.pais.pais_model import PaisModel
from src.modules.pais.pais_schema import PaisUpdateDTO, PaisCreateDTO

class PaisRepository(AbstractRepository[PaisModel, PaisCreateDTO, PaisUpdateDTO]):
    model = PaisModel

