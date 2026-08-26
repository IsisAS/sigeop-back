from __future__ import annotations
from datetime import datetime
from typing import Any, List, Dict
from sqlalchemy import MetaData, Table, select, and_, not_, literal
from src.common.repository import AbstractRepository
from src.core.errors.errors import NotFoundError, ConflictError
from src.modules.pedido.pedido_model import PedidoModel
from src.modules.pedido.pedido_schema import PedidoCreateDTO, PedidoUpdateDTO, UnidadeDestinatariaDTO
from src.modules.pedido.analista.analista_model import AnalistaModel 
from src.modules.pedido.status.status_model import StatusModel
from src.modules.pedido.unidade_destinataria.unidade_destinataria_model import UnidadeDestinatariaModel
from src.modules.caso.caso_pedido.caso_pedido_model import CasoPedidoModel
from src.modules.caso.caso_pedido.caso_pedido_repository import CasoPedidoRepository

class PedidoRepository(AbstractRepository[PedidoModel, PedidoCreateDTO, PedidoUpdateDTO]):
    model = PedidoModel  

    def _listar_analistas_por_pedido(self, cod_pedido: int) -> list[dict[str, Any]]:
        analistas = (
            self.db.query(AnalistaModel)
            .filter(
                AnalistaModel.cod_pedido == cod_pedido,
            )
            .order_by(
                AnalistaModel.flg_reg_excluido.asc(),
                AnalistaModel.flg_titular.desc(),
                AnalistaModel.dat_hor_inclusao.asc(),
            )
            .all()
        )

        return [
            {
                "cod_agente": analista.cod_agente,
                "nom_agente": None,
                "flg_titular": analista.flg_titular,
                "dat_inicio": analista.dat_inicio,
                "dat_fim": analista.dat_fim,
                "flg_reg_excluido": analista.flg_reg_excluido,
            }
            for analista in analistas
        ]
    
    def _listar_unidades_destinatarias_por_pedido(self, cod_pedido: int) -> list[dict[str, Any]]:
        unidades = (
            self.db.query(UnidadeDestinatariaModel)
            .filter(
                UnidadeDestinatariaModel.cod_pedido == cod_pedido,
                UnidadeDestinatariaModel.flg_reg_excluido == False,
            )
            .order_by(UnidadeDestinatariaModel.dat_hor_inclusao.asc())
            .all()
        )
        
        return [
            {
                "cod_unidade_destinataria": unidade.cod_unidade_destinataria,
                "sig_unidade_destinataria": unidade.sig_unidade_destinataria,
                "nom_unidade_destinataria": unidade.nom_unidade_destinataria,
                "dsc_arvore_unidade_destinataria": unidade.dsc_arvore_unidade_destinataria,
            }
            for unidade in unidades
        ]

    def create(self, obj_in: PedidoCreateDTO) -> PedidoModel:
        pedido_principal = None
        cod_pedido_relacionado = obj_in.cod_pedido_relacionado or obj_in.cod_pedido_original
        if cod_pedido_relacionado:
            pedido_principal = self.db.query(self.model).filter(
                self.model.cod_pedido == cod_pedido_relacionado
            ).first()
            if not pedido_principal:
                raise NotFoundError(f"{self.model.__name__}({cod_pedido_relacionado}) não encontrado.")

        pedido_data = obj_in.model_dump(
            exclude={"analistas", "cod_caso", "cod_casos", "cod_pedido_tipo", "cod_pedido_original"}
        )
        pedido_data["cod_pedido_relacionado"] = cod_pedido_relacionado

        db_obj = self.model(**pedido_data)
        self.db.add(db_obj)

        self.db.flush()

        if hasattr(obj_in, 'analistas') and obj_in.analistas:
            for analista_in in obj_in.analistas:
                vinculo_analista = AnalistaModel(
                    cod_pedido=db_obj.cod_pedido,
                    cod_agente=analista_in.cod_agente,
                    flg_titular=analista_in.flg_titular,
                    cif_usuario_inc=obj_in.cif_usuario_inc,
                    cif_usuario_alt=obj_in.cif_usuario_alt,
                    flg_reg_excluido=False
                )
                self.db.add(vinculo_analista)

        if pedido_principal and obj_in.dat_prazo > pedido_principal.dat_prazo:
            pedido_principal.dat_prazo = obj_in.dat_prazo
            pedido_principal.dat_hor_alteracao = datetime.utcnow()

        cod_casos = self._obter_cod_casos_do_payload(obj_in)
        if cod_casos is not None:
            self.sincronizar_casos_vinculados(
                cod_pedido=db_obj.cod_pedido,
                cod_casos=cod_casos,
                cif_usuario=obj_in.cif_usuario_alt,
            )

        self.db.commit()
        self.db.refresh(db_obj)

        return self.get_by_id(db_obj.cod_pedido)
    
    def get(self, entity_id: Any) -> dict[str, Any]:
        result = self.get_by_id(entity_id)
        if not result:
            raise NotFoundError(f"{self.model.__name__}({entity_id}) não encontrado.")
        return result

    def update(
        self,
        entity_id: Any,
        obj_in: PedidoUpdateDTO,
        *,
        unidades_destinatarias: list[UnidadeDestinatariaDTO] | None = None,
    ) -> dict[str, Any]:
        db_obj = self.db.query(PedidoModel).filter(PedidoModel.cod_pedido == entity_id).first()
        if not db_obj:
            raise ValueError(f"Pedido with id {entity_id} not found")

        pedido_data = obj_in.model_dump(
            exclude={"analistas", "cod_caso", "cod_casos", "cod_pedido_tipo", "cod_pedido_original", "unidades_destinatarias"},
            exclude_unset=True,
        )
        if "cod_pedido_relacionado" not in pedido_data and obj_in.cod_pedido_original is not None:
            pedido_data["cod_pedido_relacionado"] = obj_in.cod_pedido_original
        for field, value in pedido_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        if hasattr(obj_in, 'analistas'):
            vinculos_existentes = self.db.query(AnalistaModel).filter(
                AnalistaModel.cod_pedido == entity_id
            ).all()

            analistas_enviados = {(a.cod_agente, a.flg_titular, a.flg_reg_excluido) for a in obj_in.analistas or []}
            for vinculo in vinculos_existentes:
                chave = (vinculo.cod_agente, vinculo.flg_titular, vinculo.flg_reg_excluido)
                if chave not in analistas_enviados:
                    vinculo.flg_reg_excluido = True
                    vinculo.cif_usuario_alt = obj_in.cif_usuario_alt

            for analista_in in obj_in.analistas or []:
                vinculo_existente = next(
                    (v for v in vinculos_existentes if v.cod_agente == analista_in.cod_agente),
                    None
                )
                if vinculo_existente:
                    vinculo_existente.flg_titular = analista_in.flg_titular
                    vinculo_existente.flg_reg_excluido = analista_in.flg_reg_excluido
                    vinculo_existente.cif_usuario_alt = obj_in.cif_usuario_alt
                else:
                    vinculo_analista = AnalistaModel(
                        cod_pedido=entity_id,
                        cod_agente=analista_in.cod_agente,
                        flg_titular=analista_in.flg_titular,
                        cif_usuario_inc=db_obj.cif_usuario_inc,
                        cif_usuario_alt=obj_in.cif_usuario_alt,
                        flg_reg_excluido=analista_in.flg_reg_excluido
                    )
                    self.db.add(vinculo_analista)

        if obj_in.analistas:
            analistas_ativos = [a for a in obj_in.analistas if not a.flg_reg_excluido]
            titulares = [a for a in analistas_ativos if a.flg_titular]
            if len(titulares) > 1:
                raise ConflictError("Apenas um analista pode ser titular")
            if len(analistas_ativos) > 0 and len(titulares) == 0:
                raise ValueError("Deve haver pelo menos um analista titular")

        if unidades_destinatarias is not None:
            todos_vinculos_banco = self.db.query(UnidadeDestinatariaModel).filter(
                UnidadeDestinatariaModel.cod_pedido == entity_id
            ).all()

            vinculos_ativos = [
                v for v in todos_vinculos_banco if not v.flg_reg_excluido
            ]

            codigos_solicitados = {ud.cod_unidade_destinataria for ud in unidades_destinatarias}
            codigos_ativos = {v.cod_unidade_destinataria for v in vinculos_ativos}

            # Regra 1: existe no banco (ativo) e NÃO veio no payload → remover (exclusão lógica)
            for vinculo in vinculos_ativos:
                if vinculo.cod_unidade_destinataria not in codigos_solicitados:
                    vinculo.flg_reg_excluido = True
                    vinculo.cif_usuario_alt = obj_in.cif_usuario_alt

            # Regra 2: veio no payload e NÃO existe no banco (ativo) → criar
            # Se já existia anteriormente mas foi excluído, cria um novo registro (mantém histórico)
            for ud in unidades_destinatarias:
                if ud.cod_unidade_destinataria not in codigos_ativos:
                    # Create fake unit data if real data is not provided
                    fake_sigla = f"UD{ud.cod_unidade_destinataria:04d}"
                    fake_nome = f"Unidade Destinatária Fake {ud.cod_unidade_destinataria}"
                    fake_arvore = f"ROOT/SP/SAO_PAULO/{fake_sigla}"
                    
                    vinculo_ud = UnidadeDestinatariaModel(
                        cod_pedido=entity_id,
                        cod_unidade_destinataria=ud.cod_unidade_destinataria,
                        sig_unidade_destinataria=ud.sig_unidade_destinataria or fake_sigla,
                        nom_unidade_destinataria=ud.nom_unidade_destinataria or fake_nome,
                        dsc_arvore_unidade_destinataria=ud.dsc_arvore_unidade_destinataria or fake_arvore,
                        cif_usuario_inc=db_obj.cif_usuario_inc,
                        cif_usuario_alt=obj_in.cif_usuario_alt,
                        flg_reg_excluido=False,
                    )
                    self.db.add(vinculo_ud)

        cod_casos = self._obter_cod_casos_do_payload(obj_in)
        if cod_casos is not None:
            self.sincronizar_casos_vinculados(
                cod_pedido=entity_id,
                cod_casos=cod_casos,
                cif_usuario=obj_in.cif_usuario_alt,
            )

        self.db.commit()
        self.db.refresh(db_obj)

        return self.get_by_id(entity_id)

    def list(self, *, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        pedido = PedidoModel.__table__
        bind = self.db.get_bind()
        metadata = MetaData()
        pedido_status = Table("tb_pedido_status", metadata, autoload_with=bind, schema="sigeop")
        stmt = (
            select(
                pedido.c.cod_pedido,
                select(CasoPedidoModel.cod_caso)
                .where(
                    CasoPedidoModel.cod_pedido == pedido.c.cod_pedido,
                    CasoPedidoModel.flg_reg_excluido == False,
                )
                .limit(1)
                .scalar_subquery()
                .label("cod_caso"),
                pedido.c.cod_ppi,
                literal(None).label("cod_pedido_tipo"),
                literal(None).label("dsc_pedido_tipo"),
                pedido.c.cod_pedido_relacionado.label("cod_pedido_original"),
                pedido.c.cod_pedido_relacionado,
                pedido.c.cod_unidade_analise,
                pedido.c.cod_unidade_elo,
                pedido.c.num_pedido,
                pedido.c.num_ano,
                pedido.c.dat_emissao,
                pedido.c.dsc_assunto,
                pedido.c.dsc_tematica,
                pedido.c.idn_processo,
                pedido.c.dat_prazo,
                pedido.c.cod_pedido_status,
                pedido_status.c.dsc_pedido_status,
                pedido.c.flg_reg_excluido,
                pedido.c.cif_usuario_inc,
                pedido.c.cif_usuario_alt,
                pedido.c.dat_hor_inclusao,
                pedido.c.dat_hor_alteracao,
            )
            .select_from(
                pedido.outerjoin(
                    pedido_status,
                    pedido_status.c.cod_pedido_status == pedido.c.cod_pedido_status,
                )
            )
            .where(pedido.c.flg_reg_excluido == False)
            .order_by(pedido.c.cod_pedido.desc())
            .limit(limit)
            .offset(offset)
        )

        rows = self.db.execute(stmt).mappings().all()
        pedidos = [dict(row) for row in rows]
        for pedido_dict in pedidos:
            cod_casos = self.listar_cod_casos_ativos_por_pedido(pedido_dict["cod_pedido"])
            pedido_dict["cod_casos"] = cod_casos
            pedido_dict["cod_caso"] = cod_casos[0] if cod_casos else None
            pedido_dict["analistas"] = self._listar_analistas_por_pedido(pedido_dict["cod_pedido"])
            pedido_dict["unidades_destinatarias"] = self._listar_unidades_destinatarias_por_pedido(pedido_dict["cod_pedido"])
        return pedidos

    def get_by_id(self, cod_pedido: int) -> dict[str, Any] | None:
        pedido = PedidoModel.__table__
        pedido_status = StatusModel.__table__
        stmt = (
            select(
                pedido.c.cod_pedido,
                select(CasoPedidoModel.cod_caso)
                .where(
                    CasoPedidoModel.cod_pedido == pedido.c.cod_pedido,
                    CasoPedidoModel.flg_reg_excluido == False,
                )
                .limit(1)
                .scalar_subquery()
                .label("cod_caso"),
                pedido.c.cod_ppi,
                literal(None).label("cod_pedido_tipo"),
                literal(None).label("dsc_pedido_tipo"),
                pedido.c.cod_pedido_relacionado.label("cod_pedido_original"),
                pedido.c.cod_pedido_relacionado,
                pedido.c.cod_unidade_analise,
                pedido.c.sig_unidade_analise,
                pedido.c.nom_unidade_analise,
                pedido.c.dsc_arvore_unidade_analise,
                pedido.c.cod_unidade_elo,
                pedido.c.sig_unidade_elo,
                pedido.c.nom_unidade_elo,
                pedido.c.dsc_arvore_unidade_elo,
                pedido.c.num_pedido,
                pedido.c.num_ano,
                pedido.c.dat_emissao,
                pedido.c.dsc_assunto,
                pedido.c.dsc_tematica,
                pedido.c.idn_processo,
                pedido.c.dat_prazo,
                pedido.c.cod_pedido_status,
                pedido_status.c.dsc_pedido_status,
                pedido.c.flg_reg_excluido,
                pedido.c.cif_usuario_inc,
                pedido.c.cif_usuario_alt,
                pedido.c.dat_hor_inclusao,
                pedido.c.dat_hor_alteracao,
            )
            .select_from(
                pedido.outerjoin(
                    pedido_status,
                    pedido_status.c.cod_pedido_status == pedido.c.cod_pedido_status,
                )
            )
            .where(pedido.c.cod_pedido == cod_pedido,
                   pedido.c.flg_reg_excluido == False)
        )

        row = self.db.execute(stmt).mappings().first()
        if not row:
            return None

        pedido_dict = dict(row)

        pedido_dict["analistas"] = self._listar_analistas_por_pedido(cod_pedido)
        pedido_dict["cod_casos"] = self.listar_cod_casos_ativos_por_pedido(cod_pedido)
        pedido_dict["cod_caso"] = pedido_dict["cod_casos"][0] if pedido_dict["cod_casos"] else None
        pedido_dict["unidades_destinatarias"] = self._listar_unidades_destinatarias_por_pedido(cod_pedido)

        return pedido_dict

    def listar_casos_pedido_por_pedido(self, cod_pedido: int) -> list[CasoPedidoModel]:
        return CasoPedidoRepository(self.db).listar_por_pedido(cod_pedido)

    def listar_cod_casos_ativos_por_pedido(self, cod_pedido: int) -> list[int]:
        return CasoPedidoRepository(self.db).listar_cod_casos_ativos_por_pedido(cod_pedido)

    def _obter_cod_casos_do_payload(self, obj_in: PedidoCreateDTO | PedidoUpdateDTO) -> list[int] | None:
        if "cod_casos" in obj_in.model_fields_set:
            if obj_in.cod_casos is None:
                return None
            return [int(cod_caso) for cod_caso in obj_in.cod_casos]

        if "cod_caso" in obj_in.model_fields_set and obj_in.cod_caso is not None:
            return [int(obj_in.cod_caso)]

        return None

    def sincronizar_casos_vinculados(
        self,
        *,
        cod_pedido: int,
        cod_casos: list[int],
        cif_usuario: int,
    ) -> None:
        CasoPedidoRepository(self.db).sincronizar_por_pedido(
            cod_pedido=cod_pedido,
            cod_casos=cod_casos,
            cif_usuario=cif_usuario,
        )

    def list_by_original_id(self, cod_pedido_original: int) -> List[Dict[str, Any]]:
        pedido = self.model.__table__
        pedido_status = StatusModel.__table__
        stmt = (
            select(
                pedido.c.cod_pedido,
                pedido.c.cod_ppi,
                literal(None).label("cod_pedido_tipo"),
                literal(None).label("dsc_pedido_tipo"),
                pedido.c.cod_pedido_relacionado.label("cod_pedido_original"),
                pedido.c.cod_pedido_relacionado,
                pedido.c.cod_unidade_analise,
                pedido.c.sig_unidade_analise,
                pedido.c.nom_unidade_analise,
                pedido.c.dsc_arvore_unidade_analise,
                pedido.c.cod_unidade_elo,
                pedido.c.sig_unidade_elo,
                pedido.c.nom_unidade_elo,
                pedido.c.dsc_arvore_unidade_elo,
                pedido.c.num_pedido,
                pedido.c.num_ano,
                pedido.c.dat_emissao,
                pedido.c.dsc_assunto,
                pedido.c.dsc_tematica,
                pedido.c.idn_processo,
                pedido.c.dat_prazo,
                pedido.c.cod_pedido_status,
                pedido_status.c.dsc_pedido_status,
                pedido.c.flg_reg_excluido,
                pedido.c.cif_usuario_inc,
                pedido.c.cif_usuario_alt,
                pedido.c.dat_hor_inclusao,
                pedido.c.dat_hor_alteracao,
            )
            .select_from(
                pedido.outerjoin(pedido_status, pedido_status.c.cod_pedido_status == pedido.c.cod_pedido_status)
            )
            .where(pedido.c.cod_pedido_relacionado == cod_pedido_original)
            .order_by(pedido.c.dat_hor_inclusao.asc())
        )

        rows = self.db.execute(stmt).mappings().all()
        pedidos = [dict(row) for row in rows]
        for pedido_dict in pedidos:
            pedido_dict["analistas"] = self._listar_analistas_por_pedido(pedido_dict["cod_pedido"])
            pedido_dict["unidades_destinatarias"] = self._listar_unidades_destinatarias_por_pedido(pedido_dict["cod_pedido"])
        return pedidos

    def get_pedidos_elegiveis_para_caso(
        self,
        limit: int = 100,
        offset: int = 0,
        cod_caso: int | None = None,
    ) -> List[Dict[str, Any]]:
        from sqlalchemy import extract
        from src.modules.caso.caso.caso_model import CasoModel
        from src.modules.caso.caso_pedido.caso_pedido_model import CasoPedidoModel

        status_aberto = self.db.query(StatusModel).filter(
            StatusModel.dsc_pedido_status.ilike('%aberto%')
        ).first()
        cod_status_aberto = status_aberto.cod_pedido_status if status_aberto else None

        pedido = PedidoModel.__table__

        subq_abertura = select(CasoModel.cod_pedido_abertura)

        condicoes_vinculados = [CasoPedidoModel.flg_reg_excluido == False]
        if cod_caso is not None:
            condicoes_vinculados.append(CasoPedidoModel.cod_caso != cod_caso)

        subq_vinculados = select(CasoPedidoModel.cod_pedido).where(
            and_(*condicoes_vinculados)
        )

        conditions = [
            pedido.c.flg_reg_excluido == False,
            not_(pedido.c.cod_pedido.in_(subq_abertura)),
            not_(pedido.c.cod_pedido.in_(subq_vinculados)),
        ]

        if cod_status_aberto:
            conditions.append(pedido.c.cod_pedido_status == cod_status_aberto)

        stmt = (
            select(
                pedido.c.cod_pedido,
                pedido.c.num_pedido,
                pedido.c.num_ano,
                pedido.c.cod_unidade_analise,
                pedido.c.dsc_assunto,
            )
            .where(and_(*conditions))
            .order_by(pedido.c.num_pedido)
            .limit(limit)
            .offset(offset)
        )

        rows = self.db.execute(stmt).mappings().all()

        return [
            {
                "cod_pedido": row.cod_pedido,
                "display_text": f"{row.num_pedido} / {row.num_ano} / Unidade {row.cod_unidade_analise} – {row.dsc_assunto or ''}"
            }
            for row in rows
        ]

        
    def listar_casos_vinculados_ao_pedido(self, cod_pedido: int) -> list[dict[str, Any]]:
        from src.modules.caso.caso.caso_model import CasoModel

        casos_abertura = (
            self.db.query(CasoModel)
            .filter(
                CasoModel.cod_pedido_abertura == cod_pedido,
                CasoModel.flg_reg_excluido == False,
            )
            .all()
        )

        cod_casos_relacional = self.listar_cod_casos_ativos_por_pedido(cod_pedido)
        casos_relacional = (
            self.db.query(CasoModel)
            .filter(
                CasoModel.cod_caso.in_(cod_casos_relacional),
                CasoModel.flg_reg_excluido == False,
            )
            .all()
            if cod_casos_relacional
            else []
        )

        casos_unicos: dict[int, CasoModel] = {}
        for caso in [*casos_abertura, *casos_relacional]:
            casos_unicos[caso.cod_caso] = caso
        return [{"cod_caso": c.cod_caso} for c in casos_unicos.values()]

    def verificar_vinculos(self, cod_pedido: int) -> dict[str, list[dict[str, Any]]]:
        from src.modules.missao.missao_model import MissaoModel
        from src.modules.operacao.operacao_pedido.operacao_pedido_model import OperacaoPedidoModel
        from src.modules.relatorio.relatorio_model import RelatorioPedidoModel

        vinculos: dict[str, list[dict[str, Any]]] = {}

        casos = self.listar_casos_vinculados_ao_pedido(cod_pedido)
        if casos:
            vinculos["caso"] = casos
        
        missoes = (
            self.db.query(MissaoModel)
            .filter(
                MissaoModel.cod_pedido == cod_pedido,
                MissaoModel.flg_reg_excluido == False,
            )
            .all()
        )
        if missoes:
            vinculos["missao"] = [{"cod_missao": m.cod_missao} for m in missoes]

        operacoes = (
            self.db.query(OperacaoPedidoModel)
            .filter(
                OperacaoPedidoModel.cod_pedido == cod_pedido,
                OperacaoPedidoModel.flg_reg_excluido == False,
            )
            .all()
        )
        if operacoes:
            vinculos["operacao"] = [{"cod_operacao": o.cod_operacao} for o in operacoes]

        relatorios = (
            self.db.query(RelatorioPedidoModel)
            .filter(
                RelatorioPedidoModel.cod_pedido == cod_pedido,
                RelatorioPedidoModel.flg_reg_excluido == False,
            )
            .all()
        )
        if relatorios:
            vinculos["relatorio"] = [{"cod_relatorio": r.cod_relatorio} for r in relatorios]

        return vinculos

    def soft_delete(self, pedido_id: int, justificativa: str | None, cif_usuario: int | None) -> PedidoModel:
        obj = self.db.query(PedidoModel).filter(PedidoModel.cod_pedido == pedido_id).first()
        if not obj:
            raise ValueError(f"Pedido com código {entity_id} não encontrado")
        obj.flg_reg_excluido = True
        if justificativa is not None:
            obj.dsc_justificativa_exclusao = justificativa
        if cif_usuario is not None:
            obj.cif_usuario_alt = cif_usuario
        obj.dat_hor_alteracao = datetime.utcnow()
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
