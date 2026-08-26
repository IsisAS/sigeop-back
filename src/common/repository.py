from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar, Type, Sequence, Any

from sqlalchemy import inspect as sa_inspect, select, delete
from sqlalchemy.orm import Session

from src.core.errors.errors import NotFoundError

ModelT = TypeVar("ModelT")
CreateDTOT = TypeVar("CreateDTOT")
UpdateDTOT = TypeVar("UpdateDTOT")

class AbstractRepository(ABC, Generic[ModelT, CreateDTOT, UpdateDTOT]):
    model: Type[ModelT]

    def __init__(self, db: Session):
        self.db = db

    # ---------- helpers ----------
    def _pk_column(self):
        pk_cols = sa_inspect(self.model).primary_key
        if len(pk_cols) != 1:
            raise NotImplementedError(
                f"{self.model.__name__} tem PK composta ({len(pk_cols)} colunas). "
                "Sobrescreva o método delete() manualmente."
            )
        return pk_cols[0]

    # ---------- CRUD padrão ----------
    def get(self, entity_id: Any) -> ModelT:
        obj = self.db.get(self.model, entity_id)
        if not obj:
            raise NotFoundError(f"{self.model.__name__}({entity_id}) não encontrado.")
        return obj

    def list(self, *, limit: int = 50, offset: int = 0) -> Sequence[ModelT]:
        stmt = select(self.model).limit(limit).offset(offset)
        return self.db.execute(stmt).scalars().all()

    def create(self, dto: CreateDTOT) -> ModelT:
        data = dto.model_dump()
        obj = self.model(**data)  # type: ignore[arg-type]
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, entity_id: Any, dto: UpdateDTOT) -> ModelT:
        obj = self.get(entity_id)
        data = dto.model_dump(exclude_unset=True)

        for k, v in data.items():
            setattr(obj, k, v)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, entity_id: Any) -> None:
        _ = self.get(entity_id)  # garante NotFound
        pk = self._pk_column()
        stmt = delete(self.model).where(pk == entity_id)
        self.db.execute(stmt)
        self.db.commit()
