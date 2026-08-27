from pydantic import Field, BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema

class AnalistaDTO(BaseModel):
    cod_agente: int
    nom_agente: str | None = None
    flg_titular: bool
    dat_inicio: datetime | None = None
    dat_fim: datetime | None = None
    flg_reg_excluido: bool = False

class UnidadeDestinatariaDTO(BaseModel):
    cod_pedido: int | None = None
    cod_unidade_destinataria: int
    sig_unidade_destinataria: str | None = None
    nom_unidade_destinataria: str | None = None
    dsc_arvore_unidade_destinataria: str | None = None

class UnidadeDestinatariaCodigoDTO(BaseModel):
    cod_unidade_destinataria: int

class PedidoCreateDTO(CreateSchema):
    cod_caso: int | None = None
    cod_casos: list[int] | None = None
    cod_ppi: int
    cod_pedido_tipo: int | None = None
    cod_pedido_original: int | None = None
    cod_pedido_relacionado: int | None = None
    cod_unidade_analise: int
    cod_unidade_elo: int | None = None
    num_pedido: str | None = Field(default=None, max_length=20)
    num_ano: int
    dat_emissao: date
    dsc_assunto: str | None = None
    dsc_tematica: str | None = None
    idn_processo: str | None = Field(default=None, max_length=40)
    dat_prazo: date
    cod_pedido_status: int | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

    analistas: Optional[list[AnalistaDTO]] = Field(default=[], description="Lista de IDs dos agentes analistas")

class PedidoComplementarCreateDTO(PedidoCreateDTO):
    cod_pedido_original: int

class PedidoUpdateDTO(UpdateSchema):
    cod_caso: int | None = None
    cod_casos: list[int] | None = None
    cod_ppi: int | None = None
    cod_pedido_tipo: int | None = None
    cod_pedido_original: int | None = None
    cod_pedido_relacionado: int | None = None
    cod_unidade_analise: int | None = None
    cod_unidade_elo: int | None = None
    num_pedido: str | None = Field(default=None, max_length=20)
    num_ano: int
    dat_emissao: date
    dsc_assunto: str | None = None
    dsc_tematica: str | None = None
    idn_processo: str | None = Field(default=None, max_length=40)
    dat_prazo: date
    cod_pedido_status: int | None = None
    flg_reg_excluido: bool
    cif_usuario_alt: int
    dat_hor_alteracao: datetime | None = None

    analistas: Optional[list[AnalistaDTO]] = Field(default=[], description="Lista de IDs dos agentes analistas")
    unidades_destinatarias: list[int] | None = None 
    
class PedidoReadDTO(ReadSchema):
    cod_pedido: int
    cod_caso: int | None = None
    cod_casos: list[int] = Field(default_factory=list)
    cod_ppi: int
    cod_pedido_tipo: int | None = None
    dsc_pedido_tipo: str | None = None
    cod_pedido_original: int | None = None
    cod_pedido_relacionado: int | None = None
    cod_unidade_analise: int
    nom_unidade_analise: str | None = None
    dsc_arvore_unidade_analise: str | None = None
    sig_unidade_analise: str | None = None
    cod_unidade_elo: int | None = None
    nom_unidade_elo: str | None = None
    sig_unidade_elo: str | None = None
    num_pedido: str = Field(max_length=20)
    num_ano: int
    dat_emissao: date
    dsc_assunto: str | None = None
    dsc_tematica: str | None = None
    idn_processo: str | None = Field(default=None, max_length=40)
    dat_prazo: date
    cod_pedido_status: int | None = None
    dsc_pedido_status: str | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

    analistas: Optional[list[AnalistaDTO]] = Field(default=[], description="Lista dos agentes analistas ativos")
    unidades_destinatarias: list[UnidadeDestinatariaDTO] = Field(
        default_factory=list, description="Lista das unidades destinatárias ativas"
    )

class PedidoElegivelDTO(BaseModel):   
    cod_pedido: int
    display_text: str = Field(description="'Formato: N° SEI / Ano / Unidade Análise - Assunto'")

class JustificacaoExclusaoDTO(UpdateSchema):
    dsc_justificativa_exclusao: str | None = None
    cif_usuario_alt: int | None = None
