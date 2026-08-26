from pydantic import Field, BaseModel
from datetime import date, datetime
from typing import Optional

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class OperacaoEncarregadoCreateDTO(CreateSchema):
    cod_operacao: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0

class OperacaoEncarregadoUpdateDTO(UpdateSchema):
    cod_operacao: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0 
    cif_usuario_alt: int = 0

class OperacaoEncarregadoReadDTO(ReadSchema):
    cod_operacao_encarregado: int
    cod_operacao: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int | None = None
    cif_usuario_alt: int | None = None
    dat_hor_inclusao: datetime
    dat_hor_alteracao: datetime