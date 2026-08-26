from typing import List
from sqlalchemy import select
from src.common.repository import AbstractRepository
from src.modules.uf.uf_model import UfModel
from src.modules.uf.uf_schema import UfUpdateDTO, UfCreateDTO, UfReadDTO

class UfRepository(AbstractRepository[UfModel, UfCreateDTO, UfUpdateDTO]):
    model = UfModel

    def get_by_pais_id(self, cod_pais: int, *, limit: int = 50, offset: int = 0) -> List[UfReadDTO]:
        stmt = select(self.model).where(
            self.model.cod_pais == cod_pais
        )

        return self.db.execute(stmt).scalars().all()
