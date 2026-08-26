from src.common.service import AbstractService
from src.modules.demanda.evento_tipo.evento_tipo_model import EventoTipoModel
from src.modules.demanda.evento_tipo.evento_tipo_repository import EventoTipoRepository
from src.modules.demanda.evento_tipo.evento_tipo_schema import (
    EventoTipoCreateDTO,
    EventoTipoReadDTO,
    EventoTipoUpdateDTO,
)

class EventoTipoService(AbstractService[EventoTipoModel, EventoTipoCreateDTO, EventoTipoReadDTO, EventoTipoUpdateDTO]):
    read_dto = EventoTipoReadDTO

    def __init__(self, repository: EventoTipoRepository):
        self.repository = repository
