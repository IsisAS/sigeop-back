from src.common.service import AbstractService
from src.modules.missao.missao_status.missao_status_model import MissaoStatusModel
from src.modules.missao.missao_status.missao_status_repository import MissaoStatusRepository
from src.modules.missao.missao_status.missao_status_schema import MissaoStatusCreateDTO, MissaoStatusReadDTO, MissaoStatusUpdateDTO


class MissaoStatusService(AbstractService[MissaoStatusModel, MissaoStatusCreateDTO, MissaoStatusReadDTO, MissaoStatusUpdateDTO]):
    read_dto = MissaoStatusReadDTO

    def __init__(self, repo: MissaoStatusRepository):
        self.repository = repo
