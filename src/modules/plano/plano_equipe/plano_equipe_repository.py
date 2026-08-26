from typing import List
from sqlalchemy import select
from src.common.repository import AbstractRepository
from src.modules.plano.plano_equipe.plano_equipe_model import PlanoEquipeModel
from src.modules.plano.plano_equipe.plano_equipe_schema import PlanoEquipeUpdateDTO, PlanoEquipeCreateDTO, PlanoEquipeReadDTO

class PlanoEquipeRepository(AbstractRepository[PlanoEquipeModel, PlanoEquipeCreateDTO, PlanoEquipeUpdateDTO]):
    model = PlanoEquipeModel

    def get_by_plano_id(self, cod_plano) -> List[PlanoEquipeReadDTO]:
        stmt = select(self.model).where(
            self.model.cod_plano == cod_plano
        )

        return self.db.execute(stmt).scalars().all()
