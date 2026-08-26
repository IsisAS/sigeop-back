from typing import Sequence

from src.common.repository import AbstractRepository
from src.modules.fonte_humana.fonte_humana_model import FonteHumanaModel
from src.modules.fonte_humana.fonte_humana_schema import (
    FonteHumanaCreateDTO,
    FonteHumanaUpdateDTO,
)

class FonteHumanaRepository(AbstractRepository[FonteHumanaModel, FonteHumanaCreateDTO, FonteHumanaUpdateDTO]):
    model = FonteHumanaModel