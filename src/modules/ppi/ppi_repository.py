from src.common.repository import AbstractRepository
from typing import Any
from src.modules.ppi.ppi_model import PPIModel
from src.modules.ppi.ppi_schema import PPIUpdateDTO, PPICreateDTO

class PPIRepository(AbstractRepository[PPIModel, PPICreateDTO, PPIUpdateDTO]):
    model = PPIModel

    def alterar_status_ppi(self, cod_ppi: str, status:bool) -> PPIModel:
        ppi = (
            self.db.query(self.model)
            .filter(
                self.model.cod_ppi == cod_ppi
            ).first()
        )

        if not ppi:
            return None
        
        ppi.flg_ativo = status
        self.db.flush()

        return ppi