from src.common.service import AbstractService
from src.modules.ppi.ppi_model import PPIModel
from src.modules.ppi.ppi_repository import PPIRepository
from src.modules.ppi.ppi_schema import PPICreateDTO, PPIReadDTO, PPIUpdateDTO
from src.core.errors.errors import NotFoundError

class PPIService(AbstractService[PPIModel, PPICreateDTO, PPIReadDTO, PPIUpdateDTO]):
    read_dto = PPIReadDTO

    def __init__(self, repository: PPIRepository):
        self.repository = repository

    def list(self, *, limit: int = 50, offset: int = 0) -> list[PPIReadDTO]:
        ppi_list = self.repository.list(limit = limit, offset = offset)
        return [PPIReadDTO.from_model(item) for item in ppi_list]

    def alterar_status_ppi(self, cod_ppi: str, status: bool) -> PPIReadDTO:
        ppi_model = self.repository.alterar_status_ppi(cod_ppi, status)
        
        self.repository.db.commit()
        return self.read_dto.model_validate(ppi_model)