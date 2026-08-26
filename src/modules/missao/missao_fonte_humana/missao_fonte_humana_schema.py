from pydantic import Field, BaseModel
from datetime import datetime
from typing import Optional
from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema


class MissaoFonteHumanaCreateDTO(CreateSchema):
    cod_missao: int
    cod_fonte_humana: int
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0


class MissaoFonteHumanaUpdateDTO(UpdateSchema):
    cod_missao: int = 0
    cod_fonte_humana: int
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0


class MissaoFonteHumanaReadDTO(ReadSchema):
    cod_missao: int
    cod_fonte_humana: int
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
