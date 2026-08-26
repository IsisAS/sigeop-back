from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class PlanoEquipeDto:
    cod_plano_equipe: int | None = None
    cod_plano: int | None = None
    cod_agente: int
    cod_papel: int
    flg_reg_excluido: bool  | None = None
    cif_usuario_inc: int = 0 
    cif_usuario_alt: int = 0 
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class PlanoEquipeReadDTO(PlanoEquipeDto, ReadSchema):
    pass

class PlanoEquipeUpdateDTO(PlanoEquipeDto, UpdateSchema):
    pass

class PlanoEquipeCreateDTO(PlanoEquipeDto, CreateSchema):
    pass