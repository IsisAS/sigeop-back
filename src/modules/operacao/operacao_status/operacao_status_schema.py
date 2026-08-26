from pydantic import Field, BaseModel
from datetime import  date, datetime
from typing import Optional

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class OperacaoStatusDto:
    sig_operacao_status: str
    dsc_operacao_status: str 
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class OperacaoStatusCreateDTO(OperacaoStatusDto, CreateSchema):
    pass

class OperacaoStatusUpdateDTO(OperacaoStatusDto, UpdateSchema):
    pass

class OperacaoStatusReadDTO(OperacaoStatusDto, ReadSchema):
    cod_operacao_status: int
    pass