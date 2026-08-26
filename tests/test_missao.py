from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.modules.missao.missao_model import MissaoModel
from src.modules.missao.missao_status.missao_status_model import MissaoStatusModel 
from src.modules.missao.missao_tipo.missao_tipo_model import MissaoTipoModel 
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel
from tests.helpers import (
    MissaoFactory,
    MissaoStatusFactory,
    MissaoTipoFactory,
    RecursoTipoFactory,
    assert_validation_error,
)

def _seed_missao_tipo(db: Session, **overrides) -> MissaoTipoModel: 
    obj = MissaoTipoModel(**MissaoTipoFactory.build(**overrides))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def _seed_missao_status(db: Session, **overrides) -> MissaoStatusModel: 
    obj = MissaoStatusModel(**MissaoStatusFactory.build(**overrides))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def _seed_recurso_tipo(db: Session, **overrides) -> RecursoTipoModel:
    obj = RecursoTipoModel(**RecursoTipoFactory.build(**overrides))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

_cod_agente_counter = 5000

def _novo_cod_agente() -> int:
    global _cod_agente_counter
    _cod_agente_counter += 1
    return _cod_agente_counter

def _encarregado_payload(cod_agente: int, flg_titular: bool) -> dict: 
    return {
        "cod_agente": cod_agente,
        "flg_titular": flg_titular,
        "dat_inicio": datetime.now(timezone.utc).isoformat(),
        "dat_fim": None, 
        "flg_reg_excluido": False,
        "cif_usuario_inc": 1,
        "cif_usuario_alt": 1,
    }
    
def _fonte_humana_payload(cod_missao: int, cod_fonte_humana: int) -> dict:
    return {
        "cod_missao": cod_missao,
        "cod_fonte_humana": cod_fonte_humana,
        "flg_reg_excluido": False,
        "cif_usuario_inc": 1,
        "cif_usuario_alt": 1,
    }
    
class TestCreateMissao:
    def test_empty_body(self, client: TestClient):
        response = client.post(MissaoFactory.URL, json={})
        assert_validation_error(
            response,
            fields=[
                "body.cod_missao_tipo",
                "body.flg_reg_excluido",
                "body.encarregados",
            ],
        )
        
    def test_success(self, db: Session, client: TestClient):
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLICACAO_RECURSOS")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        recurso_tipo = _seed_recurso_tipo(db, sig_recurso_tipo="AGENTE_NAO_ORGANICO")
        agente = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            cod_recurso_tipo=recurso_tipo.cod_recurso_tipo,
            idn_agente_nao_organico="ANO-TESTE-001",
            encarregados=[_encarregado_payload(agente, True)],
        )
        payload["idn_processo"] = "LEGADO-REMOVIDO-19"
        
        response = client.post(MissaoFactory.URL, json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["dsc_missao"] == payload["dsc_missao"]
        assert data["cod_recurso_tipo"] == recurso_tipo.cod_recurso_tipo
        assert data["sig_recurso_tipo"] == "AGENTE_NAO_ORGANICO"
        assert data["idn_agente_nao_organico"] == "ANO-TESTE-001"
        assert "idn_processo" not in data
        assert len(data["encarregados"]) == 1
        assert data["encarregados"][0]["dat_fim"] is None
        
    def test_error_encarregados_vazio(self, db: Session, client: TestClient):
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLICACAO_RECURSOS")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[],
        )
        
        response = client.post(MissaoFactory.URL, json=payload)
        assert response.status_code == 409
        
    def test_error_multiplos_titulares(self, db: Session, client: TestClient):
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLICACAO_RECURSOS")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente_1 = _novo_cod_agente()
        agente_2 = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[
                _encarregado_payload(agente_1, True),
                _encarregado_payload(agente_2, True),
            ]            
        )
        
        response = client.post(MissaoFactory.URL, json=payload)
        assert response.status_code == 409
    
    def test_error_sem_titulares(self, db: Session, client: TestClient):
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLICACAO_RECURSOS")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente_1 = _novo_cod_agente()
        agente_2 = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[
                _encarregado_payload(agente_1, True),
                _encarregado_payload(agente_2, True),
            ]            
        )
        
        response = client.post(MissaoFactory.URL, json=payload)
        assert response.status_code == 409
        
class TestGetMissao:    
    def test_success(self, db: Session, client: TestClient):
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLICACAO_RECURSOS")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[_encarregado_payload(agente, True)],
        )
        created = client.post(MissaoFactory.URL, json=payload).json()
        
        response = client.get(f"{MissaoFactory.URL}/{created['cod_missao']}")
        assert response.status_code == 200
        data = response.json()
        assert data["cod_missao"] == created["cod_missao"]
        assert len(data["encarregados"]) == 1
    
    def test_not_found(self, client: TestClient):
        response = client.get(f"{MissaoFactory.URL}/999")
        assert response.status_code == 404

class TestListMissao: 
    def test_empty(self, client: TestClient):
        response = client.get(MissaoFactory.URL)
        assert response.status_code == 200
        assert response.json() == []
        
    def test_with_data(self, db: Session, client: TestClient):
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLICACAO_RECURSOS")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[_encarregado_payload(agente, True)],
        )
        client.post(MissaoFactory.URL, json=payload)
        
        response = client.get(MissaoFactory.URL)
        assert response.status_code == 200
        assert len(response.json()) == 1
        
