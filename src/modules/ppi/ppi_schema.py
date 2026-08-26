from pydantic import Field
from datetime import datetime, date
from typing import Optional
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema
from decimal import Decimal
from src.modules.ppi.ppi_model import PPIModel

class PPIDto:
    cod_unidade: int
    num_ppi: int
    sig_unidade: str | None = None
    nom_unidade: str | None = None
    dsc_arvore_unidade: str | None = None
    num_ano: int
    nom_ppi: str
    idn_codigo_poa_sigiloso: str
    idn_codigo_poa_ostensivo: str
    val_orcamento_sigiloso:  Decimal | None = None
    val_orcamento_ostensivo:  Decimal | None = None
    flg_ativo:  bool | None = None
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None

class PPIReadDTO(PPIDto, ReadSchema):
    cod_ppi: int
    ppi_unidade: str | None = None

    @classmethod
    def from_model(cls, model: PPIModel):
        ppi_unidade = model.nom_unidade

        return cls (
            cod_ppi= model.cod_ppi,
            num_ppi= model.num_ppi,
            cod_unidade= model.cod_unidade,
            sig_unidade= model.sig_unidade,
            nom_unidade= model.nom_unidade,
            dsc_arvore_unidade= model.dsc_arvore_unidade,
            num_ano= model.num_ano,
            nom_ppi= model.nom_ppi,
            idn_codigo_poa_sigiloso= model.idn_codigo_poa_sigiloso,
            idn_codigo_poa_ostensivo= model.idn_codigo_poa_ostensivo,
            val_orcamento_sigiloso=  model.val_orcamento_sigiloso,
            val_orcamento_ostensivo=  model.val_orcamento_ostensivo,
            flg_reg_excluido= model.flg_reg_excluido,
            cif_usuario_inc= model.cif_usuario_inc,
            cif_usuario_alt= model.cif_usuario_alt,
            ppi_unidade= ppi_unidade,
            flg_ativo = model.flg_ativo
        )

    pass

class PPIUpdateDTO(PPIDto, UpdateSchema):
    pass

class PPICreateDTO(PPIDto, CreateSchema):
    pass