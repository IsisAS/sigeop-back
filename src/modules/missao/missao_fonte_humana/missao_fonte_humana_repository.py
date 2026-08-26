from src.common.repository import AbstractRepository
from src.modules.missao.missao_fonte_humana.missao_fonte_humana_model import MissaoFonteHumanaModel
from src.modules.missao.missao_fonte_humana.missao_fonte_humana_schema import MissaoFonteHumanaCreateDTO, MissaoFonteHumanaUpdateDTO


class MissaoFonteHumanaRepository(AbstractRepository[MissaoFonteHumanaModel, MissaoFonteHumanaCreateDTO, MissaoFonteHumanaUpdateDTO]):
    model = MissaoFonteHumanaModel
