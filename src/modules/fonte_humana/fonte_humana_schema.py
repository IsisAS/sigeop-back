from datetime import datetime

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class FonteHumanaCreateDTO(CreateSchema):
    sig_fonte_humana: str
    cod_agente_controlador: int
    cod_agente_controlador_substituto: int | None = None
    flg_ativo: bool = True
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    
    
class FonteHumanaUpdateDTO(UpdateSchema):
    sig_fonte_humana: str
    cod_agente_controlador: int
    cod_agente_controlador_substituto: int | None = None
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    
class FonteHumanaReadDTO(ReadSchema):
    cod_fonte_humana: int
    sig_fonte_humana: str
    cod_agente_controlador: int
    cod_agente_controlador_substituto: int | None = None
    flg_ativo: bool
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None