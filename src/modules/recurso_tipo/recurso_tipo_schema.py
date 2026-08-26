from pydantic import Field, BaseModel
from datetime import  date, datetime
from typing import Optional

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class RecursoTipoDto:
    sig_recurso_tipo: str
    dsc_recurso_tipo: str 
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class RecursoTipoCreateDTO(RecursoTipoDto, CreateSchema):
    pass

class RecursoTipoUpdateDTO(RecursoTipoDto, UpdateSchema):
    pass

class RecursoTipoReadDTO(RecursoTipoDto, ReadSchema):
    cod_recurso_tipo: int
    pass