from src.common.service import AbstractService
from src.modules.missao.missao_model import MissaoModel
from src.modules.missao.missao_repository import MissaoRepository
from src.modules.missao.missao_schema import (
    MissaoCreateDTO,
    MissaoReadDTO,
    MissaoUpdateDTO,
    MissaoEncarregadoCreateDTO,
    MissaoEncarregadoReadDTO,
    MissaoFonteHumanaDTO
)
from typing import List 

class MissaoService(AbstractService[MissaoModel, MissaoCreateDTO, MissaoReadDTO, MissaoUpdateDTO]):
    read_dto = MissaoReadDTO

    def __init__(self, repository: MissaoRepository):
        self.repository = repository

    def _montar_leitura(self, item) -> MissaoReadDTO:
        if isinstance(item, dict):
            encarregados = [
                MissaoEncarregadoReadDTO.model_validate(e, from_attributes=True)
                for e in item.get("encarregados", [])
                if not (e.get("flg_reg_excluido", False) if isinstance(e, dict) else e.flg_reg_excluido)
            ]

            fontes_humanas = [
                MissaoFonteHumanaDTO.model_validate(f, from_attributes=True)
                for f in item.get("fontes_humanas", [])
                if not (f.get("flg_reg_excluido", False) if isinstance(f, dict) else f.flg_reg_excluido)
            ]
            item_data = {k: v for k, v in item.items() if k not in ("encarregados", "fontes_humanas", "nom_encarregado_titular")}
            return self.read_dto(
                **item_data,
                encarregados=encarregados,
                fontes_humanas=fontes_humanas,
                encarregados_quantidade=len(encarregados),
            )
        return self.read_dto.from_model(item)

    def list_por_caso(self, *, cod_caso: int) -> list[MissaoReadDTO]:
        items = self.repository.list_por_caso(cod_caso=cod_caso)
        return [self._montar_leitura(item) for item in items]

    def list(self, *, limit: int = 50, offset: int = 0) -> list[MissaoReadDTO]:
        items = self.repository.list(limit=limit, offset=offset) 
        return [self._montar_leitura(item) for item in items]
    
    def list_por_tipo(
        self,
        *,
        cod_missao_tipo: int,
        cod_recurso_tipo: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[MissaoReadDTO]:
        items = self.repository.list_por_tipo(
            cod_missao_tipo=cod_missao_tipo,
            cod_recurso_tipo=cod_recurso_tipo,
            limit=limit,
            offset=offset,
        )
        return [self._montar_leitura(item) for item in items]

    def soft_delete(self, entity_id: int, *, justificativa: str, cif_usuario_alt: int) -> None:
        self.repository.soft_delete(
            entity_id,
            justificativa=justificativa,
            cif_usuario_alt=cif_usuario_alt,
        )

    def get(self, entity_id: int) -> MissaoReadDTO:
        missao_model = self.repository.get(entity_id)
        return self._montar_leitura(missao_model)

    def create(self, obj_in: MissaoCreateDTO) -> MissaoReadDTO:
        missao_dict = self.repository.create(obj_in)
        return self._montar_leitura(missao_dict)

    def update(self, entity_id: int, obj_in: MissaoUpdateDTO) -> MissaoReadDTO:
        self.repository.update(entity_id, obj_in)
        self.repository.db.expire_all()
        model = self.repository.db.query(MissaoModel).filter(
            MissaoModel.cod_missao == entity_id
        ).first()
        return self.read_dto.from_model(model)