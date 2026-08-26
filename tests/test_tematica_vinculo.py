from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
 
from src.modules.pedido.tematica_vinculo.tematica_vinculo_model import TematicaVinculoModel
from tests.helpers import (
    TematicaVinculoFactory,
    assert_not_found,
    assert_conflict,
    assert_validation_error,
)

def _seed_create_tematica_vinculo(db: Session, count: int):
    objects = []
    for _ in range(count):
        obj = TematicaVinculoModel(**TematicaVinculoFactory.build())
        db.add(obj)
    objects.append(obj)

    db.commit()

    for obj in objects:
        db.refresh(obj)
        
    return objects


class TestCreateTematicaVinculo:

    def test_empty_body(self, client: TestClient):
        response = client.post(TematicaVinculoFactory.URL, json={})
        assert_validation_error(response, fields=["body.flg_reg_excluido",
                                                  "body.cif_usuario_inc",
                                                  "body.cif_usuario_alt"])
