from src.common.service import AbstractService
from src.modules.missao.missao_tipo.missao_tipo_model import MissaoTipoModel
from src.modules.missao.missao_tipo.missao_tipo_repository import MissaoTipoRepository
from src.modules.missao.missao_tipo.missao_tipo_schema import MissaoTipoCreateDTO, MissaoTipoReadDTO, MissaoTipoUpdateDTO


class MissaoTipoService(AbstractService[MissaoTipoModel, MissaoTipoCreateDTO, MissaoTipoReadDTO, MissaoTipoUpdateDTO]):
    read_dto = MissaoTipoReadDTO

    def __init__(self, repo: MissaoTipoRepository):
        self.repository = repo
