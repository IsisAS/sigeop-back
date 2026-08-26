"""
Testes do CRUD completo (repository, service, router) usando um model fake.
Garante cobertura dos métodos get, create, update, delete que não são
exercitados pelos módulos que só expõem 'list'.
"""

from fastapi import Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session

from src.common.repository import AbstractRepository
from src.common.router import CrudRouter
from src.common.service import AbstractService
from src.core.deps import get_db
from src.db.base import Base
from src.main import app


# ---------- Model fake ----------
class FakeModel(Base):
    __tablename__ = "fake"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


# ---------- Schemas ----------
class FakeCreateDTO(BaseModel):
    name: str

class FakeUpdateDTO(BaseModel):
    name: str | None = None

class FakeReadDTO(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


# ---------- Repository / Service ----------
class FakeRepository(AbstractRepository[FakeModel, FakeCreateDTO, FakeUpdateDTO]):
    model = FakeModel

class FakeService(AbstractService[FakeModel, FakeCreateDTO, FakeUpdateDTO, FakeReadDTO]):
    read_dto = FakeReadDTO

    def __init__(self, repo: FakeRepository):
        self.repository = repo


# ---------- Router ----------
def get_fake_service(db: Session = Depends(get_db)) -> FakeService:
    return FakeService(FakeRepository(db))

crud = CrudRouter(
    prefix="/fake",
    tags=["Fake"],
    create_dto=FakeCreateDTO,
    update_dto=FakeUpdateDTO,
    read_dto=FakeReadDTO,
    get_service=get_fake_service,
)

app.include_router(crud.router, prefix="/test")


FAKE_URL = "/test/fake"


class TestCrudCreate:
    def test_create_success(self, client: TestClient):
        response = client.post(FAKE_URL, json={"name": "Item 1"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Item 1"
        assert "id" in data

    def test_create_validation_error(self, client: TestClient):
        response = client.post(FAKE_URL, json={})
        assert response.status_code == 422


class TestCrudGet:
    def test_get_success(self, client: TestClient):
        created = client.post(FAKE_URL, json={"name": "Item 2"}).json()
        response = client.get(f"{FAKE_URL}/{created['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == "Item 2"

    def test_get_not_found(self, client: TestClient):
        response = client.get(f"{FAKE_URL}/999")
        assert response.status_code == 404


class TestCrudUpdate:
    def test_update_success(self, client: TestClient):
        created = client.post(FAKE_URL, json={"name": "Old"}).json()
        response = client.put(f"{FAKE_URL}/{created['id']}", json={"name": "New"})
        assert response.status_code == 200
        assert response.json()["name"] == "New"

    def test_update_not_found(self, client: TestClient):
        response = client.put(f"{FAKE_URL}/999", json={"name": "X"})
        assert response.status_code == 404


class TestCrudDelete:
    def test_delete_success(self, client: TestClient):
        created = client.post(FAKE_URL, json={"name": "ToDelete"}).json()
        response = client.delete(f"{FAKE_URL}/{created['id']}")
        assert response.status_code == 204

        response = client.get(f"{FAKE_URL}/{created['id']}")
        assert response.status_code == 404

    def test_delete_not_found(self, client: TestClient):
        response = client.delete(f"{FAKE_URL}/999")
        assert response.status_code == 404


class TestCrudList:
    def test_list_empty(self, client: TestClient):
        response = client.get(FAKE_URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_list_with_data(self, client: TestClient):
        client.post(FAKE_URL, json={"name": "A"})
        client.post(FAKE_URL, json={"name": "B"})
        response = client.get(FAKE_URL)
        assert response.status_code == 200
        assert len(response.json()) == 2
