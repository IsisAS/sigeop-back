from typing import Sequence

from src.common.service import AbstractService
from src.modules.pedido.pedido_model import PedidoModel
from src.modules.pedido.pedido_repository import PedidoRepository
from src.modules.pedido.pedido_schema import PedidoCreateDTO, PedidoReadDTO, PedidoUpdateDTO, UnidadeDestinatariaDTO
from src.modules.ciclo.ciclo_service import CicloService
from typing import Any


class PedidoService(AbstractService[PedidoModel, PedidoCreateDTO, PedidoReadDTO, PedidoUpdateDTO]):
    read_dto = PedidoReadDTO


    def __init__(self, repo: PedidoRepository, ciclo_service: CicloService | None = None):
        self.repository = repo
        self.ciclo_service = ciclo_service


    def _carregar_e_preparar_unidades_destinatarias(
        self, codigos_solicitados: list[int]
    ) -> list[UnidadeDestinatariaDTO]:
        """
        Busca os dados completos das unidades destinatárias no Ciclo e os prepara
        para serem salvos no banco, incluindo sigla, nome e a fração da unidade.
        """
        if not self.ciclo_service or not codigos_solicitados:
            return []

        unidades_cadastradas_no_ciclo = self.ciclo_service.get_unidades_destinatarias()

        indice_por_codigo: dict[int, dict] = {
            int(unidade["codigo"]): unidade
            for unidade in unidades_cadastradas_no_ciclo
            if unidade.get("codigo") is not None
        }

        unidades_preparadas: list[UnidadeDestinatariaDTO] = []
        for codigo_unidade in codigos_solicitados:
            dados_da_unidade = indice_por_codigo.get(codigo_unidade)
            if not dados_da_unidade:
                continue

            unidades_preparadas.append(
                UnidadeDestinatariaDTO(
                    cod_unidade_destinataria=int(dados_da_unidade["codigo"]),
                    sig_unidade_destinataria=dados_da_unidade.get("sigla"),
                    nom_unidade_destinataria=dados_da_unidade.get("nome"),
                    dsc_arvore_unidade_destinataria=dados_da_unidade.get("nomeFracao"),
                )
            )
        return unidades_preparadas


    def _with_analistas_nome(self, item: dict) -> dict:
        row = dict(item)
        analistas = row.get("analistas", [])
        analistas_enriquecidos = []
        for analista in analistas:
            analista_row = dict(analista)
            analista_row.setdefault("nom_agente", None)
            analista_row.setdefault("dat_inicio", None)
            analista_row.setdefault("dat_fim", None)
            analistas_enriquecidos.append(analista_row)
        row["analistas"] = analistas_enriquecidos
        return row


    def _with_unidades(self, item: dict) -> dict:
        row = self._with_unidades_many([item])[0]
        row = self._with_analistas_nome(row)
        return row


    def _with_unidades_many(self, items: list[dict]) -> list[dict]:
        if not items:
            return items

        enriched: list[dict] = []
        for item in items:
            row = dict(item)
            row["nom_unidade_analise"] = None
            row["sig_unidade_analise"] = None
            row["nom_unidade_elo"] = None
            row["sig_unidade_elo"] = None
            enriched.append(row)

        return enriched


    def list(self, *, limit: int = 50, offset: int = 0) -> Sequence[PedidoReadDTO]:
        items = self.repository.list(limit=limit, offset=offset)
        enriched = [self._with_analistas_nome(item) for item in self._with_unidades_many(items)]
        return [self.read_dto.model_validate(item) for item in enriched]


    def get(self, entity_id):
        item = self.repository.get(entity_id)
        return self.read_dto.model_validate(self._with_unidades(item))


    def create(self, dto: PedidoCreateDTO) -> PedidoReadDTO:
        if not dto.num_pedido:
            dto.num_pedido = self._generate_num_pedido(dto.num_ano)
        
        item = self.repository.create(dto)
        return self.read_dto.model_validate(self._with_unidades(item))

    def _generate_num_pedido(self, num_ano: int) -> str:
        """
        Gera número de pedido no formato PED-NNNN (até 4 dígitos)
        Busca o maior número existente para o ano e incrementa
        """
        from sqlalchemy import func, text
        db = self.repository.db
        
        pedidos = db.query(self.repository.model.num_pedido).filter(
            self.repository.model.num_ano == num_ano
        ).all()
        
        max_num = 0
        for (num_pedido,) in pedidos:
            if num_pedido and '-' in num_pedido:
                try:
                    num_part = int(num_pedido.split('-')[1])
                    max_num = max(max_num, num_part)
                except (ValueError, IndexError):
                    pass
        
        next_num = max_num + 1
        
        if next_num > 9999:
            raise ValueError(f"Limite de pedidos ({max_num}) atingido para o ano {num_ano}")
        
        return f"PED-{next_num:04d}"


    def update(self, entity_id, dto: PedidoUpdateDTO) -> PedidoReadDTO:
        unidades_destinatarias_para_gravar: list[UnidadeDestinatariaDTO] = []
        if dto.unidades_destinatarias is not None:
            codigos_das_unidades = [
                item for item in dto.unidades_destinatarias
            ]
            unidades_destinatarias_para_gravar = self._carregar_e_preparar_unidades_destinatarias(
                codigos_das_unidades
            )

        item = self.repository.update(
            entity_id,
            dto,
            unidades_destinatarias=unidades_destinatarias_para_gravar,
        )
        return self.read_dto.model_validate(self._with_unidades(item))


    def get_complementares(self, cod_pedido_original: int) -> Sequence[PedidoReadDTO]:
        items = self.repository.list_by_original_id(cod_pedido_original)
        enriched = [self._with_analistas_nome(item) for item in self._with_unidades_many(items)]
        return [self.read_dto.model_validate(item) for item in enriched]
    
    def get_pedidos_elegiveis_para_caso(
        self,
        limit: int = 100,
        offset: int = 0,
        cod_caso: int | None = None,
    ) -> Sequence[dict]:
        return self.repository.get_pedidos_elegiveis_para_caso(
            limit=limit,
            offset=offset,
            cod_caso=cod_caso,
        )

    def verificar_vinculos(self, cod_pedido: int) -> dict[str, Any]:
        self.get(cod_pedido)
        return self.repository.verificar_vinculos(cod_pedido)

    def soft_delete(self, cod_pedido: int, justificativa: str | None, cif_usuario_alt: int | None) -> None:
        obj = self.repository.soft_delete(cod_pedido, justificativa, cif_usuario_alt)
        self.repository.db.commit()
        return None