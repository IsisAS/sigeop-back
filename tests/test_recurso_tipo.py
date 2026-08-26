from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from tests.helpers import (
    RecursoTipoFactory,
    assert_validation_error
)
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel

def _seed(db: Session, count: int):
    for i in range(1, count + 1):
        db.add(RecursoTipoModel(**RecursoTipoFactory.build()))
    db.commit()

class TesteListarRecursoTipo:
    def test_empty(self, client: TestClient):
        response = client.get(RecursoTipoFactory.URL)
        assert response.status_code == 200
        assert response.json() == []
    
    def test_deve_listar_recurso_tipo(self, db: Session, client: TestClient):
        payload = RecursoTipoFactory.build(
            sig_recurso_tipo="Operacao",
            dsc_recurso_tipo="Teste"
        )

        client.post(RecursoTipoFactory.URL, json=payload)
        response = client.get(RecursoTipoFactory.URL)
        assert response.status_code == 200