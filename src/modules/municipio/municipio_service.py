from typing import List
from src.common.service import AbstractService
from src.modules.municipio.municipio_model import MunicipioModel
from src.modules.municipio.municipio_repository import MunicipioRepository
from src.modules.municipio.municipio_schema import MunicipioCreateDTO, MunicipioReadDTO, MunicipioUpdateDTO
from src.core.errors.errors import NotFoundError

class MunicipioService(AbstractService[MunicipioModel, MunicipioCreateDTO, MunicipioReadDTO, MunicipioUpdateDTO]):
    read_dto = MunicipioReadDTO

    def __init__(
        self, 
        repository: MunicipioRepository,
        ):
        self.repository = repository

    def get_by_uf_id(self, cod_uf: int, *, limit: int = 50, offset: int = 0) -> List[MunicipioReadDTO]:
        municipio_model_list = self.repository.get_by_uf_id(
            cod_uf=cod_uf,
            limit=limit,
            offset=offset
        )
        return [self.read_dto.model_validate(item) for item in municipio_model_list]