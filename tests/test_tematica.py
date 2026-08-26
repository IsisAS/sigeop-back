from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.modules.pedido.tematica.tematica_model import TematicaModel
from tests.helpers import (
    TematicaFactory,
    assert_not_found
)

def _seed(db: Session, count: int):
    for i in range(1, count + 1):
        db.add(TematicaModel(**TematicaFactory.build()))
    db.commit()

def _seed_update(db: Session, count: int):
    objects = []
    for _ in range(count):
        obj = TematicaModel(**TematicaFactory.build())
        db.add(obj)
        objects.append(obj)

    db.commit()

    for obj in objects:
        db.refresh(obj)

    return objects


class TestListTematica:
    def test_empty(self, client: TestClient):
        response = client.get(TematicaFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_with_data(self, db: Session, client: TestClient):
        _seed(db, 3)
        response = client.get(TematicaFactory.URL)
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_pagination(self, db: Session, client: TestClient):
        _seed(db, 5)

        response = client.get(f"{TematicaFactory.URL}?limit=2&offset=0")
        assert len(response.json()) == 2

        response = client.get(f"{TematicaFactory.URL}?limit=2&offset=2")
        assert len(response.json()) == 2


class TestUpdateStatusTematica:
    def test_success_ativar(self, db: Session, client: TestClient):
        objs = _seed_update(db, 1)
        teste = objs[0]
        payload = {
            "nom_tematica": teste.nom_tematica,
            "flg_ativo": True,
            "cif_usuario_inc": teste.cif_usuario_inc,
            "cif_usuario_alt": teste.cif_usuario_alt
        }
        response = client.put(f"{TematicaFactory.URL}/{teste.cod_tematica}", json=payload)
        assert response.status_code == 200
        assert response.json()["flg_ativo"] is True

    def test_success_inativar(self, db: Session, client: TestClient):
        objs = _seed_update(db, 1)
        teste = objs[0]
        payload = {
            "nom_tematica": teste.nom_tematica,
            "flg_ativo": False,
            "cif_usuario_inc": teste.cif_usuario_inc,
            "cif_usuario_alt": teste.cif_usuario_alt
        }
        response = client.put(f"{TematicaFactory.URL}/{teste.cod_tematica}", json=payload)
        assert response.status_code == 200
        assert response.json()["flg_ativo"] is False

    def test_not_found(self, db: Session, client: TestClient):
        _seed(db, 1)
        print(db.query(TematicaModel).all())
        payload = {
            "nom_tematica": "tematica 1",
            "flg_ativo": True,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1
        }
        response = client.put(f"{TematicaFactory.URL}/999", json=payload)
        assert_not_found(response)

