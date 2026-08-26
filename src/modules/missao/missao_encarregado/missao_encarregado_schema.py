from datetime import datetime

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class MissaoEncarregadoCreateDTO(CreateSchema):
    cod_missao: int
    cod_agente: int
    flg_titular: bool
    tip_papel: str | None = None
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    

class MissaoEncarregadoUpdateDTO(UpdateSchema):
    cod_missao_encarregado: int | None = None
    cod_missao: int
    cod_agente: int
    flg_titular: bool
    tip_papel: str | None = None
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    
class MissaoEncarregadoReadDTO(ReadSchema):
    cod_missao_encarregado: int 
    cod_missao: int
    cod_agente: int
    flg_titular: bool
    tip_papel: str
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None