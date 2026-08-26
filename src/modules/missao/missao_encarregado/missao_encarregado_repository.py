from sqlalchemy import delete, select 

from src.common.repository import AbstractRepository
from src.modules.missao.missao_encarregado.missao_encarregado_model import MissaoEncarregadoModel
from src.modules.missao.missao_encarregado.missao_encarregado_schema import (
    MissaoEncarregadoCreateDTO,
    MissaoEncarregadoUpdateDTO,
)

class MissaoEncarregadoRepository(AbstractRepository[MissaoEncarregadoModel, MissaoEncarregadoCreateDTO, MissaoEncarregadoUpdateDTO]):
    model = MissaoEncarregadoModel