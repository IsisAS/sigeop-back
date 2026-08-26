from pydantic import Field, BaseModel
from datetime import  date, datetime
from typing import Optional

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class OperacaoDto:
    sig_operacao_tipo: str
    dsc_operacao_tipo: str 
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class OperacaoTipoCreateDTO(OperacaoDto, CreateSchema):
    pass

class OperacaoTipoUpdateDTO(OperacaoDto, UpdateSchema):
    pass

class OperacaoTipoReadDTO(OperacaoDto, ReadSchema):
    cod_operacao_tipo: int
    pass