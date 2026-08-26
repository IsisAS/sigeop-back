from pydantic import model_validator

from src.modules.plano.plano_schema import PlanoCreateDTO, PlanoReadDTO, PlanoUpdateDTO


class PlanoCasoCreateDTO(PlanoCreateDTO):
    @model_validator(mode="after")
    def validate_cod_caso(self):
        if self.cod_caso is None:
            raise ValueError("cod_caso is required")
        return self


class PlanoCasoUpdateDTO(PlanoUpdateDTO):
    @model_validator(mode="after")
    def validate_cod_caso(self):
        if self.cod_caso is None:
            raise ValueError("cod_caso is required")
        return self


class PlanoCasoReadDTO(PlanoReadDTO):
    pass