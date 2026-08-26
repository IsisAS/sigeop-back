from datetime import datetime

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class PapelCreateDTO(CreateSchema):
    dsc_papel: str
    flg_ativo: bool = True
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0

class PapelUpdateDTO(UpdateSchema):
    dsc_papel: str
    flg_ativo: bool
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    
class PapelReadDTO(ReadSchema):
    cod_papel: int
    dsc_papel: str
    flg_ativo: bool
    flg_reg_excluido: bool
    status: str
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None