from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class PlanoLocalDto:
    cod_plano: int | None = None
    cod_pais: int
    cod_uf: int | None = None
    cod_municipio: int | None = None
    dsc_local: str | None = None
    flg_reg_excluido: bool  | None = None
    cif_usuario_inc: int = 0 
    cif_usuario_alt: int = 0 
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class PlanoLocalReadDTO(PlanoLocalDto, ReadSchema):
    cod_plano_local: int | None = None
    pass

class PlanoLocalUpdateDTO(PlanoLocalDto, UpdateSchema):
    pass

class PlanoLocalCreateDTO(PlanoLocalDto, CreateSchema):
    pass