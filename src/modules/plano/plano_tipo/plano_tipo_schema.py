from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class PlanoTipoDto:
    cod_plano_tipo: int 
    sig_plano_tipo: str
    dsc_plano_tipo: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class PlanoTipoReadDTO(PlanoTipoDto, ReadSchema):
    pass

class PlanoTipoUpdateDTO(PlanoTipoDto, UpdateSchema):
    pass

class PlanoTipoCreateDTO(PlanoTipoDto, CreateSchema):
    pass