import pytest
from pydantic import BaseModel

from src.common.router import CrudRouter


class FakeReadDTO(BaseModel):
    id: int


class FakeCreateDTO(BaseModel):
    name: str


class FakeUpdateDTO(BaseModel):
    name: str


def fake_service(db):
    pass


class TestCrudRouterOperations:
    def test_operations_and_exclude_raises(self):
        with pytest.raises(ValueError, match="operations.*exclude"):
            CrudRouter(
                prefix="/x",
                tags=["X"],
                read_dto=FakeReadDTO,
                create_dto=FakeCreateDTO,
                update_dto=FakeUpdateDTO,
                get_service=fake_service,
                operations={"list"},
                exclude={"delete"},
            )

    def test_operations_selects_only_given(self):
        crud = CrudRouter(
            prefix="/x",
            tags=["X"],
            read_dto=FakeReadDTO,
            get_service=fake_service,
            operations={"list", "get"},
        )
        paths = [r.path for r in crud.router.routes]
        assert "/x" in paths
        assert "/x/{id}" in paths
        assert len(crud.router.routes) == 2

    def test_exclude_removes_given(self):
        crud = CrudRouter(
            prefix="/x",
            tags=["X"],
            read_dto=FakeReadDTO,
            create_dto=FakeCreateDTO,
            update_dto=FakeUpdateDTO,
            get_service=fake_service,
            exclude={"delete"},
        )
        methods = []
        for r in crud.router.routes:
            methods.extend(r.methods)
        assert "DELETE" not in methods

    def test_create_without_dto_raises(self):
        with pytest.raises(ValueError, match="create_dto"):
            CrudRouter(
                prefix="/x",
                tags=["X"],
                read_dto=FakeReadDTO,
                get_service=fake_service,
                operations={"create"},
            )

    def test_update_without_dto_raises(self):
        with pytest.raises(ValueError, match="update_dto"):
            CrudRouter(
                prefix="/x",
                tags=["X"],
                read_dto=FakeReadDTO,
                get_service=fake_service,
                operations={"update"},
            )