class TestUpdateMissao:
    def test_update_success(self, db: Session, client: TestClient):
        """Testa atualização bem-sucedida de missão"""
        
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLIACAO_RECURSO")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[_encarregado_payload(agente, True)]
        )
        create_response = client.post(MissaoFactory.URL, json=payload)
        cod_missao = create_response.json()["cod_missao"]

        update_payload = MissaoFactory.build(
            num_missao="MSS-2026-UPDATE-001-MODIFIED",
            dsc_missao="Descrição alterada",
            cod_missao_status=2,
            encarregados=[_encarregado_payload(agente, True)]
        )
        response = client.put(f"{MissaoFactory.URL}/{cod_missao}", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["dsc_missao"] == "Descrição alterada"
        assert data["cod_missao_status"] == 2

    def test_update_add_encarregado(self, db: Session, client: TestClient):
        """Testa adição de novo encarregado em atualização"""
        
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLIACAO_RECURSO")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[_encarregado_payload(agente, True)]
        )
        create_response = client.post(MissaoFactory.URL, json=payload)
        cod_missao = create_response.json()["cod_missao"]

        update_payload = MissaoFactory.build(
            encarregados=[
                {
                    "cod_agente": 1,
                    "flg_titular": True,
                    "dat_inicio": "2026-04-16T00:00:00Z",
                    "dat_fim": None,
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1,
                },
                {
                    "cod_agente": 2,
                    "flg_titular": False,
                    "dat_inicio": "2026-04-16T00:00:00Z",
                    "dat_fim": None,
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1,
                }
            ]
        )
        response = client.put(f"{MissaoFactory.URL}/{cod_missao}", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        assert len(data["encarregados"]) == 2

    def test_update_inativar_encarregado(self, db: Session, client: TestClient):
        """Testa inativação de encarregado"""
        
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLIACAO_RECURSO")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente_1 = _novo_cod_agente()
        agente_2 = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[
                _encarregado_payload(agente_1, True),
                _encarregado_payload(agente_2, False),
            ]
        )
        create_response = client.post(MissaoFactory.URL, json=payload)
        cod_missao = create_response.json()["cod_missao"]

        update_payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[
                _encarregado_payload(agente_1, True),
                {
                    "cod_agente": agente_2,
                    "flg_titular": False,
                    "dat_inicio": "2026-04-16T00:00:00Z",
                    "dat_fim": "2026-05-16T00:00:00Z",
                    "flg_reg_excluido": True,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1,
                }
            ]
        )
        response = client.put(f"{MissaoFactory.URL}/{cod_missao}", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        ativos = data["encarregados"]
        assert len(ativos) == 1
        assert ativos[0]["cod_agente"] == agente_1
        
    def test_update_not_found(self, client: TestClient):
        """Testa atualização de missão inexistente"""
        payload = MissaoFactory.build()
        response = client.put(f"{MissaoFactory.URL}/9999", json=payload)
        assert response.status_code == 404
        
    def test_update_error_data_fim_menor_que_inicio(self, db: Session, client: TestClient):
        """Testa atualização com data fim menor que data inicio"""
                
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLIACAO_RECURSO")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[_encarregado_payload(agente, True)]
        )
        create_response = client.post(MissaoFactory.URL, json=payload)
        cod_missao = create_response.json()["cod_missao"]
        
        update_payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[{
                    "cod_agente": agente,
                    "flg_titular": True,
                    "dat_inicio": "2026-04-16T00:00:00Z",
                    "dat_fim": "2026-03-16T00:00:00Z",
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1,
                }]
        )
        
        response = client.put(f"{MissaoFactory.URL}/{cod_missao}", json=update_payload)
        assert response.status_code == 409
        
    def test_update_multiplas_fontes_humanas(self, db: Session, client: TestClient):
        """Teste adição de múltiplas fontes humanas no update"""
        
        tipo = _seed_missao_tipo(db, sig_missao_tipo="AMPLIACAO_RECURSO")
        status = _seed_missao_status(db, sig_missao_status="EM_PLANEJAMENTO")
        agente = _novo_cod_agente()
        
        payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[
                _encarregado_payload(agente, True)
            ]
        )
        create_response = client.post(MissaoFactory.URL, json=payload)
        cod_missao = create_response.json()["cod_missao"]

        update_payload = MissaoFactory.build(
            cod_missao_tipo=tipo.cod_missao_tipo,
            cod_missao_status=status.cod_missao_status,
            encarregados=[_encarregado_payload(agente, True)],
            fontes_humanas=[
                _fonte_humana_payload(cod_missao=cod_missao, cod_fonte_humana=1),
                _fonte_humana_payload(cod_missao=cod_missao, cod_fonte_humana=2)
            ]
        )
        response = client.put(f"{MissaoFactory.URL}/{cod_missao}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "fontes_humanas" in data
        assert len(data["fontes_humanas"]) == 2
