from datetime import datetime
from typing import Any

from sqlalchemy import select

from src.common.repository import AbstractRepository
from src.modules.papel.papel_model import PapelModel
from src.modules.papel.papel_schema import PapelCreateDTO, PapelUpdateDTO

class PapelRepository(AbstractRepository[PapelModel, PapelCreateDTO, PapelUpdateDTO]):
    model = PapelModel
    
    def list(self, *, limit: int = 50, offset: int = 0):
        stmt = (
            select(self.model)
            .order_by(self.model.flg_ativo.desc(), self.model.dsc_papel.asc(), self.model.cod_papel.asc())
            .limit(limit)
            .offset(offset)
        )
        return self.db.execute(stmt).scalars().all()
    
    def update(self, entity_id: Any, dto: PapelUpdateDTO) -> PapelModel:
        obj = self.get(entity_id)
        data = dto.model_dump(exclude_unset=True)
        
        for key, value in data.items():
            setattr(obj, key, value)
        
        obj.dat_hor_alteracao = datetime.utcnow()
        self.db.commit()
        self.db.refresh(obj)
        return obj