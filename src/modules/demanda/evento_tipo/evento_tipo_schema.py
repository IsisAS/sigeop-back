from datetime import datetime
from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class EventoTipoDto:
    sig_evento_tipo: str
    dsc_evento_tipo: str
    flg_ativo: bool = True
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None


class EventoTipoCreateDTO(CreateSchema, EventoTipoDto):
    pass


class EventoTipoUpdateDTO(UpdateSchema, EventoTipoDto):
    pass


class EventoTipoReadDTO(ReadSchema, EventoTipoDto):
    cod_evento_tipo: int = 0
    pass
