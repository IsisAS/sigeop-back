from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class CasoStatusCreateDTO(CreateSchema):
    sig_caso_status: int | None = None
    dsc_caso_status: str
    flg_ativo: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    
class CasoStatusUpdateDTO(UpdateSchema):
    sig_caso_status: int | None = None
    dsc_caso_status: str
    flg_ativo: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0

class CasoStatusReadDTO(ReadSchema):
    cod_caso_status: int 
    dsc_caso_status: str
    sig_caso_status: str
    flg_ativo: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
