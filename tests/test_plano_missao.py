from itertools import count

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.missao.missao_model import MissaoModel
from src.modules.missao.missao_status.missao_status_model import MissaoStatusModel
from src.modules.missao.missao_tipo.missao_tipo_model import MissaoTipoModel
from src.modules.plano.plano_local.plano_local_model import PlanoLocalModel
from src.modules.plano.plano_missao.plano_missao_model import PlanoMissaoModel
from src.modules.plano.plano_status.plano_status_model import PlanoStatusModel
from src.modules.plano.plano_tipo.plano_tipo_model import PlanoTipoModel
from tests.helpers import (
    MissaoFactory,
    MissaoStatusFactory,
    MissaoTipoFactory,
    PlanoMissaoFactory,
    PlanoStatusFactory,
    PlanoTipoFactory,
    assert_not_found,
    assert_validation_error,
)

_payload_counter = count(1)
_local_counter = count(1)


def _persist(db: Session, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def _seed_plano_tipo(db: Session, **overrides) -> PlanoTipoModel:
    return _persist(db, PlanoTipoModel(**PlanoTipoFactory.build(**overrides)))


def _seed_plano_status(db: Session, **overrides) -> PlanoStatusModel:
    return _persist(db, PlanoStatusModel(**PlanoStatusFactory.build(**overrides)))


def _seed_missao_tipo(db: Session, **overrides) -> MissaoTipoModel:
    return _persist(db, MissaoTipoModel(**MissaoTipoFactory.build(**overrides)))


def _seed_missao_status(db: Session, **overrides) -> MissaoStatusModel:
    return _persist(db, MissaoStatusModel(**MissaoStatusFactory.build(**overrides)))


def _seed_missao(db: Session, **overrides) -> MissaoModel:
    payload = MissaoFactory.build(encarregados=[], fontes_humanas=[], **overrides)
    return _persist(db, MissaoModel(**payload))


def _build_local_payload(**overrides) -> dict:
    n = next(_local_counter)
    payload = {
        "cod_pais": n,
        "cod_uf": n,
        "cod_municipio": n,
        "dsc_local": f"Local da missao {n}",
        "flg_reg_excluido": False,
        "cif_usuario_inc": 1,
        "cif_usuario_alt": 1,
    }
    payload.update(overrides)
    return payload


def _build_plano_missao_payload(
    *,
    cod_plano_tipo: int,
    cod_plano_status: int,
    cod_missao: int,
    **overrides,
) -> dict:
    n = next(_payload_counter)
    payload = PlanoMissaoFactory.build(
        cod_plano_tipo=cod_plano_tipo,
        cod_plano_status=cod_plano_status,
        cod_missao=cod_missao,
        cod_unidade=n,
        num_plano=f"PLANO-MISSAO-{n}",
        dsc_assunto=f"Assunto do plano missao {n}",
        local=[_build_local_payload()],
    )
    payload.update(overrides)
    return payload


def _prepare_dependencies(db: Session, *, cod_missao: int = 1):
    plano_tipo = _seed_plano_tipo(db)
    plano_status = _seed_plano_status(db)
    missao_tipo = _seed_missao_tipo(db)
    missao_status = _seed_missao_status(db)
    missao = _seed_missao(
        db,
        cod_missao=cod_missao,
        cod_missao_tipo=missao_tipo.cod_missao_tipo,
        cod_missao_status=missao_status.cod_missao_status,
    )
    return plano_tipo, plano_status, missao


def _as_json(payload: dict) -> dict:
    return jsonable_encoder(payload)


class TestCreatePlanoMissao:
    def test_success(self, db: Session, client: TestClient):
        plano_tipo, plano_status, missao = _prepare_dependencies(db)
        payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=missao.cod_missao,
        )

        response = client.post(PlanoMissaoFactory.URL, json=_as_json(payload))

        assert response.status_code == 200
        data = response.json()
        assert data["cod_missao"] == missao.cod_missao
        assert data["num_plano"] == payload["num_plano"]
        assert len(data["local"]) == 1
        assert data["local"][0]["dsc_local"] == payload["local"][0]["dsc_local"]

    def test_empty_body(self, client: TestClient):
        response = client.post(PlanoMissaoFactory.URL, json={})

        assert_validation_error(
            response,
            fields=[
                "body.cod_plano_tipo",
                "body.cod_plano_status",
                "body.num_plano",
                "body.num_ano",
                "body.dat_emissao",
                "body.dat_inicio",
                "body.dat_termino",
                "body.flg_reg_excluido",
                "body.cif_usuario_inc",
                "body.cif_usuario_alt",
                "body.plano_equipe",
                "body.local",
            ],
        )

    def test_cod_missao_obrigatorio(self, db: Session, client: TestClient):
        plano_tipo, plano_status, missao = _prepare_dependencies(db)
        payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=missao.cod_missao,
        )
        payload.pop("cod_missao")

        response = client.post(PlanoMissaoFactory.URL, json=_as_json(payload))

        assert_validation_error(response)
        data = response.json()
        assert any("cod_missao" in error["message"] for error in data["errors"])


