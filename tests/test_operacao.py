from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder

from src.modules.operacao.operacao_model import OperacaoModel
from src.modules.operacao.operacao_tipo.operacao_tipo_model import OperacaoTipoModel
from src.modules.operacao.operacao_status.operacao_status_model import OperacaoStatusModel
from src.modules.operacao.operacao_encarregado.operacao_encarregado_model import OperacaoEncarregadoModel
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel
from src.modules.caso.caso.caso_model import CasoModel
from src.modules.agente.agente_model import AgenteModel

from tests.helpers import (
    OperacaoTipoFactory,
    OperacaoStatusFactory,
    OperacaoFactory,
    RecursoTipoFactory,
    CasoFactory,
    AgenteFactory,
    assert_validation_error,
    assert_not_found
)

def _seed_generic(db: Session, factory, model_class, count: int, **overrides):
    objects = []
    for _ in range(count):
        obj = model_class(**factory.build(**overrides))
        db.add(obj)
        objects.append(obj)
    db.commit()
    for obj in objects:
        db.refresh(obj)
    return objects

class TestCreateOperacao:
    def test_empty_body(self, client: TestClient):
        response = client.post(OperacaoFactory.URL, json={})
        assert_validation_error(
            response,
            fields=[
                "body.cod_operacao_tipo",
                "body.cod_operacao_status",
                "body.nom_operacao",
                "body.encarregados", 
            ]
        )
    
    def test_success(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 1, sig_operacao_tipo="COORDENADA")[0]
        status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 1, sig_operacao_status="EM_PLANEJAMENTO")[0]
        caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        agente = _seed_generic(db, AgenteFactory, AgenteModel, 1)[0]
        recurso_tipo = _seed_generic (db, RecursoTipoFactory, RecursoTipoModel, 1)[0]

        payload = OperacaoFactory.build(
            cod_operacao_tipo=tipo.cod_operacao_tipo,
            cod_operacao_status=status.cod_operacao_status,
            cod_recurso_tipo = recurso_tipo.cod_recurso_tipo,
            cod_caso=caso.cod_caso,
            encarregados=[
                {
                    "cod_agente": agente.cod_agente,
                    "flg_titular": True,
                    "dat_inicio": datetime.now(timezone.utc).isoformat(),
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1
                }
            ]
        )

        response = client.post(OperacaoFactory.URL, json=jsonable_encoder(payload))
        assert response.status_code == 201
        data = response.json()
        assert "encarregados" in data
      
    def test_deve_retornar_error_quando_nome_duplicado(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 1, sig_operacao_tipo="COORDENADA")[0]
        status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 1, sig_operacao_status="EM_PLANEJAMENTO")[0]
        caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        agente = _seed_generic(db, AgenteFactory, AgenteModel, 1)[0]

        payload = OperacaoFactory.build(
            cod_operacao_tipo=tipo.cod_operacao_tipo,
            cod_operacao_status=status.cod_operacao_status,
            cod_caso=caso.cod_caso,
            nom_operacao="Operação Duplicada",
            encarregados=[
                {
                    "cod_agente": agente.cod_agente,
                    "flg_titular": True,
                    "dat_inicio": datetime.now(timezone.utc).isoformat(),
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1
                }
            ]
        )
        
        client.post(OperacaoFactory.URL, json=jsonable_encoder(payload))
        duplicate_response = client.post(OperacaoFactory.URL, json=jsonable_encoder(payload))
        assert duplicate_response.status_code == 409
    
    def test_error_encarregados_vazio(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 1)[0]
        status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 1)[0]
        caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]

        payload = OperacaoFactory.build(
            cod_operacao_tipo=tipo.cod_operacao_tipo,
            cod_operacao_status=status.cod_operacao_status,
            cod_caso=caso.cod_caso,
            encarregados=[]
        )
        response = client.post(OperacaoFactory.URL, json=jsonable_encoder(payload))
        assert response.status_code == 500

    def test_error_n_encarregados_titulares(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 1)[0]
        status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 1)[0]
        caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        agentes = _seed_generic(db, AgenteFactory, AgenteModel, 2)

        payload = OperacaoFactory.build(
            cod_operacao_tipo=tipo.cod_operacao_tipo,
            cod_operacao_status=status.cod_operacao_status,
            cod_caso=caso.cod_caso,
            encarregados=[
                {
                    "cod_agente": agentes[0].cod_agente,
                    "flg_titular": True,
                    "dat_inicio": datetime.now(timezone.utc).isoformat(),
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1
                },
                {
                    "cod_agente": agentes[1].cod_agente,
                    "flg_titular": True,
                    "dat_inicio": datetime.now(timezone.utc).isoformat(),
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1
                }   
            ]
        )
        
        response = client.post(OperacaoFactory.URL, json=jsonable_encoder(payload))
        assert response.status_code == 500

    def test_error_nenhum_encarregado_titular(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 1)[0]
        status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 1)[0]
        caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        agentes = _seed_generic(db, AgenteFactory, AgenteModel, 2)

        payload = OperacaoFactory.build(
            cod_operacao_tipo=tipo.cod_operacao_tipo,
            cod_operacao_status=status.cod_operacao_status,
            cod_caso=caso.cod_caso,
            encarregados=[
                {
                    "cod_agente": agentes[0].cod_agente,
                    "flg_titular": False,
                    "dat_inicio": datetime.now(timezone.utc).isoformat(),
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1
                },
                {
                    "cod_agente": agentes[1].cod_agente,
                    "flg_titular": False,
                    "dat_inicio": datetime.now(timezone.utc).isoformat(),
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1
                }   
            ]
        )

        response = client.post(OperacaoFactory.URL, json=jsonable_encoder(payload))
        assert response.status_code == 500

