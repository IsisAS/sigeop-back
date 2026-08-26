from src.common.service import AbstractService
from src.modules.pais.pais_model import PaisModel
from src.modules.pais.pais_repository import PaisRepository
from src.modules.pais.pais_schema import PaisCreateDTO, PaisReadDTO, PaisUpdateDTO
from src.core.errors.errors import NotFoundError

class PaisService(AbstractService[PaisModel, PaisCreateDTO, PaisReadDTO, PaisUpdateDTO]):
    read_dto = PaisReadDTO

    def __init__(
        self, 
        repository: PaisRepository,
        ):
        self.repository = repository