from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.modules.caso.caso_status.caso_status_model import CasoStatusModel
from tests.helpers import CasoStatusFactory

def _seed(db: Session, count: int):
    for i in range(1, count + 1):
        db.add(CasoStatusModel(**CasoStatusFactory.build()))
    db.commit()

class TestListCasoStatus:
    def test_empty(self, client: TestClient):
        response = client.get(CasoStatusFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_with_data(self, db: Session, client: TestClient):
        _seed(db, 3)
        response = client.get(CasoStatusFactory.URL)
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_pagination(self, db: Session, client: TestClient):
        _seed(db, 5)

        response = client.get(f"{CasoStatusFactory.URL}?limit=2&offset=0")
        assert len(response.json()) == 2

        response = client.get(f"{CasoStatusFactory.URL}?limit=2&offset=2")
        assert len(response.json()) == 2
