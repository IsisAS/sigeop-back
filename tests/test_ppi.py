from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, mapped_column, Mapped
from sqlalchemy import DateTime, Integer, String, Date, Boolean
from datetime import date, datetime
from decimal import Decimal
from fastapi.encoders import jsonable_encoder
from src.modules.unidade.unidade_model import UnidadeModel
from src.modules.ppi.ppi_model import PPIModel

from tests.helpers import (
    UnidadeFactory,
    PPIFactory,
    assert_not_found,
    assert_conflict,
    assert_validation_error,
)

def _seed_generic(db: Session, factory, model_class, count: int, **overrides):
    objects = []
    for _ in range(count):
        obj = model_class(**factory.build())
        db.add(obj)
        objects.append(obj)
    db.commit()
    for obj in objects:
        db.refresh(obj)
    return objects

class TestCreatePPI:
    def test_success(self, db: Session, client: TestClient):
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        payload = PPIFactory.build()
        payload['cod_unidade'] = teste_unidade.cod_unidade

        response = client.post(f"{PPIFactory.URL}", json=payload)
        body = response.json()

        val_orcamento_sigiloso_decimal = Decimal(body['val_orcamento_sigiloso'])
        val_orcamento_ostensivo_decimal = Decimal(body['val_orcamento_ostensivo'])
        assert body['cod_unidade'] == teste_unidade.cod_unidade
        assert body['num_ano'] == payload['num_ano']
        assert body['nom_ppi'] == payload['nom_ppi']
        assert body['idn_codigo_poa_sigiloso'] == payload['idn_codigo_poa_sigiloso']
        assert body['idn_codigo_poa_ostensivo'] == payload['idn_codigo_poa_ostensivo']
        assert val_orcamento_sigiloso_decimal == payload['val_orcamento_sigiloso']
        assert val_orcamento_ostensivo_decimal == payload['val_orcamento_ostensivo']
        assert response.status_code == 201

    def test_empty_body(self, client: TestClient):
        response = client.post(PPIFactory.URL, json={})
        assert_validation_error(response, fields=[
            "body.cod_unidade", 
            "body.num_ano",
            "body.nom_ppi", 
            "body.idn_codigo_poa_sigiloso", 
            "body.idn_codigo_poa_ostensivo",
            "body.flg_reg_excluido", 
            "body.cif_usuario_inc",
            "body.cif_usuario_alt", 
        ])

class TestUpdatePPI:
    def test_success(self, db: Session, client: TestClient):
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        payload = PPIFactory.build()
        payload['cod_unidade'] = teste_unidade.cod_unidade
            
        response_create = client.post(f"{PPIFactory.URL}", json=payload)
        assert response_create.status_code == 201
        ppi_id = response_create.json()["cod_ppi"]

        payload_update = {
            'cod_unidade': teste_unidade.cod_unidade,
            'num_ano': 2027,
            'nom_ppi': 'Nome PPI Atualizado',
            'idn_codigo_poa_sigiloso': 'Codigo poa sigiloso Atualizado',
            'idn_codigo_poa_ostensivo': 'Codigo poa ostensivo Atualizado',
            'idn_codigo_poa_ostensivo': 'Codigo poa ostensivo Atualizado',
            'val_orcamento_sigiloso': 20.00,
            'val_orcamento_ostensivo': 25.00,
            "flg_reg_excluido": True,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 99,
        }

        response_update = client.put(f"{PPIFactory.URL}/{ppi_id}", json=payload_update)
        
        assert response_update.status_code == 200
        data = response_update.json()

        val_orcamento_sigiloso_decimal = Decimal(data['val_orcamento_sigiloso'])
        val_orcamento_ostensivo_decimal = Decimal(data['val_orcamento_ostensivo'])

        assert data['cod_unidade'] == payload_update['cod_unidade']
        assert data['num_ano'] == payload_update['num_ano']
        assert data['nom_ppi'] == payload_update['nom_ppi']
        assert data['idn_codigo_poa_sigiloso'] == payload_update['idn_codigo_poa_sigiloso']
        assert data['idn_codigo_poa_ostensivo'] == payload_update['idn_codigo_poa_ostensivo']
        assert val_orcamento_sigiloso_decimal == payload_update['val_orcamento_sigiloso']
        assert val_orcamento_ostensivo_decimal == payload_update['val_orcamento_ostensivo']
        assert data['flg_reg_excluido'] == payload_update['flg_reg_excluido']
        assert data['cif_usuario_inc'] == payload_update['cif_usuario_inc']
        assert data['cif_usuario_alt'] == payload_update['cif_usuario_alt']
        
        assert response_update.status_code == 200

    def test_not_found_ao_atualizar(self, client: TestClient):
        payload = {"cif_usuario_alt": 1}
        response = client.put(f"{PPIFactory.URL}/99999", json=payload)
        
        assert response.status_code in [404, 422]

    def test_propriedades_obrigatorias_faltando_ao_atualizar(self, db: Session, client: TestClient):
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        payload = PPIFactory.build()
        payload['cod_unidade'] = teste_unidade.cod_unidade
            
        response_create = client.post(f"{PPIFactory.URL}", json=payload)
        assert response_create.status_code == 201
        ppi_id = response_create.json()["cod_ppi"]

        payload_update = {
            'idn_codigo_poa_ostensivo': 'Codigo poa ostensivo Atualizado',
            'val_orcamento_sigiloso': 20.00,
            'val_orcamento_ostensivo': 25.00,
            "flg_reg_excluido": True,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 99,
        }
        
        response = client.put(f"{PPIFactory.URL}/{ppi_id}", json=payload_update)
        assert response.status_code == 422
        
class TestGetPPI:
    def criar_ppi(self, db):
        teste_ppi = _seed_generic(db, PPIFactory, PPIModel, 1)[0]
        return teste_ppi

    def test_get_by_id_success(self, db: Session, client: TestClient):
        ppi = self.criar_ppi(db)

        response = client.get(f"{PPIFactory.URL}/{ppi.cod_ppi}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["cod_ppi"] == ppi.cod_ppi
        assert data["num_ano"] == ppi.num_ano
        assert data["nom_ppi"] == ppi.nom_ppi

    def test_get_by_id_not_found(self, client: TestClient):
        response = client.get(f"{PPIFactory.URL}/999999")
        
        assert_not_found(response)

class TestListPPI:
    def test_empty(self, client: TestClient):
        response = client.get(PPIFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_with_data(self, db: Session, client: TestClient):
        qtd_ppis = 3
        _seed_generic(db, PPIFactory, PPIModel, qtd_ppis)[0]
        response = client.get(PPIFactory.URL)
        assert response.status_code == 200
        assert len(response.json()) == qtd_ppis

    def test_pagination(self, db: Session, client: TestClient):
        _seed_generic(db, PPIFactory, PPIModel, 5)[0]
        
        response = client.get(f"{PPIFactory.URL}?limit=2&offset=0")
        assert len(response.json()) == 2

        response = client.get(f"{PPIFactory.URL}?limit=2&offset=2")
        assert len(response.json()) == 2
