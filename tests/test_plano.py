from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, mapped_column, Mapped
from sqlalchemy import DateTime, Integer, String, Date, Boolean
from datetime import date, datetime
from fastapi.encoders import jsonable_encoder
from src.modules.plano.plano_model import PlanoModel
from src.modules.plano.plano_tipo.plano_tipo_model import PlanoTipoModel
from src.modules.plano.plano_status.plano_status_model import PlanoStatusModel
from src.modules.caso.caso.caso_model import CasoModel
from src.modules.operacao.operacao_model import OperacaoModel
from src.modules.missao.missao_model import MissaoModel
from src.modules.unidade.unidade_model import UnidadeModel

from tests.helpers import (
    PlanoFactory,
    PlanoTipoFactory,
    PlanoStatusFactory,
    CasoFactory,
    OperacaoFactory,
    MissaoFactory,
    UnidadeFactory,
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

class TestCreatePlano:
    def test_success(self, db: Session, client: TestClient):
        teste_plano_tipo = _seed_generic(db, PlanoTipoFactory, PlanoTipoModel, 1)[0]
        teste_plano_status = _seed_generic(db, PlanoStatusFactory, PlanoStatusModel, 1)[0]
        teste_plano = _seed_generic(db, PlanoFactory, PlanoModel, 1)[0]

        payload = {
            "cod_plano_tipo": teste_plano_tipo.cod_plano_tipo,
            "cod_plano_status": teste_plano_status.cod_plano_status,
            "num_plano": teste_plano.num_plano,
            "cod_caso": None,
            "cod_operacao": None,
            "cod_missao": None,
            "cod_unidade": None,
            "num_ano": teste_plano.num_ano,
            "dat_emissao": "2026-05-04T18:45:36.163Z",
            "dat_inicio": "2026-05-04T18:45:36.163Z",
            "dat_termino": "2026-05-04T18:45:36.163Z",
            "dsc_assunto": teste_plano.dsc_assunto,
            "dsc_local": teste_plano.dsc_local,
            "num_equipe": teste_plano.num_equipe,
            "flg_reg_excluido": False,
            "cif_usuario_inc": teste_plano.cif_usuario_inc,
            "cif_usuario_alt": teste_plano.cif_usuario_alt,
        }
        response = client.post(f"{PlanoFactory.URL}", json=payload)
        body = response.json()
        
        assert body['num_plano'] == payload['num_plano']
        assert body['dsc_local'] == payload['dsc_local']
        assert response.status_code == 201

    def test_success_criacao_completa(self, db: Session, client: TestClient):
        teste_plano = _seed_generic(db, PlanoFactory, PlanoModel, 1)[0]
        teste_plano_tipo = _seed_generic(db, PlanoTipoFactory, PlanoTipoModel, 1)[0]
        teste_plano_status = _seed_generic(db, PlanoStatusFactory, PlanoStatusModel, 1)[0]
        teste_caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        teste_operacao = _seed_generic(db, OperacaoFactory, OperacaoModel, 1)[0]
        teste_missao = _seed_generic(db, MissaoFactory, MissaoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
                
        payload = {
            "cod_plano_tipo": teste_plano_tipo.cod_plano_tipo,
            "cod_plano_status": teste_plano_status.cod_plano_status,
            "cod_caso": teste_caso.cod_caso,
            "cod_operacao": teste_operacao.cod_operacao,
            "cod_missao": teste_missao.cod_missao,
            "cod_unidade": teste_unidade.cod_unidade,
            "num_plano": teste_plano.num_plano,
            "num_ano": teste_plano.num_ano,
            "dat_emissao": "2026-05-04T18:45:36.163Z",
            "dat_aprovacao": "2026-05-04T18:45:36.163Z",
            "dat_inicio": "2026-05-04T18:45:36.163Z",
            "dat_termino": "2026-05-04T18:45:36.163Z",
            "dat_baixa": "2026-05-04T18:45:36.163Z",
            "dsc_assunto": teste_plano.dsc_assunto,
            "vlr_custo_estimado": 2000,
            "vlr_verba_sigilosa_aprovada": 4000,
            "vlr_verba_ostensiva_aprovada": 3000,
            "dsc_local": teste_plano.dsc_local,
            "num_equipe": teste_plano.num_equipe,
            "flg_reg_excluido": False,
            "cif_usuario_inc": teste_plano.cif_usuario_inc,
            "cif_usuario_alt": teste_plano.cif_usuario_alt,
        }

        response = client.post(f"{PlanoFactory.URL}", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body['cod_plano_tipo'] == teste_plano_tipo.cod_plano_tipo
        assert body['cod_plano_status'] == teste_plano_status.cod_plano_status
        assert body['cod_caso'] == teste_caso.cod_caso
        assert body['cod_operacao'] == teste_operacao.cod_operacao
        assert body['cod_missao'] == teste_missao.cod_missao
        assert body['cod_unidade'] == teste_unidade.cod_unidade

    def test_empty_body(self, client: TestClient):
        response = client.post(PlanoFactory.URL, json={})
        print("[TEST PLANO] test_empty_body: ", response)
        assert_validation_error(response, fields=[
            "body.cod_plano_tipo", 
            "body.cod_plano_status",
            "body.num_plano", 
            "body.num_ano", 
            "body.dat_emissao",
            "body.dat_inicio", 
            "body.dat_termino",
            "body.flg_reg_excluido",
            "body.cif_usuario_inc", 
            "body.cif_usuario_alt"
        ])

class TestUpdatePlano:
    def test_success_update_completo(self, db: Session, client: TestClient):
        teste_plano = _seed_generic(db, PlanoFactory, PlanoModel, 1)[0]
        teste_plano_tipo = _seed_generic(db, PlanoTipoFactory, PlanoTipoModel, 1)[0]
        teste_plano_status = _seed_generic(db, PlanoStatusFactory, PlanoStatusModel, 1)[0]
        teste_caso = _seed_generic(db, CasoFactory, CasoModel, 1)[0]
        teste_operacao = _seed_generic(db, OperacaoFactory, OperacaoModel, 1)[0]
        teste_missao = _seed_generic(db, MissaoFactory, MissaoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
                
        payload = {
            "cod_plano_tipo": teste_plano_tipo.cod_plano_tipo,
            "cod_plano_status": teste_plano_status.cod_plano_status,
            "cod_caso": teste_caso.cod_caso,
            "cod_operacao": teste_operacao.cod_operacao,
            "cod_missao": teste_missao.cod_missao,
            "cod_unidade": teste_unidade.cod_unidade,
            "num_plano": teste_plano.num_plano,
            "num_ano": teste_plano.num_ano,
            "dat_emissao": "2026-05-04T18:45:36.163Z",
            "dat_aprovacao": "2026-05-04T18:45:36.163Z",
            "dat_inicio": "2026-05-04T18:45:36.163Z",
            "dat_termino": "2026-05-04T18:45:36.163Z",
            "dat_baixa": "2026-05-04T18:45:36.163Z",
            "dsc_assunto": teste_plano.dsc_assunto,
            "vlr_custo_estimado": 2000,
            "vlr_verba_sigilosa_aprovada": 4000,
            "vlr_verba_ostensiva_aprovada": 3000,
            "dsc_local": teste_plano.dsc_local,
            "num_equipe": teste_plano.num_equipe,
            "flg_reg_excluido": False,
            "cif_usuario_inc": teste_plano.cif_usuario_inc,
            "cif_usuario_alt": teste_plano.cif_usuario_alt,
        }

        response_create = client.post(f"{PlanoFactory.URL}", json=payload)
        assert response_create.status_code == 201
        plano_id = response_create.json()["cod_plano"]

        payload_update = {
            "cod_plano_tipo": teste_plano_tipo.cod_plano_tipo,
            "cod_plano_status": teste_plano_status.cod_plano_status,
            "cod_caso": teste_caso.cod_caso,
            "cod_operacao": teste_operacao.cod_operacao,
            "cod_missao": teste_missao.cod_missao,
            "cod_unidade": teste_unidade.cod_unidade,
            "num_plano": f"{teste_plano.num_plano} Editado",
            "num_ano": teste_plano.num_ano,
            "dat_emissao": "2026-05-04T18:45:36.163Z",
            "dat_aprovacao": "2026-05-04T18:45:36.163Z",
            "dat_inicio": "2026-05-04T18:45:36.163Z",
            "dat_termino": "2026-05-04T18:45:36.163Z",
            "dat_baixa": "2026-05-04T18:45:36.163Z",
            "dsc_assunto": f"{teste_plano.dsc_assunto} Editado",
            "vlr_custo_estimado": 1000,
            "vlr_verba_sigilosa_aprovada": 1000,
            "vlr_verba_ostensiva_aprovada": 1000,
            "dsc_local": teste_plano.dsc_local,
            "num_equipe": teste_plano.num_equipe,
            "flg_reg_excluido": False,
            "cif_usuario_inc": teste_plano.cif_usuario_inc,
            "cif_usuario_alt": 99,
        }

        response_update = client.put(f"{PlanoFactory.URL}/{plano_id}", json=payload_update)
        
        assert response_update.status_code == 200
        data = response_update.json()

        assert data["num_plano"] == f"{teste_plano.num_plano} Editado"
        assert data["dsc_assunto"] == f"{teste_plano.dsc_assunto} Editado"
        assert data["vlr_custo_estimado"] == '1000.00'
        assert data["vlr_verba_sigilosa_aprovada"] == '1000.00'
        assert data["vlr_verba_ostensiva_aprovada"] == '1000.00'
        assert data["cif_usuario_alt"] == 99

    def test_not_found_ao_atualizar(self, client: TestClient):
        payload = {"cif_usuario_alt": 1}
        response = client.put(f"{PlanoFactory.URL}/99999", json=payload)
        
        assert response.status_code in [404, 422]
        
class TestGetPlano:
    def criar_plano(self, db):
        teste_plano = _seed_generic(db, PlanoFactory, PlanoModel, 1)[0]
        return teste_plano

    def test_get_by_id_success(self, db: Session, client: TestClient):
        plano = self.criar_plano(db)

        response = client.get(f"{PlanoFactory.URL}/{plano.cod_plano}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["cod_plano"] == plano.cod_plano
        assert data["num_plano"] == plano.num_plano
        assert data["dsc_assunto"] == plano.dsc_assunto

    def test_get_by_id_not_found(self, client: TestClient):
        response = client.get(f"{PlanoFactory.URL}/999999")
        
        assert_not_found(response)
        
