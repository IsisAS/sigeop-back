from typing import List
from sqlalchemy import select, distinct
from src.common.repository import AbstractRepository
from src.modules.plano.plano_local.plano_local_model import PlanoLocalModel
from src.modules.plano.plano_local.plano_local_schema import PlanoLocalUpdateDTO, PlanoLocalCreateDTO, PlanoLocalReadDTO

class PlanoLocalRepository(AbstractRepository[PlanoLocalModel, PlanoLocalCreateDTO, PlanoLocalUpdateDTO]):
    model = PlanoLocalModel

    def get_by_plano_id(self, cod_plano) -> List[PlanoLocalReadDTO]:
        stmt = select(self.model).where(
            self.model.cod_plano == cod_plano
        )
        
        return self.db.execute(stmt).scalars().all()
    
    def get_descricoes(
        self, 
        cod_pais: int, 
        cod_uf: int | None = None, 
        cod_municipio: int | None = None,
    ) -> List[str]:
        stmt = (
            select(distinct(self.model.dsc_local))
            .where(
                self.model.cod_pais == cod_pais,
                self.model.dsc_local.isnot(None),
                self.model.dsc_local != "",
                self.model.flg_reg_excluido.is_(False)
            )
            .order_by(self.model.dsc_local)
        )
        if cod_uf is not None:
            stmt = stmt.where(self.model.cod_uf == cod_uf)
        if cod_municipio is not None:
            stmt = stmt.where(self.model.cod_municipio == cod_municipio)
            
        return [row for row in self.db.execute(stmt).scalars().all()]