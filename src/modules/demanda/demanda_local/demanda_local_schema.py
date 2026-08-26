from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class DemandaLocalDto:
    cod_demanda: int | None = None
    cod_pais: int | None = None
    cod_uf: int | None = None
    cod_municipio: int | None = None
    dsc_local_demanda: str | None = None
    flg_reg_excluido: bool  | None = None
    cif_usuario_inc: int = 0 
    cif_usuario_alt: int = 0 
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class DemandaLocalReadDTO(DemandaLocalDto, ReadSchema):
    cod_local_demanda: int | None = None
    pass

class DemandaLocalUpdateDTO(DemandaLocalDto, UpdateSchema):
    pass

class DemandaLocalCreateDTO(DemandaLocalDto, CreateSchema):
    pass