from pydantic import Field, BaseModel, ConfigDict
from datetime import  date, datetime
from typing import Optional
from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema
from src.modules.operacao.operacao_model import OperacaoModel
from src.modules.operacao.operacao_encarregado.operacao_encarregado_schema import OperacaoEncarregadoReadDTO

class GridMissaoDTO(ReadSchema):
    cod_missao: int
    dsc_tipo: Optional[str] = None
    dsc_recurso_tipo: Optional[str] = None
    dsc_status: Optional[str] = None
    cif_encarregado: Optional[str] = None

class GridPlanoDTO(ReadSchema):
    cod_plano: int
    num_plano: str
    num_ano: int
    dsc_assunto: Optional[str] = None
    dsc_status: Optional[str] = None

class OperacaoInteligenciaProtecaoGridDTO(ReadSchema):
    cod_operacao: int
    nom_operacao: str
    cod_caso: Optional[int] = None
    nom_caso: Optional[str] = None
    encarregado_cif: Optional[int] = None
    dsc_operacao_status: Optional[str] = None

class EncarregadoDto(CreateSchema):
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int

class OperacaoDto:
    cod_operacao_tipo: int
    cod_caso: int | None = None
    cod_pedido: int | None = None
    cod_recurso_tipo: int | None = None
    nom_operacao: str
    dsc_operacao: str | None = None
    cod_operacao_status: int
    flg_reg_excluido: bool | None = None
    dsc_justificativa_exclusao: str | None = None
    cif_usuario_inc: int
    cif_usuario_alt: int
    encarregados: list[EncarregadoDto]

class OperacaoCreateDTO(OperacaoDto, CreateSchema):
    pass

class OperacaoUpdateDTO(OperacaoDto, UpdateSchema):
    cod_operacao: int | None = None
    pass

class OperacaoDeleteDTO(CreateSchema):
    dsc_justificativa_exclusao: str = Field(..., min_length=1, max_length=1000)

class OperacaoReadDTO(OperacaoDto, ReadSchema):
    cod_operacao: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
    encarregados: list[OperacaoEncarregadoReadDTO] = []
    encarregados_quantidade: int | None = None
    dsc_operacao_tipo: str | None = None
    dsc_operacao_status: str | None = None
    
    @classmethod
    def from_model(cls, model: OperacaoModel):
        tipo_operacao_model = model.tipo_operacao
        status_operacao_model = model.status_operacao
        recurso_tipo_model = model.recurso_tipo

        encarregados = [
            OperacaoEncarregadoReadDTO(
                cod_operacao_encarregado = item.cod_operacao_encarregado,
                cod_operacao = item.cod_operacao, 
                cod_agente = item.cod_agente,
                flg_titular = item.flg_titular,
                dat_inicio = item.dat_inicio,
                dat_fim = item.dat_fim,
                flg_reg_excluido = item.flg_reg_excluido,
                cif_usuario_inc = item.cif_usuario_inc,
                cif_usuario_alt = item.cif_usuario_alt,
                dat_hor_inclusao = item.dat_hor_inclusao,
                dat_hor_alteracao = item.dat_hor_alteracao,
            )

            for item in model.encarregados
            if not item.flg_reg_excluido
        ]

        quantidade = sum(
            1 for e in model.encarregados
            if not e.flg_reg_excluido
        )

        return cls (
            cod_operacao = model.cod_operacao,
            cod_operacao_tipo = model.cod_operacao_tipo,
            cod_caso = model.cod_caso,
            cod_pedido = next(
                (
                    item.cod_pedido
                    for item in getattr(model, "pedidos", [])
                    if not item.flg_reg_excluido
                ),
                None,
            ),
            cod_operacao_status = model.cod_operacao_status,
            nom_operacao = model.nom_operacao,
            dsc_operacao = model.dsc_operacao,
            flg_reg_excluido = model.flg_reg_excluido,
            dsc_justificativa_exclusao = model.dsc_justificativa_exclusao,
            cif_usuario_inc = model.cif_usuario_inc,
            cif_usuario_alt = model.cif_usuario_alt,
            dat_hor_inclusao = model.dat_hor_inclusao,
            dat_hor_alteracao = model.dat_hor_alteracao,
            dsc_operacao_tipo = tipo_operacao_model.dsc_operacao_tipo,
            dsc_operacao_status = status_operacao_model.dsc_operacao_status,
            encarregados_quantidade = quantidade,
            encarregados = encarregados
        )
