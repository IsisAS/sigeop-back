from typing import List
from src.common.service import AbstractService
from src.modules.operacao.operacao_encarregado.operacao_encarregado_model import OperacaoEncarregadoModel
from src.modules.operacao.operacao_model import OperacaoModel
from src.modules.operacao.operacao_repository import OperacaoRepository
from src.modules.operacao.operacao_schema import OperacaoCreateDTO, OperacaoReadDTO, OperacaoUpdateDTO, EncarregadoDto, GridMissaoDTO, GridPlanoDTO, OperacaoInteligenciaProtecaoGridDTO
from src.core.errors.errors import NotFoundError, ConflictError
from src.modules.pedido.pedido_schema import PedidoReadDTO


class OperacaoService(AbstractService[OperacaoModel, OperacaoCreateDTO, OperacaoReadDTO, OperacaoUpdateDTO]):
    read_dto = OperacaoReadDTO
    model_encarregados = OperacaoEncarregadoModel

    def __init__(self, repository: OperacaoRepository):
        self.repository = repository
    
    def list(self, *, limit: int = 50, offset: int = 0) -> list[OperacaoReadDTO]:
        operacao_list = self.repository.list(limit = limit, offset = offset)
        return [OperacaoReadDTO.from_model(item) for item in operacao_list]
    
    def get_by_id(self, id: int) -> OperacaoReadDTO:
        result = self.repository.get_by_id(id)
        if not result:
            raise NotFoundError(f"Operação com ID {id} não encontrada.")
    
        return self.read_dto.model_validate(result)

    def create(self, dto: OperacaoCreateDTO) -> OperacaoReadDTO:
        operacao_dict = self.repository.create(dto)
        return self.read_dto.model_validate(operacao_dict)

    def update(self, id: int, dto: OperacaoUpdateDTO) -> OperacaoReadDTO:
        operacao_atualizada = self.repository.update(id, dto)
        if not operacao_atualizada:
            raise NotFoundError(f"Operação com ID {id} não encontrada para atualização.")
            
        return self.read_dto.model_validate(operacao_atualizada)

    def get_by_caso(self, caso_id, limit: int = 50, offset: int = 0):
        operacao_list = self.repository.get_operacao_by_caso_id(caso_id)

        return [OperacaoReadDTO.from_model(item) for item in operacao_list]

    def listar_inteligencia_protecao(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[OperacaoInteligenciaProtecaoGridDTO]:
        operacoes = self.repository.listar_inteligencia_protecao(limit=limit, offset=offset)
        return [OperacaoInteligenciaProtecaoGridDTO.model_validate(item) for item in operacoes]

    def listar_missoes_por_operacao(self, cod_operacao: int) -> List[GridMissaoDTO]:
        missoes_model = self.repository.listar_missoes_por_operacao(cod_operacao)
        resultados = []
        for mi in missoes_model:
            titular = next((e for e in mi.encarregados if e.flg_titular and not e.flg_reg_excluido), None)
            
            resultados.append(GridMissaoDTO(
                cod_missao=mi.cod_missao,
                dsc_tipo=getattr(mi.tipo, 'dsc_missao_tipo', None),
                dsc_recurso_tipo=getattr(mi.recurso_tipo, 'dsc_recurso_tipo', None),
                dsc_status=getattr(mi.status, 'dsc_missao_status', None),
                cif_encarregado=str(titular.cod_agente) if titular else "Não definido"
            ))
        return resultados

    def listar_planos_por_operacao(self, cod_operacao: int) -> List[GridPlanoDTO]:
        planos_model = self.repository.listar_planos_por_operacao(cod_operacao)
        resultados = []
        for pl in planos_model:
            resultados.append(GridPlanoDTO(
                cod_plano=pl.cod_plano,
                num_plano=pl.num_plano,
                num_ano=pl.num_ano,
                dsc_assunto=pl.dsc_assunto,
                dsc_status=getattr(pl.plano_status, 'dsc_plano_status', None)
            ))
        return resultados

    def listar_pedidos_por_operacao(self, cod_operacao: int) -> List[PedidoReadDTO]:
        pedidos_model = self.repository.listar_pedidos_por_operacao(cod_operacao)
        return [PedidoReadDTO.model_validate(pedido) for pedido in pedidos_model]

    def delete(self, cod_operacao: int, dsc_justificativa_exclusao: str) -> None:
        self.repository.get(cod_operacao)

        missoes = self.repository.listar_missoes_por_operacao(cod_operacao)
        planos = self.repository.listar_planos_por_operacao(cod_operacao)
        if missoes or planos:
            linhas: list[str] = []
            if missoes:
                numeros = ", ".join(str(m.cod_missao) for m in missoes)
                linhas.append(f"Missão Nº {numeros}")
            if planos:
                numeros = ", ".join(
                    f"{p.num_plano}, {p.num_ano}"
                    if getattr(p, "num_ano", None) is not None
                    else p.num_plano
                    for p in planos
                )
                linhas.append(f"Plano Nº {numeros}")
            raise ConflictError(
                "Exclusão não permitida pois esta Operação está vinculada a: "
                + " | ".join(linhas)
            )

        try:
            self.repository.delete(cod_operacao, dsc_justificativa_exclusao=dsc_justificativa_exclusao)
            self.repository.commit()
        except Exception:
            self.repository.rollback()
            raise
