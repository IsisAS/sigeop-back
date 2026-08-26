from pydantic import Field, BaseModel
from datetime import datetime
from typing import Optional
from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema


class MissaoTipoCreateDTO(CreateSchema):
    sig_missao_tipo: str
    dsc_missao_tipo: str
    flg_ativo: bool = True
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0


class MissaoTipoUpdateDTO(UpdateSchema):
    sig_missao_tipo: str
    dsc_missao_tipo: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0


class MissaoTipoReadDTO(ReadSchema):
    cod_missao_tipo: int
    sig_missao_tipo: str
    dsc_missao_tipo: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
