import re 
from datetime import datetime
from pydantic import Field, field_validator
from src.common.schemas import CreateSchema, ReadSchema, UpdateSchema
from src.modules.missao.missao_model import MissaoModel

IDN_AGENTE_NAO_ORGANICO_PATTERN = re.compile(r"^[A-Z]\d{6}$")

def validar_idn_agente_nao_organico(value: str | None) -> str | None:
    if value is None or value == "":
        return value
    if not IDN_AGENTE_NAO_ORGANICO_PATTERN.match(value):
        raise ValueError(
            "idn_agente_nao_organico deve seguir o formato de uma letra seguido de 6 números (ex: H123456)"
        )
    return value


class MissaoEncarregadoCreateDTO(CreateSchema):
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
    cod_missao: int = 0
    cod_agente: int
    flg_titular: bool
    tip_papel: str
    dat_inicio: datetime
    dat_fim: datetime | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime
    dat_hor_alteracao: datetime


class MissaoFonteHumanaDTO(CreateSchema):
    cod_missao: int = 0
    cod_fonte_humana: int
    sig_fonte_humana: str | None = None
    descricao: str | None = None
    flg_ativo: bool = True
    flg_reg_excluido: bool = False
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0


class MissaoCreateDTO(CreateSchema):
    cod_missao_tipo: int
    cod_recurso_tipo: int | None = None
    cod_caso: int | None = None
    cod_operacao: int | None = None
    cod_pedido: int | None = None
    dsc_missao: str | None = None
    idn_agente_nao_organico: str | None = None
    cod_unidade_responsavel: int 
    sig_unidade_responsavel: str | None = None
    nom_unidade_responsavel: str | None = None
    dsc_arvore_unidade_responsavel: str | None = None
    cod_missao_status: int | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    encarregados: list[MissaoEncarregadoCreateDTO]
    fontes_humanas: list[MissaoFonteHumanaDTO] = Field(default_factory=list)

    _validar_idn_agente_nao_organico = field_validator("idn_agente_nao_organico")(
        validar_idn_agente_nao_organico
    )

class MissaoUpdateDTO(UpdateSchema):
    cod_missao_tipo: int
    cod_recurso_tipo: int | None = None
    cod_caso: int | None = None
    cod_operacao: int | None = None
    cod_pedido: int | None = None
    dsc_missao: str | None = None
    idn_agente_nao_organico: str | None = None
    cod_unidade_responsavel: int 
    sig_unidade_responsavel: str | None = None
    nom_unidade_responsavel: str | None = None
    dsc_arvore_unidade_responsavel: str | None = None
    cod_missao_status: int | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    encarregados: list[MissaoEncarregadoCreateDTO]
    fontes_humanas: list[MissaoFonteHumanaDTO] = Field(default_factory=list)
    
    _validar_idn_agente_nao_organico = field_validator("idn_agente_nao_organico")(
        validar_idn_agente_nao_organico
    )

