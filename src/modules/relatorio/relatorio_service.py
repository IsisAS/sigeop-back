from __future__ import annotations

from datetime import datetime

from src.common.service import AbstractService
from src.core.errors.errors import ValidationError
from src.modules.relatorio.relatorio_model import RelatorioModel
from src.modules.relatorio.relatorio_repository import RelatorioRepository
from src.modules.relatorio.relatorio_schema import (
    RelatorioCreateDTO,
    RelatorioDifusaoDTO,
    RelatorioPedidoResumoDTO,
    RelatorioReadDTO,
    RelatorioStatusDTO,
    RelatorioTipoDTO,
    RelatorioUpdateDTO,
)


class RelatorioService(
    AbstractService[RelatorioModel, RelatorioCreateDTO, RelatorioUpdateDTO, RelatorioReadDTO]
):
    read_dto = RelatorioReadDTO

    def __init__(self, repository: RelatorioRepository):
        self.repository = repository

    def list(self, *, limit: int = 50, offset: int = 0) -> list[RelatorioReadDTO]:
        return [self._to_read(item) for item in self.repository.list(limit=limit, offset=offset)]

    def get(self, entity_id: int) -> RelatorioReadDTO:
        return self._to_read(self.repository.get(entity_id))

    def create(self, dto: RelatorioCreateDTO) -> RelatorioReadDTO:
        self._validate(dto)
        return self._to_read(self.repository.create(dto))

    def update(self, entity_id: int, dto: RelatorioUpdateDTO) -> RelatorioReadDTO:
        self._validate(dto, entity_id)
        return self._to_read(self.repository.update(entity_id, dto))

    def list_tipos(self) -> list[RelatorioTipoDTO]:
        return [
            RelatorioTipoDTO.model_validate(item, from_attributes=True)
            for item in self.repository.list_tipos_permitidos()
        ]

    def list_status(self) -> list[RelatorioStatusDTO]:
        return [
            RelatorioStatusDTO.model_validate(item, from_attributes=True)
            for item in self.repository.list_status()
        ]

    def list_pedidos_elegiveis(self) -> list[RelatorioPedidoResumoDTO]:
        ano_atual = datetime.now().year
        return [self._pedido_to_read(pedido, status) for pedido, status in self.repository.list_pedidos_elegiveis(ano_atual)]

    def _validate(
        self,
        dto: RelatorioCreateDTO | RelatorioUpdateDTO,
        cod_relatorio: int | None = None,
    ) -> None:
        if not self.repository.tipo_permitido(dto.cod_relatorio_tipo):
            raise ValidationError("O tipo do relatório deve ser RDI ou RELINT.")
        if not self.repository.status_valido(dto.cod_relatorio_status):
            raise ValidationError("Status de relatório inválido.")
        if len(dto.pedidos) != len(set(dto.pedidos)):
            raise ValidationError("Não é permitido associar o mesmo pedido mais de uma vez.")
        pedidos_permitidos = self.repository.codigos_pedidos_elegiveis(datetime.now().year)
        if cod_relatorio is not None:
            pedidos_permitidos.update(
                self.repository.codigos_pedidos_associados(cod_relatorio)
            )
        if not set(dto.pedidos).issubset(pedidos_permitidos):
            raise ValidationError(
                "Somente pedidos abertos do ano corrente podem ser associados ao relatório."
            )
        codigos_difusao = [item.cod_unidade for item in dto.difusoes]
        if len(codigos_difusao) != len(set(codigos_difusao)):
            raise ValidationError("Não é permitido inserir a mesma unidade de difusão mais de uma vez.")

    def _to_read(self, item: RelatorioModel) -> RelatorioReadDTO:
        return RelatorioReadDTO(
            cod_relatorio=item.cod_relatorio,
            cod_relatorio_tipo=item.cod_relatorio_tipo,
            cod_relatorio_status=item.cod_relatorio_status,
            cod_unidade=item.cod_unidade,
            sig_unidade=item.sig_unidade,
            nom_unidade=item.nom_unidade,
            dsc_arvore_unidade=item.dsc_arvore_unidade,
            num_relatorio=item.num_relatorio,
            num_ano=item.num_ano,
            dat_emissao=item.dat_emissao,
            dsc_assunto=item.dsc_assunto,
            idn_processo=item.idn_processo,
            idn_agente_nao_organico=item.idn_agente_nao_organico,
            flg_reg_excluido=item.flg_reg_excluido,
            cif_usuario_inc=item.cif_usuario_inc,
            cif_usuario_alt=item.cif_usuario_alt,
            dat_hor_inclusao=item.dat_hor_inclusao,
            dat_hor_alteracao=item.dat_hor_alteracao,
            sig_relatorio_tipo=item.tipo.sig_relatorio_tipo,
            dsc_relatorio_tipo=item.tipo.dsc_relatorio_tipo,
            sig_relatorio_status=item.status.sig_relatorio_status,
            dsc_relatorio_status=item.status.dsc_relatorio_status,
            num_ordem_status=item.status.num_ordem,
            pedidos=[
                self._pedido_to_read(
                    vinculo.pedido,
                    vinculo.pedido.pedido_status.dsc_pedido_status
                    if vinculo.pedido.pedido_status
                    else None,
                )
                for vinculo in item.pedidos
                if not vinculo.flg_reg_excluido
            ],
            difusoes=[
                RelatorioDifusaoDTO(
                    cod_unidade=difusao.cod_unidade,
                    sig_unidade=difusao.sig_unidade,
                    nom_unidade=difusao.nom_unidade,
                    dsc_arvore_unidade=difusao.dsc_arvore_unidade,
                )
                for difusao in item.difusoes
                if not difusao.flg_reg_excluido and difusao.cod_unidade is not None
            ],
        )

    @staticmethod
    def _pedido_to_read(pedido, status_descricao: str | None) -> RelatorioPedidoResumoDTO:
        unidade = pedido.sig_unidade_analise or pedido.nom_unidade_analise or str(pedido.cod_unidade_analise)
        identificacao = f"{pedido.num_pedido} / {pedido.num_ano} / {unidade}"
        assunto = (pedido.dsc_assunto or "").strip()
        return RelatorioPedidoResumoDTO(
            cod_pedido=pedido.cod_pedido,
            num_pedido=pedido.num_pedido,
            num_ano=pedido.num_ano,
            cod_unidade_analise=pedido.cod_unidade_analise,
            sig_unidade_analise=pedido.sig_unidade_analise,
            nom_unidade_analise=pedido.nom_unidade_analise,
            sig_unidade_elo=pedido.sig_unidade_elo,
            nom_unidade_elo=pedido.nom_unidade_elo,
            dsc_assunto=pedido.dsc_assunto,
            dat_prazo=pedido.dat_prazo,
            cod_pedido_status=pedido.cod_pedido_status,
            dsc_pedido_status=status_descricao,
            display_text=f"{identificacao} - {assunto}" if assunto else identificacao,
        )
