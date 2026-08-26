from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.modules.operacao.operacao_status.operacao_status_model import OperacaoStatusModel
from tests.helpers import OperacaoStatusFactory

def _seed(db: Session, count: int):
    for i in range(1, count + 1):
        db.add(OperacaoStatusModel(**OperacaoStatusFactory.build()))
    db.commit()

class TestListOperacaoStatus:
    def test_empty(self, client: TestClient):
        response = client.get(OperacaoStatusFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def buscar_operacoes(self, client: TestClient):
        response = client.get(OperacaoStatusFactory.URL)
        assert response.status_code == 200