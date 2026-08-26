from src.common.service import AbstractService
from src.modules.fonte_humana.fonte_humana_model import FonteHumanaModel
from src.modules.fonte_humana.fonte_humana_repository import FonteHumanaRepository
from src.modules.fonte_humana.fonte_humana_schema import (
    FonteHumanaCreateDTO,
    FonteHumanaReadDTO,
    FonteHumanaUpdateDTO,
)


class FonteHumanaService(
    AbstractService[FonteHumanaModel, FonteHumanaCreateDTO, FonteHumanaUpdateDTO, FonteHumanaReadDTO]
):
    read_dto = FonteHumanaReadDTO

    def __init__(self, repository: FonteHumanaRepository):
        self.repository = repository
