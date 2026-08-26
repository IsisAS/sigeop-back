import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from src.modules.caso.caso.caso_model import CasoModel
from src.modules.pedido.pedido_model import PedidoModel
from tests.helpers import (
    CasoFactory,
    PedidoFactory,
    assert_validation_error,
)

def _seed_create(db: Session, count: int, cod_pedido: int):
    objects = []
    for i in range(count):
        dados_caso = CasoFactory.build()
        dados_caso.pop("encarregados", None)
        dados_caso.pop("pedidos_vinculados", None)
        
        dados_caso["cod_pedido_abertura"] = cod_pedido + i
        
        obj = CasoModel(**dados_caso)
        db.add(obj)
        objects.append(obj)

    db.commit()

    for obj in objects:
        db.refresh(obj)
        
    return objects

def _seed_pedido(db: Session, count: int):
    objects = []
    for _ in range(count):
        dados_pedido = PedidoFactory.build()
        dados_pedido.pop("cod_pedido_tipo", None)
        dados_pedido.pop("cod_pedido_original", None)
        
        obj = PedidoModel(**dados_pedido)
        db.add(obj)
        objects.append(obj)

    db.commit()

    for obj in objects:
        db.refresh(obj)
    
    return objects

def _obter_payload_padrao_caso(db):
   pedidos = _seed_pedido(db, 2)
   pedido_livre = pedidos[1]
   
   teste = _seed_create(db, 1, pedidos[0].cod_pedido)[0]
   
   payload = {
       "cod_pedido_abertura": pedido_livre.cod_pedido, 
       "nom_caso": "Teste do caso", 
       "dsc_caso": teste.dsc_caso, 
       "flg_reg_excluido": False, 
       "cif_usuario_inc": teste.cif_usuario_inc, 
       "cif_usuario_alt": teste.cif_usuario_alt,
       "cod_caso_status": teste.cod_caso_status,
       "encarregados": [],
       "pedidos_vinculados": []
    }
   return payload

def _obter_data_formatada(data_utc) -> str:
   return data_utc.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def _obter_data_inicio() -> str:
   data_hoje_utc = datetime.now(timezone.utc)
   data_formatada_hoje = _obter_data_formatada(data_hoje_utc)
   return data_formatada_hoje

def _obter_encarregados(**kwargs):
   data_inicio = _obter_data_inicio()
   return [
           {
              "cod_agente": 1,
              "flg_titular": kwargs.get('flag_titular1'),
              "dat_inicio": data_inicio,
              "flg_reg_excluido": False
           },
           {
              "cod_agente": 2,
              "flg_titular": kwargs.get('flag_titular2'),
              "dat_inicio": data_inicio,
              "flg_reg_excluido": False
           }
       ]

