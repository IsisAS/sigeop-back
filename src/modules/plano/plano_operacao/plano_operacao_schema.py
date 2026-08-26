from pydantic import model_validator

from src.modules.plano.plano_schema import PlanoCreateDTO, PlanoReadDTO, PlanoUpdateDTO


class PlanoOperacaoCreateDTO(PlanoCreateDTO):
    @model_validator(mode="after")
    def validate_cod_operacao(self):
        if self.cod_operacao is None:
            raise ValueError("cod_operacao is required")
        return self


class PlanoOperacaoUpdateDTO(PlanoUpdateDTO):
    @model_validator(mode="after")
    def validate_cod_operacao(self):
        if self.cod_operacao is None:
            raise ValueError("cod_operacao is required")
        return self


class PlanoOperacaoReadDTO(PlanoReadDTO):
    pass