class TestGetPlanoMissao:
    def test_get_by_id_success(self, db: Session, client: TestClient):
        plano_tipo, plano_status, missao = _prepare_dependencies(db)
        payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=missao.cod_missao,
        )
        created = client.post(PlanoMissaoFactory.URL, json=_as_json(payload)).json()

        response = client.get(f"{PlanoMissaoFactory.URL}/{created['cod_plano']}")

        assert response.status_code == 200
        data = response.json()
        assert data["cod_plano"] == created["cod_plano"]
        assert data["cod_missao"] == missao.cod_missao

    def test_get_by_id_not_found(self, client: TestClient):
        response = client.get(f"{PlanoMissaoFactory.URL}/999999")

        assert_not_found(response)


class TestListPlanoMissao:
    def test_list_by_missao_success(self, db: Session, client: TestClient):
        plano_tipo, plano_status, missao = _prepare_dependencies(db, cod_missao=10)
        _, _, outra_missao = _prepare_dependencies(db, cod_missao=20)

        primeiro_payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=missao.cod_missao,
        )
        segundo_payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=missao.cod_missao,
        )
        outro_payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=outra_missao.cod_missao,
        )

        primeiro = client.post(PlanoMissaoFactory.URL, json=_as_json(primeiro_payload)).json()
        segundo = client.post(PlanoMissaoFactory.URL, json=_as_json(segundo_payload)).json()
        client.post(PlanoMissaoFactory.URL, json=_as_json(outro_payload))

        response = client.get(f"{PlanoMissaoFactory.URL}/missao/{missao.cod_missao}")

        assert response.status_code == 200
        data = response.json()
        assert [item["cod_plano"] for item in data] == [
            segundo["cod_plano"],
            primeiro["cod_plano"],
        ]
        assert all(item["cod_missao"] == missao.cod_missao for item in data)


class TestUpdatePlanoMissao:
    def test_update_success_sincroniza_missao_e_locais(self, db: Session, client: TestClient):
        plano_tipo, plano_status, missao = _prepare_dependencies(db, cod_missao=30)
        _, _, nova_missao = _prepare_dependencies(db, cod_missao=40)

        payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=missao.cod_missao,
            local=[
                _build_local_payload(dsc_local="Local original 1"),
                _build_local_payload(dsc_local="Local original 2"),
            ],
        )
        created = client.post(PlanoMissaoFactory.URL, json=_as_json(payload)).json()
        local_existente = created["local"][0]

        update_payload = _build_plano_missao_payload(
            cod_plano_tipo=plano_tipo.cod_plano_tipo,
            cod_plano_status=plano_status.cod_plano_status,
            cod_missao=nova_missao.cod_missao,
            num_plano=f"{payload['num_plano']}-ATUALIZADO",
            local=[
                {
                    **local_existente,
                    "dsc_local": "Local atualizado",
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1,
                }
            ],
        )

        response = client.put(
            f"{PlanoMissaoFactory.URL}/{created['cod_plano']}",
            json=_as_json(update_payload),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["cod_missao"] == nova_missao.cod_missao
        assert data["num_plano"] == update_payload["num_plano"]
        assert len(data["local"]) == 1
        assert data["local"][0]["dsc_local"] == "Local atualizado"

        vinculo = db.execute(
            select(PlanoMissaoModel).where(PlanoMissaoModel.cod_plano == created["cod_plano"])
        ).scalar_one()
        locais = db.execute(
            select(PlanoLocalModel).where(PlanoLocalModel.cod_plano == created["cod_plano"])
        ).scalars().all()

        assert vinculo.cod_missao == nova_missao.cod_missao
        assert len(locais) == 1
        assert locais[0].dsc_local == "Local atualizado"
