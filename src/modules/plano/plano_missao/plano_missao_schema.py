from pydantic import model_validator

from src.modules.plano.plano_schema import PlanoCreateDTO, PlanoReadDTO, PlanoUpdateDTO


class PlanoMissaoCreateDTO(PlanoCreateDTO):
    @model_validator(mode="after")
    def validate_cod_missao(self):
        if self.cod_missao is None:
            raise ValueError("cod_missao é obrigatório")
        return self


class PlanoMissaoUpdateDTO(PlanoUpdateDTO):
    @model_validator(mode="after")
    def validate_cod_missao(self):
        if self.cod_missao is None:
            raise ValueError("cod_missao é obrigatório")
        return self


class PlanoMissaoReadDTO(PlanoReadDTO):
    pass
