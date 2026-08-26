from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema

class CasoEncarregadoUpdateDTO(UpdateSchema):
    cod_caso_encarregado: int | None = None 
    cod_caso: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0

class CasoEncarregadoCreateDTO(CreateSchema):
    cod_caso: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0

    @classmethod
    def from_update_dto(cls, updateDto: CasoEncarregadoUpdateDTO):
        return cls(
          cod_caso=updateDto.cod_caso,
          cod_agente=updateDto.cod_agente,
          flg_titular=updateDto.flg_titular,
          dat_inicio=updateDto.dat_inicio,
          flg_reg_excluido=updateDto.flg_reg_excluido,
          cif_usuario_inc=updateDto.cif_usuario_inc,
          cif_usuario_alt=updateDto.cif_usuario_alt
        )

class CasoEncarregadoReadDTO(ReadSchema):
    cod_caso_encarregado: int 
    cod_caso: int
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
