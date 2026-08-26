from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema


class RelatorioDifusaoDTO(BaseModel):
    cod_unidade: int
    sig_unidade: str | None = None
    nom_unidade: str | None = None
    dsc_arvore_unidade: str | None = None


class RelatorioPedidoResumoDTO(BaseModel):
    cod_pedido: int
    num_pedido: str
    num_ano: int
    cod_unidade_analise: int
    sig_unidade_analise: str | None = None
    nom_unidade_analise: str | None = None
    sig_unidade_elo: str | None = None
    nom_unidade_elo: str | None = None
    dsc_assunto: str | None = None
    dat_prazo: date
    cod_pedido_status: int | None = None
    dsc_pedido_status: str | None = None
    display_text: str


class RelatorioTipoDTO(BaseModel):
    cod_relatorio_tipo: int
    sig_relatorio_tipo: str
    dsc_relatorio_tipo: str


class RelatorioStatusDTO(BaseModel):
    cod_relatorio_status: int
    sig_relatorio_status: str
    dsc_relatorio_status: str
    num_ordem: int


class RelatorioFields:
    cod_relatorio_tipo: int
    cod_relatorio_status: int
    cod_unidade: int
    sig_unidade: str | None = Field(default=None, max_length=50)
    nom_unidade: str | None = Field(default=None, max_length=255)
    dsc_arvore_unidade: str | None = Field(default=None, max_length=1000)
    num_relatorio: str = Field(min_length=1, max_length=20)
    num_ano: int = Field(ge=1900, le=9999)
    dat_emissao: date
    dsc_assunto: str = Field(min_length=1)
    idn_processo: str = Field(min_length=1, max_length=40)
    idn_agente_nao_organico: str | None = None
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 1
    cif_usuario_alt: int = 1

    @field_validator("num_relatorio", "dsc_assunto", "idn_processo")
    @classmethod
    def nao_aceita_texto_vazio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo não pode ser vazio.")
        return value


class RelatorioCreateDTO(CreateSchema, RelatorioFields):
    pedidos: list[int] = Field(default_factory=list)
    difusoes: list[RelatorioDifusaoDTO] = Field(min_length=1)


class RelatorioUpdateDTO(UpdateSchema, RelatorioFields):
    pedidos: list[int] = Field(default_factory=list)
    difusoes: list[RelatorioDifusaoDTO] = Field(min_length=1)


class RelatorioReadDTO(ReadSchema, RelatorioFields):
    cod_relatorio: int
    sig_relatorio_tipo: str
    dsc_relatorio_tipo: str
    sig_relatorio_status: str
    dsc_relatorio_status: str
    num_ordem_status: int
    pedidos: list[RelatorioPedidoResumoDTO] = Field(default_factory=list)
    difusoes: list[RelatorioDifusaoDTO] = Field(default_factory=list)
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
