from pydantic import Field
from datetime import datetime
from typing import Optional

from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class StatusCreateDTO(CreateSchema):
    sig_pedido_status: str = Field(min_length=2, max_length=60)
    dsc_pedido_status: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class StatusUpdateDTO(UpdateSchema):
    sig_pedido_status: str = Field(min_length=2, max_length=60)
    dsc_pedido_status: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class StatusReadDTO(ReadSchema):
    cod_pedido_status: int
    sig_pedido_status: str
    dsc_pedido_status: str
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime
    dat_hor_alteracao: datetime
