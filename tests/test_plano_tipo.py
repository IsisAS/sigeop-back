from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.modules.plano.plano_tipo.plano_tipo_model import PlanoTipoModel
from tests.helpers import PlanoTipoFactory

def _seed(db: Session, count: int):
    for i in range(1, count + 1):
        db.add(PlanoTipoModel(**PlanoTipoFactory.build()))
    db.commit()

class TestPlanoTipo:
    def test_empty(self, client: TestClient):
        response = client.get(PlanoTipoFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_with_data(self, db: Session, client: TestClient):
        qtd_planos = 3
        _seed(db, qtd_planos)
        response = client.get(PlanoTipoFactory.URL)
        assert response.status_code == 200
        assert len(response.json()) == qtd_planos

    def test_pagination(self, db: Session, client: TestClient):
        _seed(db, 5)

        response = client.get(f"{PlanoTipoFactory.URL}?limit=2&offset=0")
        assert len(response.json()) == 2

        response = client.get(f"{PlanoTipoFactory.URL}?limit=2&offset=2")
        assert len(response.json()) == 2
