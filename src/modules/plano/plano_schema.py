from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema
from decimal import Decimal
from src.modules.plano.plano_equipe.plano_equipe_schema import PlanoEquipeReadDTO
from src.modules.plano.plano_local.plano_local_schema import PlanoLocalReadDTO
from src.modules.plano.plano_model import PlanoModel

class PlanoDto:
    cod_plano_tipo: int 
    cod_plano_status: int
    cod_caso: int | None = None
    cod_operacao: int | None = None
    cod_missao: int | None = None
    cod_unidade: int | None = None
    sig_unidade: str | None = None
    nom_unidade: str | None = None
    dsc_arvore_unidade: str | None = None
    tip_plano_contexto: str | None = None
    idn_processo: str | None = None
    num_plano: str
    num_ano: int
    dat_emissao: datetime
    dat_aprovacao: datetime | None = None
    dat_inicio: datetime
    dat_termino: datetime 
    dat_baixa: datetime | None = None
    num_equipe: int | None = None
    dsc_assunto: str | None = None
    vlr_custo_estimado: Decimal | None = None
    vlr_verba_sigilosa_aprovada: Decimal | None = None
    vlr_verba_ostensiva_aprovada: Decimal | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
    plano_status: str | None = None
    plano_tipo: str | None = None

class PlanoReadDTO(PlanoDto, ReadSchema):
    cod_plano: int
    plano_equipe: list[PlanoEquipeReadDTO]
    local: list[PlanoLocalReadDTO]
    
    @classmethod
    def from_model(cls, model: PlanoModel):
        planos_status_model = getattr(model, "plano_status", None)
        plano_tipo_model = getattr(model, "plano_tipo", None)
       
        pass
        return cls (
            cod_plano_tipo = model.cod_plano_tipo,
            cod_plano_status = model.cod_plano_status,
            cod_caso = getattr(model, "cod_caso", None),
            cod_operacao = getattr(model, "cod_operacao", None),
            cod_unidade = model.cod_unidade,
            sig_unidade = model.sig_unidade,
            nom_unidade = model.nom_unidade,
            dsc_arvore_unidade = model.dsc_arvore_unidade,
            cod_missao = getattr(model, "cod_missao", None),
            tip_plano_contexto = model.tip_plano_contexto,
            idn_processo = model.idn_processo,
            num_plano = model.num_plano,
            num_ano = model.num_ano,
            dat_emissao = model.dat_emissao,
            dat_aprovacao = model.dat_aprovacao,
            dat_inicio = model.dat_inicio,
            dat_termino = model.dat_termino,
            dsc_assunto = model.dsc_assunto,
            dat_baixa = model.dat_baixa,
            vlr_custo_estimado = model.vlr_custo_estimado,
            vlr_verba_sigilosa_aprovada = model.vlr_verba_sigilosa_aprovada,
            vlr_verba_ostensiva_aprovada = model.vlr_verba_ostensiva_aprovada,
            flg_reg_excluido = model.flg_reg_excluido,
            cif_usuario_inc = model.cif_usuario_inc,
            cif_usuario_alt = model.cif_usuario_alt,
            dat_hor_inclusao = model.dat_hor_inclusao,
            dat_hor_alteracao = model.dat_hor_alteracao,
            cod_plano = model.cod_plano,
            plano_status = planos_status_model.dsc_plano_status if planos_status_model else None,
            plano_tipo = plano_tipo_model.dsc_plano_tipo if plano_tipo_model else None,
            plano_equipe = model.plano_equipe,
            local = model.local,
            num_equipe = model.num_equipe
        )


class PlanoUpdateDTO(PlanoDto, UpdateSchema):
    plano_equipe: list[PlanoEquipeReadDTO]
    local: list[PlanoLocalReadDTO]
    pass

class PlanoCreateDTO(PlanoDto, CreateSchema):
    plano_equipe: list[PlanoEquipeReadDTO]
    local: list[PlanoLocalReadDTO]
    pass