class TestCreateCaso:
    
    def test_empty_body(self, client: TestClient):
        response = client.post(CasoFactory.URL, json={})
        assert_validation_error(response, fields=[
            "body.cod_pedido_abertura",
            "body.nom_caso",
            "body.dsc_caso",
            "body.flg_reg_excluido",
            "body.cif_usuario_inc",
            "body.cif_usuario_alt",
            "body.cod_caso_status",
            "body.encarregados"
        ])

    def test_success(self, db: Session, client: TestClient):
        payload = _obter_payload_padrao_caso(db)
        payload["encarregados"] = _obter_encarregados(flag_titular1=True, flag_titular2=False)
        response = client.post(f"{CasoFactory.URL}", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["nom_caso"] == "Teste do caso"
        assert "encarregados" in data

    def test_error_encarregados_vazio(self, db: Session, client: TestClient):
        payload = _obter_payload_padrao_caso(db)
        response = client.post(f"{CasoFactory.URL}", json=payload)
        assert response.status_code == 500

    def test_error_n_encarregados_titulares(self, db: Session, client: TestClient):
        payload = _obter_payload_padrao_caso(db)
        payload['encarregados'] = _obter_encarregados(flag_titular1=True, flag_titular2=True)
        response = client.post(f"{CasoFactory.URL}", json=payload)
        assert response.status_code == 500

    def test_error_nenhum_encarregado_titular(self, db: Session, client: TestClient):
        payload = _obter_payload_padrao_caso(db)
        payload['encarregados'] = _obter_encarregados(flag_titular1=False, flag_titular2=False)
        response = client.post(f"{CasoFactory.URL}", json=payload)
        assert response.status_code == 500
    
class TestGetCaso:

    def _criar_caso_sucesso(self, db: Session, client: TestClient) -> int:
        payload = _obter_payload_padrao_caso(db)
        payload["encarregados"] = _obter_encarregados(flag_titular1=True, flag_titular2=False)
        response = client.post(f"{CasoFactory.URL}", json=payload)
        data = response.json()
        return data['cod_caso']

    def test_success(self, db: Session, client: TestClient):
        cod_caso = self._criar_caso_sucesso(db, client)
        response = client.get(f"{CasoFactory.URL}/{cod_caso}")
        data = response.json()
        assert response.status_code == 200
        assert data["nom_caso"] == "Teste do caso"
        assert "encarregados" in data
    
    def test_error(self, client: TestClient):
        cod_caso = -1
        response = client.get(f"{CasoFactory.URL}/{cod_caso}")
        assert response.status_code == 404

class TestUpdateCaso:
    def _criar_caso_sucesso(self, db: Session, client: TestClient) -> dict:
        payload = _obter_payload_padrao_caso(db)
        payload["encarregados"] = _obter_encarregados(flag_titular1=True, flag_titular2=False)
        response = client.post(f"{CasoFactory.URL}", json=payload)
        return response.json()

    def test_success(self, db: Session, client: TestClient):
        caso_criado = self._criar_caso_sucesso(db, client)
        caso_criado['nom_caso'] = "Teste editado"
        cod_caso = caso_criado['cod_caso']
        caso_criado["encarregados"] = [
            {
              "cod_agente": 1,
              "flg_titular": False,
              "dat_inicio": _obter_data_inicio(),
              "flg_reg_excluido": False
           },
           {
              "cod_agente": 2,
              "flg_titular": True,
              "dat_inicio": _obter_data_inicio(),
              "flg_reg_excluido": False
           },
           {
              "cod_agente": 3,
              "flg_titular": False,
              "dat_inicio": _obter_data_inicio(),
              "flg_reg_excluido": True
           }
        ]
        caso_criado["pedidos_vinculados"] = []
        response = client.put(f"{CasoFactory.URL}/{cod_caso}", json=caso_criado)
        data = response.json()
        assert response.status_code == 200
        assert data["nom_caso"] == "Teste editado"
        assert "encarregados" in data

    def test_error_encarregados_vazio(self, db: Session, client: TestClient):
        payload = self._criar_caso_sucesso(db, client)
        cod_caso = payload['cod_caso']
        payload['encarregados'] = []
        response = client.put(f"{CasoFactory.URL}/{cod_caso}", json=payload)
        assert response.status_code == 500

    def test_error_n_encarregados_titulares(self, db: Session, client: TestClient):
        payload = self._criar_caso_sucesso(db, client)
        payload['encarregados'] = _obter_encarregados(flag_titular1=True, flag_titular2=True)
        cod_caso = payload['cod_caso']
        response = client.put(f"{CasoFactory.URL}/{cod_caso}", json=payload)
        assert response.status_code == 500

    def test_error_nenhum_encarregado_titular(self, db: Session, client: TestClient):
        payload = self._criar_caso_sucesso(db, client)
        payload['encarregados'] = _obter_encarregados(flag_titular1=False, flag_titular2=False)
        cod_caso = payload['cod_caso']
        response = client.put(f"{CasoFactory.URL}/{cod_caso}", json=payload)
        assert response.status_code == 500
    

class TestGetByPedidoAbertura:
    
    def test_success_get_casos_by_pedido_abertura(self, db: Session, client: TestClient):
        db.query(CasoModel).delete(synchronize_session=False)
        db.commit()
        
        pedido = _seed_pedido(db, 1)[0]
        template_caso = CasoFactory.build()
        
        payload = {
            "cod_pedido_abertura": pedido.cod_pedido,
            "nom_caso": "Caso unico teste",
            "dsc_caso": template_caso["dsc_caso"],
            "flg_reg_excluido": False,
            "cif_usuario_inc": template_caso["cif_usuario_inc"],
            "cif_usuario_alt": template_caso["cif_usuario_alt"],
            "cod_caso_status": template_caso["cod_caso_status"],
            "encarregados": [
                {
                    "cod_agente": 1,
                    "flg_titular": True,
                    "dat_inicio": _obter_data_inicio(),
                    "flg_reg_excluido": False
                }
            ],
            "pedidos_vinculados": []
        }
        client.post(f"{CasoFactory.URL}", json=payload)

        response = client.get(f"{CasoFactory.URL}/pedido-abertura/{pedido.cod_pedido}")
        assert response.status_code == 200
        
        casos = response.json()
        assert len(casos) == 1, "De acordo com v1.8, so pode existir 1 Caso por Pedido de Abertura"
        assert casos[0]["cod_pedido_abertura"] == pedido.cod_pedido

    def test_empty_result_get_casos_by_pedido_abertura(self, db: Session, client: TestClient):
        pedido = _seed_pedido(db, 1)[0]
        response = client.get(f"{CasoFactory.URL}/pedido-abertura/{pedido.cod_pedido}")
        assert response.status_code == 200
        casos = response.json()
        assert len(casos) == 0