class MissaoReadDTO(ReadSchema):
    cod_missao: int = 0
    cod_missao_tipo: int 
    cod_recurso_tipo: int | None = None
    sig_recurso_tipo: str | None = None
    dsc_recurso_tipo: str | None = None
    cod_caso: int | None
    dsc_caso: str | None
    cod_operacao: int | None 
    dsc_operacao: str | None
    cod_pedido: int | None 
    cod_unidade_elo: int | None = None
    dsc_missao: str | None
    dsc_missao_tipo: str | None = None
    idn_agente_nao_organico: str | None = None
    cod_missao_status: int | None
    dsc_missao_status: str | None = None
    cod_unidade_responsavel: int | None = None
    sig_unidade_responsavel: str | None = None
    nom_unidade_responsavel: str | None = None
    dsc_arvore_unidade_responsavel: str | None = None
    flg_reg_excluido: bool 
    dsc_justificativa_exclusao: str | None = None
    cif_usuario_inc: int = 0
    cif_usuario_alt: int = 0
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
    encarregados: list[MissaoEncarregadoReadDTO] = Field(default_factory=list)
    fontes_humanas: list[MissaoFonteHumanaDTO] = Field(default_factory=list)
    encarregados_quantidade: int | None = None
    nom_encarregado_titular: str | None = None

    @classmethod
    def from_model(cls, model: MissaoModel):
        tipo_missao_model = model.tipo
        recurso_tipo_model = model.recurso_tipo
        status_missao_model = model.status

        encarregados = [
            MissaoEncarregadoReadDTO(
                cod_missao_encarregado=item.cod_missao_encarregado,
                cod_missao=item.cod_missao,
                cod_agente=item.cod_agente,
                flg_titular=item.flg_titular,
                tip_papel=item.tip_papel,
                dat_inicio=item.dat_inicio,
                dat_fim=item.dat_fim,
                flg_reg_excluido=item.flg_reg_excluido,
                cif_usuario_inc=item.cif_usuario_inc,
                cif_usuario_alt=item.cif_usuario_alt,
                dat_hor_inclusao=item.dat_hor_inclusao,
                dat_hor_alteracao=item.dat_hor_alteracao,
            )
            for item in model.encarregados
            if not item.flg_reg_excluido
        ]

        fontes_humanas = [
            MissaoFonteHumanaDTO(
                cod_missao=item.cod_missao,
                cod_fonte_humana=item.cod_fonte_humana,
                sig_fonte_humana=getattr(item.fonte_humana, "sig_fonte_humana", None),
                descricao=getattr(item.fonte_humana, "sig_fonte_humana", None),
                flg_reg_excluido=item.flg_reg_excluido,
                cif_usuario_inc=item.cif_usuario_inc,
                cif_usuario_alt=item.cif_usuario_alt,
            )
            for item in model.fontes_humanas
            if not item.flg_reg_excluido
        ]

        quantidade_encarregados = sum(
            1 for e in model.encarregados
            if not e.flg_reg_excluido
        )
        nom_encarregado_titular = None

        return cls(
            cod_missao=model.cod_missao,
            cod_missao_tipo=model.cod_missao_tipo,
            cod_recurso_tipo=model.cod_recurso_tipo,
            sig_recurso_tipo=recurso_tipo_model.sig_recurso_tipo if recurso_tipo_model else None,
            dsc_recurso_tipo=recurso_tipo_model.dsc_recurso_tipo if recurso_tipo_model else None,
            dsc_missao_tipo=tipo_missao_model.dsc_missao_tipo if tipo_missao_model else None,
            cod_caso=model.cod_caso,
            dsc_caso=model.caso.dsc_caso if model.caso else None,
            cod_operacao=model.cod_operacao,
            dsc_operacao=model.operacao.dsc_operacao if model.operacao else None,
            cod_pedido=model.cod_pedido,
            cod_unidade_elo=model.pedido.cod_unidade_elo if model.pedido else None,
            dsc_missao=model.dsc_missao,
            idn_agente_nao_organico=model.idn_agente_nao_organico,
            cod_unidade_responsavel=model.cod_unidade_responsavel,
            sig_unidade_responsavel=model.sig_unidade_responsavel,
            nom_unidade_responsavel=model.nom_unidade_responsavel,
            dsc_arvore_unidade_responsavel=model.dsc_arvore_unidade_responsavel,
            cod_missao_status=model.cod_missao_status,
            dsc_missao_status=status_missao_model.dsc_missao_status if status_missao_model else None,
            flg_reg_excluido=model.flg_reg_excluido,
            dsc_justificativa_exclusao=model.dsc_justificativa_exclusao,
            cif_usuario_inc=model.cif_usuario_inc,
            cif_usuario_alt=model.cif_usuario_alt,
            dat_hor_inclusao=model.dat_hor_inclusao,
            dat_hor_alteracao=model.dat_hor_alteracao,
            encarregados_quantidade=quantidade_encarregados,
            nom_encarregado_titular=nom_encarregado_titular,
            encarregados=encarregados,
            fontes_humanas=fontes_humanas,
        )


class MissaoDeleteDTO(UpdateSchema):
    justificativa: str = Field(min_length=1)
    cif_usuario_alt: int = 0

