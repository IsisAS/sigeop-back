from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema
from decimal import Decimal

class UfDto:
    cod_pais: int
    sig_uf: str
    nom_uf: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class UfReadDTO(UfDto, ReadSchema):
    cod_uf: int
    pass

class UfUpdateDTO(UfDto, UpdateSchema):
    pass

class UfCreateDTO(UfDto, CreateSchema):
    pass