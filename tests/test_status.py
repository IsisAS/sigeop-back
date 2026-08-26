from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.modules.pedido.status.status_model import StatusModel
from tests.helpers import StatusFactory


def _seed(db: Session, count: int):
    for i in range(1, count + 1):
        db.add(StatusModel(**StatusFactory.build()))
    db.commit()


class TestListStatus:
    def test_empty(self, client: TestClient):
        response = client.get(StatusFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_with_data(self, db: Session, client: TestClient):
        _seed(db, 3)
        response = client.get(StatusFactory.URL)
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_pagination(self, db: Session, client: TestClient):
        _seed(db, 5)

        response = client.get(f"{StatusFactory.URL}?limit=2&offset=0")
        assert len(response.json()) == 2

        response = client.get(f"{StatusFactory.URL}?limit=2&offset=2")
        assert len(response.json()) == 2
