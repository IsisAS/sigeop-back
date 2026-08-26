from src.common.repository import AbstractRepository
from src.modules.plano.plano_tipo.plano_tipo_model import PlanoTipoModel
from src.modules.plano.plano_tipo.plano_tipo_schema import PlanoTipoUpdateDTO, PlanoTipoCreateDTO

class PlanoTipoRepository(AbstractRepository[PlanoTipoModel, PlanoTipoCreateDTO, PlanoTipoUpdateDTO]):
    model = PlanoTipoModel
