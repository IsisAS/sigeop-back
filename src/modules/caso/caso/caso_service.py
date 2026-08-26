from typing import List
from src.common.service import AbstractService
from src.core.errors.errors import NotFoundError
from src.modules.caso.caso.caso_model import CasoModel
from src.modules.caso.caso_encarregado.caso_encarregado_model import CasoEncarregadoModel
from src.modules.caso.caso.caso_schema import CasoCreateDTO, CasoUpdateDTO, CasoReadDTO, EncarregadoDto, ListarCasoDto, InformacoesPedidoDto, GridOperacaoDTO, GridMissaoDTO, GridPlanoDTO
from src.modules.caso.caso_encarregado.caso_encarregado_schema import CasoEncarregadoCreateDTO, CasoEncarregadoUpdateDTO, CasoEncarregadoReadDTO
from src.modules.caso.caso_encarregado.caso_encarregado_repository import CasoEncarregadoRepository
from src.modules.caso.caso.caso_repository import CasoRepository
from src.modules.pedido.pedido_schema import PedidoReadDTO
from src.modules.caso.caso_status.caso_status_repository import CasoStatusRepository
from src.modules.pedido.pedido_repository import PedidoRepository

class CasoService(AbstractService[CasoModel, CasoCreateDTO, CasoReadDTO, CasoUpdateDTO]):
    model = CasoModel
    read_dto = CasoReadDTO
    read_encarregado_dto = EncarregadoDto
    read_caso_encarregado_dto = CasoEncarregadoReadDTO

    def __init__(
        self, 
        repository: CasoRepository, 
        caso_encarregado_repository: CasoEncarregadoRepository | None = None,
        caso_status_repository: CasoStatusRepository | None = None,
        pedido_repository: PedidoRepository | None = None,
        ):
        self.repository = repository
        if caso_encarregado_repository is None:
            self.caso_encarregado_repository = CasoEncarregadoRepository(self.repository.db)
        else:
            self.caso_encarregado_repository = caso_encarregado_repository

        if caso_status_repository is None:
            self.caso_status_repository = CasoStatusRepository(self.repository.db)
        else:
            self.caso_status_repository = caso_status_repository
        if pedido_repository is None:
            self.pedido_repository = PedidoRepository(self.repository.db)
        else:
            self.pedido_repository = pedido_repository
        
    def set_repositories(self, caso_encarregado_repository: CasoEncarregadoRepository, caso_status_repository: CasoStatusRepository):
        self.caso_encarregado_repository = caso_encarregado_repository
        self.caso_status_repository = caso_status_repository

    def _obter_dtos_de_model_caso_encarregado(self, casos_encarregados_model: list[CasoEncarregadoModel]) -> list[read_encarregado_dto]:
        encarregados_dto = []
        for caso_encarregado_model in casos_encarregados_model:
            caso_encarregado_dto = self.read_caso_encarregado_dto.model_validate(caso_encarregado_model)
            encarregado = self.read_encarregado_dto(
                cod_caso_encarregado=caso_encarregado_dto.cod_caso_encarregado,
                cod_agente=caso_encarregado_dto.cod_agente,
                nom_agente=getattr(caso_encarregado_model, 'nom_agente', None),
                flg_titular=caso_encarregado_dto.flg_titular,
                dat_inicio=caso_encarregado_dto.dat_inicio,
                flg_reg_excluido=caso_encarregado_dto.flg_reg_excluido
            )
            encarregados_dto.append(self.read_encarregado_dto.model_validate(encarregado))

        return encarregados_dto
    
    def obter_encarregados_por_caso(self, cod_caso: int) -> list[read_encarregado_dto]:
        encarregados_associados_model = self.caso_encarregado_repository.obter_encarregados_associados_a_caso(cod_caso)
        encarregados_associados_dto = self._obter_dtos_de_model_caso_encarregado(encarregados_associados_model)
        return encarregados_associados_dto

    def _with_pedido_unidades_many(self, items) -> list[dict]:
        if not items:
            return items

        enriched: list[dict] = []
        for item in items:
            if hasattr(item, '__dict__'):
                row = item.__dict__.copy()
                row.pop('_sa_instance_state', None)
            else:
                row = dict(item)
                
            row.setdefault("nom_unidade_analise", None)
            row.setdefault("sig_unidade_analise", None)
            row.setdefault("nom_unidade_elo", None)
            row.setdefault("sig_unidade_elo", None)
            enriched.append(row)

        return enriched

    def listar_pedidos_por_caso(self, cod_caso: int) -> List[PedidoReadDTO]:
        caso_model = self.repository.get(cod_caso)
        cod_pedido_abertura = getattr(caso_model, "cod_pedido_abertura", None)
        
        todos = []
        if cod_pedido_abertura:
            principal = self.pedido_repository.get(int(cod_pedido_abertura))
            complementares = self.pedido_repository.list_by_original_id(int(cod_pedido_abertura))
            todos = [principal, *list(complementares or [])]
            
        pedidos_nn = self.repository.listar_pedidos_vinculados_nn(cod_caso)
        todos.extend(pedidos_nn)

        pedidos_unicos = { getattr(p, 'cod_pedido', p.get('cod_pedido') if isinstance(p, dict) else None): p for p in todos }.values()

        for item in pedidos_unicos:
            if isinstance(item, dict):
                item.pop("tematicas", None)

        def sort_key(p):
            dt = p.get("dat_hor_inclusao") if isinstance(p, dict) else getattr(p, "dat_hor_inclusao", None)
            cod = p.get("cod_pedido") if isinstance(p, dict) else getattr(p, "cod_pedido", None)
            return (dt is not None, dt, cod)

        todos_sorted = sorted(pedidos_unicos, key=sort_key, reverse=True)
        enriched = self._with_pedido_unidades_many(todos_sorted)
        return [PedidoReadDTO.model_validate(item) for item in enriched]

    def get(self, entity_id: int) -> read_dto:
        caso_model = self.repository.get(entity_id)
        encarregados_associados_model = self.caso_encarregado_repository.obter_encarregados_associados_a_caso(entity_id)
        encarregados_associados_dto = self._obter_dtos_de_model_caso_encarregado(encarregados_associados_model)
        caso_dto = self.read_dto.from_model(caso_model, encarregados_associados_dto)
        return caso_dto

    def _tratar_encarregados_da_dto(self, dto) -> list:
        encarregados = []
        if hasattr(dto, "encarregados"):
            encarregados.extend(dto.encarregados)
            del dto.encarregados
        return encarregados
    
    def _validar_qtde_encarregados_titular(self, encarregados) -> None:
        indica_apenas_um_titular = sum(encarregado.flg_titular and not encarregado.flg_reg_excluido for encarregado in encarregados) == 1
        if not indica_apenas_um_titular:
            raise ValueError("Para registrar um caso é necessário haver um encarregado cadastrado como titular.")

    def create(self, dto: CasoCreateDTO) -> read_dto:
        encarregados = self._tratar_encarregados_da_dto(dto)
        
        self._validar_qtde_encarregados_titular(encarregados)

        obj_caso_model = self.repository.create(dto)
        caso_dto = self.read_dto.model_validate(obj_caso_model)

        casos_encarregados_dto = []
        cod_caso = caso_dto.cod_caso
        for encarregado in encarregados:
            caso_encarregado_create_dto = CasoEncarregadoCreateDTO(
                 cod_caso= cod_caso,
                 cod_agente= encarregado.cod_agente,
                 flg_titular= encarregado.flg_titular,
                 dat_inicio= encarregado.dat_inicio,
                 flg_reg_excluido= encarregado.flg_reg_excluido,
                 cif_usuario_inc= caso_dto.cif_usuario_inc,
                 cif_usuario_alt= caso_dto.cif_usuario_alt
            )

            casos_encarregados_dto.append(caso_encarregado_create_dto)
        
        self.caso_encarregado_repository.create(casos_encarregados_dto)

        self.repository.db.commit()
        
        caso_dto.encarregados = encarregados
        return caso_dto

    def get_by_pedido_abertura(self, cod_pedido_abertura: int, *, limit: int = 50, offset: int = 0) -> List[CasoReadDTO]:
        """Retorna todos os casos relacionados ao cod_pedido_abertura"""
        casos_model = self.repository.get_by_pedido_abertura(
            cod_pedido_abertura=cod_pedido_abertura,
            limit=limit,
            offset=offset
        )
        casos_dto = []
        for caso_model in casos_model:
            encarregados_associados_model = self.caso_encarregado_repository.obter_encarregados_associados_a_caso(caso_model.cod_caso)
            encarregados_associados_dto = self._obter_dtos_de_model_caso_encarregado(encarregados_associados_model)
            caso_dto = self.read_dto(
                cod_caso=caso_model.cod_caso,
                cod_pedido_abertura=caso_model.cod_pedido_abertura,
                nom_caso=caso_model.nom_caso,
                dsc_caso=caso_model.dsc_caso,
                flg_reg_excluido=caso_model.flg_reg_excluido,
                cif_usuario_inc=caso_model.cif_usuario_inc,
                cif_usuario_alt=caso_model.cif_usuario_alt,
                dat_hor_inclusao=caso_model.dat_hor_inclusao,
                dat_hor_alteracao=caso_model.dat_hor_alteracao,
                cod_caso_status=caso_model.cod_caso_status,
                encarregados=encarregados_associados_dto
            )
            casos_dto.append(caso_dto)
        return casos_dto
    
    def update(self, cod_caso: int, dto: CasoUpdateDTO) -> read_dto:
        encarregados = self._tratar_encarregados_da_dto(dto)

        self._validar_qtde_encarregados_titular(encarregados)
        
        sincronizar_pedidos = "pedidos_vinculados" in dto.model_fields_set
        pedidos_vinculados = (
            dto.pedidos_vinculados
            if sincronizar_pedidos
            else [pedido.cod_pedido for pedido in self.repository.listar_pedidos_vinculados_nn(cod_caso)]
        )
        total_pedidos = 1 + len(pedidos_vinculados) if dto.cod_pedido_abertura else len(pedidos_vinculados)
        if total_pedidos < 1:
            raise ValueError("É obrigatório permanecer pelo menos um Pedido associado ao caso.")
        
        obj_caso_model = self.repository.update(cod_caso, dto)
        
        if sincronizar_pedidos:
            self.repository.sincronizar_pedidos_vinculados(
                cod_caso=cod_caso, 
                pedidos_ids=pedidos_vinculados,
                cif_usuario=dto.cif_usuario_alt
            )

        caso_dto = self.read_dto.from_model(obj_caso_model, encarregados)

        casos_encarregados_dto = []
        cod_caso = caso_dto.cod_caso
        for encarregado in encarregados:
            caso_encarregado_dto = CasoEncarregadoUpdateDTO(
                 cod_caso_encarregado=encarregado.cod_caso_encarregado,
                 cod_caso= cod_caso,
                 cod_agente= encarregado.cod_agente,
                 flg_titular= encarregado.flg_titular,
                 dat_inicio= encarregado.dat_inicio,
                 flg_reg_excluido= encarregado.flg_reg_excluido,
                 cif_usuario_inc= caso_dto.cif_usuario_inc,
                 cif_usuario_alt= caso_dto.cif_usuario_alt
            )

            casos_encarregados_dto.append(caso_encarregado_dto)
        
        encarregados_model = self.caso_encarregado_repository.atualizar_encarregados_associadoas_a_caso(cod_caso, casos_encarregados_dto)
        
        self.repository.db.commit()

        caso_dto.encarregados = self._obter_dtos_de_model_caso_encarregado(encarregados_model)
        return caso_dto
    
    def listar_casos(self, filtro: str | int, limit: int = 50, offset: int = 0) -> List[ListarCasoDto]:
        casos_model = self.repository.listar_com_filtro(
                filtro=filtro,
                limit=limit,
                offset=offset
            )
            
        casos_dto = []
        for caso_model in casos_model:
            qtde_encarregados = (
                self.caso_encarregado_repository
                    .obter_qtde_encarregados_ativos_associados_a_caso(
                     caso_model.cod_caso
                    )
            )
            
            pedido = InformacoesPedidoDto(
                num_pedido=getattr(caso_model.pedido_abertura, 'num_pedido', None),
                num_ano=getattr(caso_model.pedido_abertura, 'num_ano', None),
                dat_prazo=getattr(caso_model.pedido_abertura, 'dat_prazo', None),
                cod_unidade_analise=getattr(caso_model.pedido_abertura, 'cod_unidade_analise', None),
                cod_unidade_elo=getattr(caso_model.pedido_abertura, 'cod_unidade_elo', None)
            )

            caso_dto = ListarCasoDto(
                cod_caso=caso_model.cod_caso,
                cod_pedido_abertura=caso_model.cod_pedido_abertura,
                nom_caso=caso_model.nom_caso,
                dsc_caso=caso_model.dsc_caso,
                flg_reg_excluido=caso_model.flg_reg_excluido,
                cif_usuario_inc=caso_model.cif_usuario_inc,
                cif_usuario_alt=caso_model.cif_usuario_alt,
                dat_hor_inclusao=caso_model.dat_hor_inclusao,
                dat_hor_alteracao=caso_model.dat_hor_alteracao,
                cod_caso_status=caso_model.cod_caso_status,
                pedido=pedido,
                dsc_caso_status=getattr(caso_model.caso_status, 'dsc_caso_status', None),
                qtde_encarregados=qtde_encarregados
            )
            casos_dto.append(caso_dto)
        return casos_dto

    def listar_pedidos_disponiveis(self) -> List[PedidoReadDTO]:
        pedidos_model = self.repository.listar_pedidos_disponiveis()
        enriched = self._with_pedido_unidades_many(pedidos_model)
        return [PedidoReadDTO.model_validate(item) for item in enriched]

    def listar_missoes_por_caso(self, cod_caso: int) -> List[GridMissaoDTO]:
        missoes_model = self.repository.listar_missoes_por_caso(cod_caso)
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

    def listar_planos_por_caso(self, cod_caso: int) -> List[GridPlanoDTO]:
        planos_model = self.repository.listar_planos_por_caso(cod_caso)
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
