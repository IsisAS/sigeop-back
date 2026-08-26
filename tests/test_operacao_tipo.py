from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.modules.operacao.operacao_tipo.operacao_tipo_model import OperacaoTipoModel
from tests.helpers import OperacaoTipoFactory

def _seed(db: Session, count: int):
    for i in range(1, count + 1):
        db.add(OperacaoTipoModel(**OperacaoTipoFactory.build()))
    db.commit()

class TestListOperacaoTipo:
    def test_empty(self, client: TestClient):
        response = client.get(OperacaoTipoFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def buscar_operacoes(self, client: TestClient):
        response = client.get(OperacaoTipoFactory.URL)
        assert response.status_code == 200