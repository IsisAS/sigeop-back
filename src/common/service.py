from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar, Sequence, Any, Type

from src.common.repository import AbstractRepository

ModelT = TypeVar("ModelT")
CreateDTOT = TypeVar("CreateDTOT")
UpdateDTOT = TypeVar("UpdateDTOT")
ReadDTOT = TypeVar("ReadDTOT")

class AbstractService(ABC, Generic[ModelT, CreateDTOT, UpdateDTOT, ReadDTOT]):
    """
    Service base: encapsula o CRUD e converte para DTO de leitura.
    Você só precisa:
      - declarar repository
      - declarar read_dto
    """
    repository: AbstractRepository[ModelT, CreateDTOT, UpdateDTOT]
    read_dto: Type[ReadDTOT]

    def list(self, *, limit: int = 50, offset: int = 0) -> Sequence[ReadDTOT]:
        items = self.repository.list(limit=limit, offset=offset)
        return [self.read_dto.model_validate(x) for x in items]  # type: ignore[attr-defined]

    def get(self, entity_id: Any) -> ReadDTOT:
        obj = self.repository.get(entity_id)
        return self.read_dto.model_validate(obj)  # type: ignore[attr-defined]

    def create(self, dto: CreateDTOT) -> ReadDTOT:
        obj = self.repository.create(dto)
        return self.read_dto.model_validate(obj)  # type: ignore[attr-defined]

    def update(self, entity_id: Any, dto: UpdateDTOT) -> ReadDTOT:
        obj = self.repository.update(entity_id, dto)
        return self.read_dto.model_validate(obj)  # type: ignore[attr-defined]

    def delete(self, entity_id: Any) -> None:
        self.repository.delete(entity_id)
