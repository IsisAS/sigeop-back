from datetime import date, datetime
from src.common.schemas import CreateSchema, UpdateSchema, ReadSchema
from src.modules.caso.caso.caso_model import CasoModel
from typing import Optional

class GridOperacaoDTO(ReadSchema):
    cod_operacao: int
    nom_operacao: str
    dsc_status: Optional[str] = None
    cif_encarregado: Optional[str] = None

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

class EncarregadoCreateDto(CreateSchema):
    cod_agente: int
    flg_titular: bool
    dat_inicio: datetime
    flg_reg_excluido: bool
    

class EncarregadoDto(EncarregadoCreateDto):
    cod_caso_encarregado: int | None = None
    nom_agente: str | None = None

class CasoCreateDTO(CreateSchema):
    cod_pedido_abertura: int
    nom_caso: str
    dsc_caso: str
    flg_reg_excluido: bool
    cif_usuario_inc: int 
    cif_usuario_alt: int 
    cod_caso_status: int
    encarregados: list[EncarregadoCreateDto]

class CasoUpdateDTO(UpdateSchema):
    cod_pedido_abertura: int
    nom_caso: str
    dsc_caso: str
    flg_reg_excluido: bool
    cif_usuario_inc: int 
    cif_usuario_alt: int 
    cod_caso_status: int
    encarregados: list[EncarregadoDto]
    pedidos_vinculados: list[int] = []

class CasoDTO(ReadSchema):
    cod_caso: int
    cod_pedido_abertura: int
    nom_caso: str
    dsc_caso: str
    flg_reg_excluido: bool
    cif_usuario_inc: int
    cif_usuario_alt: int
    dat_hor_inclusao: datetime | None = None
    dat_hor_alteracao: datetime | None = None
    cod_caso_status: int

class CasoReadDTO(CasoDTO):
    encarregados: list[EncarregadoDto]

    @classmethod
    def from_model(cls, model: CasoModel, encarregados: list[EncarregadoDto]):
        return cls(
            cod_caso=model.cod_caso,
            cod_pedido_abertura=model.cod_pedido_abertura,
            nom_caso=model.nom_caso,
            dsc_caso=model.dsc_caso,
            flg_reg_excluido=model.flg_reg_excluido,
            cif_usuario_inc=model.cif_usuario_inc,
            cif_usuario_alt=model.cif_usuario_alt,
            dat_hor_inclusao=model.dat_hor_inclusao,
            dat_hor_alteracao=model.dat_hor_alteracao,
            cod_caso_status=model.cod_caso_status,
            encarregados=encarregados
        )

class InformacoesPedidoDto(ReadSchema):
    num_pedido: str | None
    num_ano: int | None
    dat_prazo: date | None = None
    cod_unidade_analise: int | None = None
    cod_unidade_elo: int | None = None

class ListarCasoDto(CasoDTO):
    pedido: InformacoesPedidoDto | None
    dsc_caso_status: str | None
    qtde_encarregados: int

