from pydantic import Field
from typing import Optional
from src.common.schemas import ReadSchema


class OperacaoRecrutamentoReadDTO(ReadSchema):
    """
    DTO de leitura para a grid de Operações de Recrutamento (Menu 3.1.2).

    apenas operações do tipo 'Ampliação de recursos operacionais'
          com recurso tipo 'Agente não-orgânico'.
    pode_editar = False quando há caso vinculado.
    encarregado_cif = CIF do encarregado titular ativo.
    """

    cod_operacao: int
    nom_operacao: str
    nom_caso: Optional[str] = None
    cod_caso: Optional[int] = None
    encarregado_cif: Optional[int] = None
    dsc_operacao_status: Optional[str] = None
    pode_editar: bool = False