class TestGetByIdOperacao:
    def test_get_success(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 1, dsc_operacao_tipo="Coordenada")[0]
        status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 1, dsc_operacao_status="Em planejamento")[0]
        caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        agente = _seed_generic(db, AgenteFactory, AgenteModel, 1)[0]

        data_mock = OperacaoFactory.build(
            cod_operacao_tipo=tipo.cod_operacao_tipo,
            cod_operacao_status=status.cod_operacao_status,
            cod_caso=caso.cod_caso
        )
        data_mock.pop("encarregados", None) 
        
        operacao_mock = OperacaoModel(**data_mock)
        db.add(operacao_mock)
        db.flush()

        encarregado = OperacaoEncarregadoModel(
            cod_operacao=operacao_mock.cod_operacao,
            cod_agente=agente.cod_agente,
            flg_titular=True,
            dat_inicio=datetime.now(timezone.utc),
            cif_usuario_inc=1,
            cif_usuario_alt=1,
            flg_reg_excluido=False
        )
        db.add(encarregado)
        db.commit()

        response = client.get(f"{OperacaoFactory.URL}/{operacao_mock.cod_operacao}")

        assert response.status_code == 200
        data = response.json()
        assert data["dsc_operacao_tipo"] == "Coordenada"
        assert data["dsc_operacao_status"] == "Em planejamento"
        assert len(data["encarregados"]) > 0
        assert data["encarregados"][0]["flg_titular"] is True

    def test_get_by_id_not_found(self, client: TestClient):
        response = client.get(f"{OperacaoFactory.URL}/999999")
        assert_not_found(response)

class TestUpdateOperacao:
    def test_update_success(self, db: Session, client: TestClient):
        tipos = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 2)
        status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 2)
        caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        agentes = _seed_generic(db, AgenteFactory, AgenteModel, 2)
        
        payload_create = OperacaoFactory.build(
            cod_operacao_tipo=tipos[0].cod_operacao_tipo,
            cod_operacao_status=status[0].cod_operacao_status,
            cod_caso=caso.cod_caso,
            nom_operacao="Operação Inicial",
            encarregados=[{
                "cod_agente": agentes[0].cod_agente, 
                "flg_titular": True, 
                "dat_inicio": datetime.now(timezone.utc).isoformat(), 
                "flg_reg_excluido": False,
                "cif_usuario_inc": 1,
                "cif_usuario_alt": 1
            }]
        )

        response_create = client.post(OperacaoFactory.URL, json=jsonable_encoder(payload_create))
        assert response_create.status_code == 201
        operacao_id = response_create.json()["cod_operacao"]

        payload_update = OperacaoFactory.build(
            cod_operacao_tipo=tipos[1].cod_operacao_tipo,
            cod_operacao_status=status[1].cod_operacao_status,
            cod_caso=caso.cod_caso,
            nom_operacao="Operação Atualizada",
            encarregados=[
                {
                    "cod_agente": agentes[1].cod_agente, 
                    "flg_titular": True, 
                    "dat_inicio": datetime.now(timezone.utc).isoformat(), 
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1
                }
            ]
        )

        response_update = client.put(f"{OperacaoFactory.URL}/{operacao_id}", json=jsonable_encoder(payload_update))
        
        assert response_update.status_code == 200
        data = response_update.json()
        assert data["nom_operacao"] == "Operação Atualizada"
        assert data["cod_operacao_tipo"] == tipos[1].cod_operacao_tipo
        assert any(e["cod_agente"] == agentes[1].cod_agente and e["flg_titular"] for e in data["encarregados"])

    def test_update_not_found(self, client: TestClient):
        payload = {"nom_operacao": "teste"}
        response = client.put(f"{OperacaoFactory.URL}/99999", json=payload)
        assert response.status_code in [404, 422]

class TesteListarOperacao:
    def test_deve_listar_operacoes(self, db: Session, client: TestClient):
        payload = OperacaoFactory.build(
            nom_operacao="Operação Teste"
        )

        client.post(OperacaoFactory.URL, json=payload)
        response = client.get(OperacaoFactory.URL)
        assert response.status_code == 200

class TestGetOperacaoByCasoId:
        def test_get_success(self, db: Session, client: TestClient):
            tipo = _seed_generic(db, OperacaoTipoFactory, OperacaoTipoModel, 1, dsc_operacao_tipo="Coordenada")[0]
            status = _seed_generic(db, OperacaoStatusFactory, OperacaoStatusModel, 1, dsc_operacao_status="Em planejamento")[0]
            caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
            agente = _seed_generic(db, AgenteFactory, AgenteModel, 1)[0]    
            data_mock = OperacaoFactory.build(
                cod_operacao_tipo=tipo.cod_operacao_tipo,
                cod_operacao_status=status.cod_operacao_status,
                cod_caso=15
            )
            data_mock.pop("encarregados", None) 
            
            operacao_mock = OperacaoModel(**data_mock)
            db.add(operacao_mock)
            db.flush()  
            encarregado = OperacaoEncarregadoModel(
                cod_operacao=operacao_mock.cod_operacao,
                cod_agente=agente.cod_agente,
                flg_titular=True,
                dat_inicio=datetime.now(timezone.utc),
                cif_usuario_inc=1,
                cif_usuario_alt=1,
                flg_reg_excluido=False
            )
            db.add(encarregado)
            db.commit() 
            response = client.get(f"{OperacaoFactory.URL}/caso/15")
            data = response.json()

            assert response.status_code == 200
            assert all(item["cod_caso"] == 15 for item in data)
