from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
 
from src.modules.pedido.analista.analista_model import AnalistaModel
from tests.helpers import (
    AnalistaFactory,
    assert_not_found,
    assert_conflict,
    assert_validation_error,
)

def _seed_create_analista_vinculo(db: Session, count: int):
    objects = []
    for _ in range(count):
        obj = AnalistaModel(**AnalistaFactory.build())
        db.add(obj)
    objects.append(obj)

    db.commit()

    for obj in objects:
        db.refresh(obj)
        
    return objects


class TestCreateAnalista:

    def test_empty_body(self, client: TestClient):
        response = client.post(AnalistaFactory.URL, json={})
        assert_validation_error(response, fields=["body.cod_pedido",
                                                  "body.cod_agente",
                                                  "body.flg_titular",
                                                  "body.dat_inicio",
                                                  "body.flg_reg_excluido",
                                                  "body.cif_usuario_inc",
                                                  "body.cif_usuario_alt",])
