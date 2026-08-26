from typing import List
from sqlalchemy import select
from src.common.repository import AbstractRepository
from src.modules.demanda.demanda_local.demanda_local_model import DemandaLocalModel
from src.modules.demanda.demanda_local.demanda_local_schema import DemandaLocalUpdateDTO, DemandaLocalCreateDTO, DemandaLocalReadDTO

class DemandaLocalRepository(AbstractRepository[DemandaLocalModel, DemandaLocalCreateDTO, DemandaLocalUpdateDTO]):
    model = DemandaLocalModel

    def list(self, *, limit: int = 50, offset: int = 0) -> list[DemandaLocalModel]:
        stmt = (
            select(self.model)
            .where(self.model.flg_reg_excluido == False)
            .limit(limit)
            .offset(offset)
        )
        return self.db.execute(stmt).scalars().all()

    def get_by_demanda_id(self, cod_demanda) -> List[DemandaLocalReadDTO]:
        stmt = select(self.model).where(
            self.model.cod_demanda == cod_demanda,
            self.model.flg_reg_excluido == False,
        )
        
        return self.db.execute(stmt).scalars().all()