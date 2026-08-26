from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema
from decimal import Decimal

class MunicipioDto:
    cod_uf: int
    nom_municipio: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class MunicipioReadDTO(MunicipioDto, ReadSchema):
    cod_municipio: int
    pass

class MunicipioUpdateDTO(MunicipioDto, UpdateSchema):
    pass

class MunicipioCreateDTO(MunicipioDto, CreateSchema):
    pass