from src.common.repository import AbstractRepository
from src.modules.demanda.evento_tipo.evento_tipo_model import EventoTipoModel
from src.modules.demanda.evento_tipo.evento_tipo_schema import EventoTipoCreateDTO, EventoTipoUpdateDTO


class EventoTipoRepository(AbstractRepository[EventoTipoModel, EventoTipoCreateDTO, EventoTipoUpdateDTO]):
    model = EventoTipoModel
