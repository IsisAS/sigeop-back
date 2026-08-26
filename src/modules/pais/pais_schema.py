from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema
from decimal import Decimal

class PaisDto:
    sig_pais: str
    nom_pais: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class PaisReadDTO(PaisDto, ReadSchema):
    cod_pais: int
    pass

class PaisUpdateDTO(PaisDto, UpdateSchema):
    pass

class PaisCreateDTO(PaisDto, CreateSchema):
    pass