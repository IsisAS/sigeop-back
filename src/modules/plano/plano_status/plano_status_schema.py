from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class PlanoStatusDto:
    cod_plano_status: int 
    sig_plano_status: str
    dsc_plano_status: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class PlanoStatusReadDTO(PlanoStatusDto, ReadSchema):
    pass

class PlanoStatusUpdateDTO(PlanoStatusDto, UpdateSchema):
    pass

class PlanoStatusCreateDTO(PlanoStatusDto, CreateSchema):
    pass