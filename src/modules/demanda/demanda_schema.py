from datetime import datetime
from pydantic import Field
from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema
from src.modules.demanda.demanda_model import DemandaModel
from src.modules.demanda.demanda_local.demanda_local_schema import DemandaLocalReadDTO

class DemandaDto:
    cod_operacao: int | None = None
    cod_tipo_evento_demanda: int
    dsc_responsavel: str
    dsc_atividade: str
    dat_inicio_evento: datetime
    dat_fim_evento: datetime | None = None
    flg_reg_excluido: bool = False
    dsc_justificativa_exclusao: str | None = None
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None


class DemandaCreateDTO(CreateSchema, DemandaDto):
    local: list[DemandaLocalReadDTO] = Field(default_factory=list)
    pass

class DemandaUpdateDTO(UpdateSchema, DemandaDto):
    cod_demanda: int = 0
    local: list[DemandaLocalReadDTO] = Field(default_factory=list)
    pass

class DemandaDeleteDTO(CreateSchema):
    dsc_justificativa_exclusao: str = Field(..., min_length=1, max_length=1000)

class DemandaReadDTO(ReadSchema, DemandaDto):
    cod_demanda: int = 0
    dsc_tipo_evento: str | None = None
    local: list[DemandaLocalReadDTO]

    @classmethod
    def from_model(cls, model: DemandaModel):
        tipo_evento_model = model.tipo_evento

        return cls(
            cod_demanda=model.cod_demanda,
            cod_operacao=model.cod_operacao,
            cod_tipo_evento_demanda=model.cod_tipo_evento_demanda,
            dsc_responsavel=model.dsc_responsavel,
            dsc_atividade=model.dsc_atividade,
            dat_inicio_evento=model.dat_inicio_evento,
            dat_fim_evento=model.dat_fim_evento,
            flg_reg_excluido=model.flg_reg_excluido,
            dsc_justificativa_exclusao=model.dsc_justificativa_exclusao,
            cif_usuario_inc=model.cif_usuario_inc,
            cif_usuario_alt=model.cif_usuario_alt,
            dat_hor_inclusao=model.dat_hor_inclusao,
            dat_hor_alteracao=model.dat_hor_alteracao,
            dsc_tipo_evento=tipo_evento_model.dsc_evento_tipo,
            local = model.demanda_local
        )
