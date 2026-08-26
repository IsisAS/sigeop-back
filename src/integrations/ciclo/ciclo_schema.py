from __future__ import annotations
from pydantic import BaseModel


class UnidadeSchema(BaseModel):
    codigo: int
    nome: str
    sigla: str
    nomeFracao: str | None = None
    uf: str | None = None
    nomeEstado: str | None = None
    nomeMunicipio: str | None = None
    unidadeResponsavel: UnidadeSchema | None = None


class ServidorSchema(BaseModel):
    cif: str
    nome: str
    nomeDeGuerra: str | None = None
    unidade: UnidadeSchema | None = None
    ramal: str | None = None
    email: str | None = None
    dataAniversario: str | None = None
    divulgaAniversario: bool | None = None