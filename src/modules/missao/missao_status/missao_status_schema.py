from pydantic import Field, BaseModel
from datetime import datetime
from typing import Optional
from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema


class MissaoStatusCreateDTO(CreateSchema):
    sig_missao_status: str
    dsc_missao_status: str
    flg_ativo: bool = True
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0


class MissaoStatusUpdateDTO(UpdateSchema):
    sig_missao_status: str
    dsc_missao_status: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0


class MissaoStatusReadDTO(ReadSchema):
    cod_missao_status: int
    sig_missao_status: str
    dsc_missao_status: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
