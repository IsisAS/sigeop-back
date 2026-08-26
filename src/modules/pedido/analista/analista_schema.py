from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema


class AnalistaVinculoDTO(BaseModel):
    cod_agente: int
    flg_titular: bool = False

class AnalistaCreateDTO(CreateSchema):
    cod_pedido: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class AnalistaUpdateDTO(UpdateSchema):
    cod_pedido: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_alt: int
    dat_hor_alteracao: datetime | None = None

class AnalistaReadDTO(ReadSchema):
    cod_pedido_analista: int
    cod_pedido: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
