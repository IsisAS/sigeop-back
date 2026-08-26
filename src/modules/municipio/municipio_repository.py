from typing import List
from sqlalchemy import select
from src.common.repository import AbstractRepository
from src.modules.municipio.municipio_model import MunicipioModel
from src.modules.municipio.municipio_schema import MunicipioUpdateDTO, MunicipioCreateDTO, MunicipioReadDTO

class MunicipioRepository(AbstractRepository[MunicipioModel, MunicipioCreateDTO, MunicipioUpdateDTO]):
    model = MunicipioModel

    def get_by_uf_id(self, cod_uf: int, *, limit: int = 50, offset: int = 0) -> List[MunicipioReadDTO]:
        stmt = select(self.model).where(
            self.model.cod_uf == cod_uf
        )

        return self.db.execute(stmt).scalars().all()