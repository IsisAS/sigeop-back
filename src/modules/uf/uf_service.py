from typing import List
from src.common.service import AbstractService
from src.modules.uf.uf_model import UfModel
from src.modules.uf.uf_repository import UfRepository
from src.modules.uf.uf_schema import UfCreateDTO, UfReadDTO, UfUpdateDTO
from src.core.errors.errors import NotFoundError

class UfService(AbstractService[UfModel, UfCreateDTO, UfReadDTO, UfUpdateDTO]):
    read_dto = UfReadDTO

    def __init__(
        self, 
        repository: UfRepository,
        ):
        self.repository = repository

    def get_by_pais_id(self, cod_pais: int, *, limit: int = 50, offset: int = 0) -> List[UfReadDTO]:
        uf_model_list = self.repository.get_by_pais_id(
            cod_pais=cod_pais,
            limit=limit,
            offset=offset
        )
        return [self.read_dto.model_validate(item) for item in uf_model_list]