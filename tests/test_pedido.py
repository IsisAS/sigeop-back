from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, mapped_column, Mapped
from sqlalchemy import DateTime, Integer, String, Date, Boolean
from datetime import date, datetime
from fastapi.encoders import jsonable_encoder
import pytest

from src.db.base import Base
from src.modules.pedido.pedido_model import PedidoModel

from src.modules.pedido.status.status_model import StatusModel
from src.modules.pedido.analista.analista_model import AnalistaModel
from src.modules.agente.agente_model import AgenteModel
from src.modules.unidade.unidade_model import UnidadeModel
from src.modules.ppi.ppi_model import PPIModel

from tests.helpers import (
    PedidoFactory,
    PPIFactory,
    TematicaFactory,
    TematicaVinculoFactory,
    TipoFactory,
    UnidadeFactory,
    StatusFactory,
    AnalistaFactory,
    AgenteFactory,
    assert_validation_error,
    assert_not_found
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

class TestListTipo:
    def test_empty(self, client: TestClient):
        response = client.get(TipoFactory.URL)
        assert response.status_code == 200
        assert response.json() == []

    def test_with_data(self, db: Session, client: TestClient):
        _seed_generic(db, TipoFactory, TipoModel, 3)
        response = client.get(TipoFactory.URL)
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_pagination(self, db: Session, client: TestClient):
        _seed_generic(db, TipoFactory, TipoModel, 5)

        response = client.get(f"{TipoFactory.URL}?limit=2&offset=0")
        assert len(response.json()) == 2

        response = client.get(f"{TipoFactory.URL}?limit=2&offset=2")
        assert len(response.json()) == 2

class TestCreatePedido:
    def test_success(self, db: Session, client: TestClient):
        teste_ppi = _seed_generic(db, PPIFactory, PPIModel, 1)[0]
        teste_pedido_tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        teste_pedido_status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]
        
        payload = {
            "cod_ppi": teste_ppi.cod_ppi,
            "cod_pedido_tipo": teste_pedido_tipo.cod_pedido_tipo,
            "cod_pedido_original": None,
            "cod_unidade_analise": teste_unidade.cod_unidade,
            "cod_unidade_elo": teste_unidade.cod_unidade,
            "num_pedido": "REQ-MOCK-2026",
            "num_ano": 2026,
            "dat_emissao": "2026-03-04",
            "dsc_assunto": "Assunto teste",
            "idn_processo": "PROC-12345",
            "dat_prazo": "2026-04-04",
            "cod_pedido_status": teste_pedido_status.cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1
        }

        payload = jsonable_encoder(payload)
        response = client.post(f"{PedidoFactory.URL}", json=payload)
        
        assert response.status_code == 201
        novo_cod_pedido = response.json()["cod_pedido"]
        
        teste_pedido_tematica = _seed_generic(db, TematicaFactory, TematicaModel, 1)[0]
        payloadTematicaVinculo = {
            "cod_pedido": novo_cod_pedido,
            "cod_tematica": teste_pedido_tematica.cod_tematica,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1
        }
        response_tem = client.post(f"{TematicaVinculoFactory.URL}", json=payloadTematicaVinculo)
        assert response_tem.status_code == 201
        
        teste_agente = _seed_generic(db, AgenteFactory, AgenteModel, 1)[0]
        payloadAnalista = {
            "cod_pedido": novo_cod_pedido,
            "cod_agente": teste_agente.cod_agente,
            "flg_titular": True,
            "dat_inicio": "2026-03-04T10:00:00",
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1
        }
        response_ana = client.post(f"{AnalistaFactory.URL}", json=payloadAnalista)
        assert response_ana.status_code == 201
        

    def test_success_criacao_completa(self, db: Session, client: TestClient):
        teste_ppi = _seed_generic(db, PPIFactory, PPIModel, 1)[0]
        teste_pedido_tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        teste_pedido_status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]
        
        tematicas_mock = _seed_generic(db, TematicaFactory, TematicaModel, 2)
        analistas_mock = _seed_generic(db, AnalistaFactory, AnalistaModel, 2)
        
        ids_tematicas = [t.cod_tematica for t in tematicas_mock]
        payload_analista = [
            {"cod_agente": analistas_mock[0].cod_agente, "flg_titular": False},
            {"cod_agente": analistas_mock[1].cod_agente, "flg_titular": True}
        ]    
                
        payload = {
            "cod_ppi": teste_ppi.cod_ppi,
            "cod_pedido_tipo": teste_pedido_tipo.cod_pedido_tipo, 
            "cod_unidade_analise": teste_unidade.cod_unidade, 
            "num_pedido": "12345",
            "num_ano": 2026, 
            "dat_emissao": "2026-03-15", 
            "dsc_assunto": "Assunto do Pedido Teste",
            "idn_processo": "PRC-999",
            "dat_prazo": "2026-04-15",
            "cod_pedido_status": teste_pedido_status.cod_pedido_status, 
            "flg_reg_excluido": False, 
            "cif_usuario_inc": 123, 
            "cif_usuario_alt": 123,
            "tematicas": ids_tematicas,
            "analistas": payload_analista
        }
                
        response = client.post(f"{PedidoFactory.URL}", json=payload)
        assert response.status_code == 201
        assert "cod_pedido" in response.json()

    def test_empty_body(self, client: TestClient):
        response = client.post(PedidoFactory.URL, json={})
        assert_validation_error(response, fields=[
            "body.cod_ppi",
            "body.cod_pedido_tipo", 
            "body.cod_unidade_analise",
            "body.num_ano", 
            "body.dat_emissao",
            "body.dat_prazo", 
            "body.flg_reg_excluido",
            "body.cif_usuario_inc", 
            "body.cif_usuario_alt"
        ])

class TestUpdatePedido:
    def test_success_update_completo(self, db: Session, client: TestClient):
        ppis = _seed_generic(db, PPIFactory, PPIModel, 1)
        tipos = _seed_generic(db, TipoFactory, TipoModel, 2)
        unidades = _seed_generic(db, UnidadeFactory, UnidadeModel, 2)
        status = _seed_generic(db, StatusFactory, StatusModel, 2)
        tematicas = _seed_generic(db, TematicaFactory, TematicaModel, 3)
        agentes = _seed_generic(db, AgenteFactory, AgenteModel, 2)
        
        payload_create = {
            "cod_ppi": ppis[0].cod_ppi,
            "cod_pedido_tipo": tipos[0].cod_pedido_tipo,
            "cod_unidade_analise": unidades[0].cod_unidade,
            "cod_unidade_elo": unidades[0].cod_unidade,
            "num_pedido": "PED-INICIAL-001",
            "num_ano": 2026,
            "dat_emissao": "2026-03-01",
            "dsc_assunto": "Assunto Inicial",
            "idn_processo": "PROC-INICIAL",
            "dat_prazo": "2026-04-01",
            "cod_pedido_status": status[0].cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1,
            "tematicas": [tematicas[0].cod_tematica, tematicas[1].cod_tematica],
            "analistas": [
                {"cod_agente": agentes[0].cod_agente, "flg_titular": True, "flg_reg_excluido": False}
            ]
        }
        
        response_create = client.post(PedidoFactory.URL, json=jsonable_encoder(payload_create))
        assert response_create.status_code == 201
        pedido_id = response_create.json()["cod_pedido"]

        payload_update = {
            "cod_ppi": ppis[0].cod_ppi,
            "cod_pedido_tipo": tipos[1].cod_pedido_tipo,
            "cod_unidade_analise": unidades[1].cod_unidade,
            "cod_unidade_elo": unidades[1].cod_unidade,
            "num_pedido": "PED-ALTERADO-999",
            "num_ano": 2027,
            "dat_emissao": "2027-05-10",
            "dsc_assunto": "Assunto Totalmente Editado",
            "idn_processo": "PROC-FINAL",
            "dat_prazo": "2027-06-10",
            "cod_pedido_status": status[1].cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_alt": 99,
            "dat_hor_alteracao": datetime.utcnow().isoformat(),
            "tematicas": [tematicas[1].cod_tematica, tematicas[2].cod_tematica], 
            "analistas": [
                {"cod_agente": agentes[0].cod_agente, "flg_titular": False, "flg_reg_excluido": False},
                {"cod_agente": agentes[1].cod_agente, "flg_titular": True, "flg_reg_excluido": False} 
            ]
        }

        response_update = client.put(f"{PedidoFactory.URL}/{pedido_id}", json=jsonable_encoder(payload_update))
        
        assert response_update.status_code == 200
        data = response_update.json()

        assert data["cod_pedido_tipo"] == tipos[1].cod_pedido_tipo
        assert data["cod_unidade_analise"] == unidades[1].cod_unidade
        assert data["cod_unidade_elo"] == unidades[1].cod_unidade
        assert data["num_pedido"] == "PED-ALTERADO-999"
        assert data["num_ano"] == 2027
        assert data["dat_emissao"] == "2027-05-10"
        assert data["dsc_assunto"] == "Assunto Totalmente Editado"
        assert data["idn_processo"] == "PROC-FINAL"
        assert data["dat_prazo"] == "2027-06-10"
        assert data["cod_pedido_status"] == status[1].cod_pedido_status
        assert data["cif_usuario_alt"] == 99

        assert len(data["tematicas"]) == 2
        tematicas_retornadas = [t["cod_tematica"] for t in data["tematicas"]]
        assert tematicas[1].cod_tematica in tematicas_retornadas
        assert tematicas[2].cod_tematica in tematicas_retornadas
        assert tematicas[0].cod_tematica not in tematicas_retornadas

        analistas_ativos = [a for a in data["analistas"] if a["flg_reg_excluido"] is False]
        assert len(analistas_ativos) == 2
        
        novo_titular = next(a for a in analistas_ativos if a["cod_agente"] == agentes[1].cod_agente)
        antigo_titular = next(a for a in analistas_ativos if a["cod_agente"] == agentes[0].cod_agente)
        
        assert novo_titular["flg_titular"] is True
        assert antigo_titular["flg_titular"] is False

    def test_not_found_ao_atualizar(self, client: TestClient):
        payload = {"cif_usuario_alt": 1}
        response = client.put(f"{PedidoFactory.URL}/99999", json=payload)
        
        assert response.status_code in [404, 422]
        
    def test_update_pedido_com_multiplos_titulares_analistas_fails(self, db: Session, client: TestClient):
        ppis = _seed_generic(db, PPIFactory, PPIModel, 1)
        tipos = _seed_generic(db, TipoFactory, TipoModel, 1)
        unidades = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)
        status = _seed_generic(db, StatusFactory, StatusModel, 1)
        agentes = _seed_generic(db, AgenteFactory, AgenteModel, 2)

        payload_create = {
            "cod_ppi": ppis[0].cod_ppi,
            "cod_pedido_tipo": tipos[0].cod_pedido_tipo,
            "cod_unidade_analise": unidades[0].cod_unidade,
            "num_pedido": "PED-INICIAL-001",
            "num_ano": 2026,
            "dat_emissao": "2026-03-01",
            "dsc_assunto": "Assunto Inicial",
            "idn_processo": "PROC-INICIAL",
            "dat_prazo": "2026-04-01",
            "cod_pedido_status": status[0].cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1,
            "tematicas": [],
            "analistas": [
                {"cod_agente": agentes[0].cod_agente, "flg_titular": True, "flg_reg_excluido": False}
            ]
        }
        response_create = client.post(PedidoFactory.URL, json=jsonable_encoder(payload_create))
        assert response_create.status_code == 201
        pedido_id = response_create.json()["cod_pedido"]

        payload_update = {
            "cod_ppi": ppis[0].cod_ppi,
            "cod_pedido_tipo": tipos[0].cod_pedido_tipo,
            "cod_unidade_analise": unidades[0].cod_unidade,
            "num_pedido": "PED-ALTERADO-999",
            "num_ano": 2027,
            "dat_emissao": "2027-05-10",
            "dsc_assunto": "Assunto Totalmente Editado",
            "idn_processo": "PROC-FINAL",
            "dat_prazo": "2027-06-10",
            "cod_pedido_status": status[0].cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_alt": 99,
            "tematicas": [],
            "analistas": [
                {"cod_agente": agentes[0].cod_agente, "flg_titular": True, "flg_reg_excluido": False},
                {"cod_agente": agentes[1].cod_agente, "flg_titular": True, "flg_reg_excluido": False} 
            ]
        }

        response_update = client.put(f"{PedidoFactory.URL}/{pedido_id}", json=jsonable_encoder(payload_update))
        assert response_update.status_code == 409
        
class TestGetPedido:
    def test_get_by_id_success(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]
        
        pedido_mock = PedidoModel(**PedidoFactory.build(
            cod_pedido_tipo=tipo.cod_pedido_tipo,
            cod_unidade_analise=unidade.cod_unidade,
            cod_pedido_status=status.cod_pedido_status,
            cif_usuario_inc=1,
            cif_usuario_alt=1
        ))
        db.add(pedido_mock)
        db.flush()
        
        tematica_mock = _seed_generic(db, TematicaFactory, TematicaModel, 1)[0]
        vinculo = TematicaVinculoModel(
            cod_pedido=pedido_mock.cod_pedido,
            cod_tematica=tematica_mock.cod_tematica,
            cif_usuario_inc=1,
            cif_usuario_alt=1,
            flg_reg_excluido=False
        )
        db.add(vinculo)
        
        agente_mock = _seed_generic(db, AgenteFactory, AgenteModel, 1)[0]
        analista = AnalistaModel(
            cod_pedido=pedido_mock.cod_pedido,
            cod_agente=agente_mock.cod_agente,
            flg_titular=True,
            cif_usuario_inc=1,
            cif_usuario_alt=1,
            flg_reg_excluido=False
        )
        db.add(analista)
        db.commit()

        response = client.get(f"{PedidoFactory.URL}/{pedido_mock.cod_pedido}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["cod_pedido"] == pedido_mock.cod_pedido
        assert data["num_pedido"] == pedido_mock.num_pedido
        
        assert isinstance(data["tematicas"], list)
        assert len(data["tematicas"]) == 1
        assert data["tematicas"][0]["cod_tematica"] == tematica_mock.cod_tematica
        assert "nom_tematica" in data["tematicas"][0]
        
        assert isinstance(data["analistas"], list)
        assert len(data["analistas"]) == 1
        assert data["analistas"][0]["cod_agente"] == agente_mock.cod_agente

    def test_get_by_id_not_found(self, client: TestClient):
        response = client.get(f"{PedidoFactory.URL}/999999")
        
        assert_not_found(response)
        
class TestGetPedido:
    def test_get_by_id_success(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]
        
        pedido_mock = PedidoModel(**PedidoFactory.build(
            cod_pedido_tipo=tipo.cod_pedido_tipo,
            cod_unidade_analise=unidade.cod_unidade,
            cod_pedido_status=status.cod_pedido_status,
            cif_usuario_inc=1,
            cif_usuario_alt=1
        ))
        db.add(pedido_mock)
        db.flush()
        
        tematica_mock = _seed_generic(db, TematicaFactory, TematicaModel, 1)[0]
        vinculo = TematicaVinculoModel(
            cod_pedido=pedido_mock.cod_pedido,
            cod_tematica=tematica_mock.cod_tematica,
            cif_usuario_inc=1,
            cif_usuario_alt=1,
            flg_reg_excluido=False
        )
        db.add(vinculo)
        
        agente_mock = _seed_generic(db, AgenteFactory, AgenteModel, 1)[0]
        analista = AnalistaModel(
            cod_pedido=pedido_mock.cod_pedido,
            cod_agente=agente_mock.cod_agente,
            flg_titular=True,
            cif_usuario_inc=1,
            cif_usuario_alt=1,
            flg_reg_excluido=False
        )
        db.add(analista)
        db.commit()

        response = client.get(f"{PedidoFactory.URL}/{pedido_mock.cod_pedido}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["cod_pedido"] == pedido_mock.cod_pedido
        assert data["num_pedido"] == pedido_mock.num_pedido
        
        assert isinstance(data["tematicas"], list)
        assert len(data["tematicas"]) == 1
        assert data["tematicas"][0]["cod_tematica"] == tematica_mock.cod_tematica
        assert "nom_tematica" in data["tematicas"][0]
        
        assert isinstance(data["analistas"], list)
        assert len(data["analistas"]) == 1
        assert data["analistas"][0]["cod_agente"] == agente_mock.cod_agente

    def test_get_by_id_not_found(self, client: TestClient):
        response = client.get(f"{PedidoFactory.URL}/999999")
        
        assert_not_found(response)
        
class TestCreatePedidoComplementar:
    def test_success_com_pedido_pai(self, db: Session, client: TestClient):
        teste_ppi = _seed_generic(db, PPIFactory, PPIModel, 1)[0]
        teste_pedido_tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        teste_pedido_status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]

        pedido_pai = PedidoModel(
            cod_ppi=teste_ppi.cod_ppi,
            cod_pedido_tipo=teste_pedido_tipo.cod_pedido_tipo,
            cod_pedido_original=None,
            cod_unidade_analise=teste_unidade.cod_unidade,
            cod_unidade_elo=teste_unidade.cod_unidade,
            num_pedido="PAI-001",
            num_ano=2026,
            dat_emissao=date(2026, 3, 1),
            dsc_assunto="Pedido pai",
            idn_processo="PROC-PAI-001",
            dat_prazo=date(2026, 4, 1),
            cod_pedido_status=teste_pedido_status.cod_pedido_status,
            flg_reg_excluido=False,
            cif_usuario_inc=1,
            cif_usuario_alt=1,
        )
        db.add(pedido_pai)
        db.commit()
        db.refresh(pedido_pai)

        payload = {
            "cod_ppi": teste_ppi.cod_ppi,
            "cod_pedido_tipo": teste_pedido_tipo.cod_pedido_tipo,
            "cod_pedido_original": pedido_pai.cod_pedido,
            "cod_unidade_analise": teste_unidade.cod_unidade,
            "cod_unidade_elo": teste_unidade.cod_unidade,
            "num_pedido": "COMP-001",
            "num_ano": 2026,
            "dat_emissao": "2026-03-15",
            "dsc_assunto": "Pedido complementar",
            "idn_processo": "PROC-COMP-001",
            "dat_prazo": "2026-04-15",
            "cod_pedido_status": teste_pedido_status.cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1,
        }

        response = client.post("/pedido/complementar", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["cod_pedido_original"] == pedido_pai.cod_pedido

        db.refresh(pedido_pai)
        assert str(pedido_pai.dat_prazo) == "2026-04-15"

    def test_error_sem_pedido_pai(self, db: Session, client: TestClient):
        teste_pedido_tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        teste_pedido_status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]

        payload = {
            "cod_pedido_tipo": teste_pedido_tipo.cod_pedido_tipo,
            "cod_unidade_analise": teste_unidade.cod_unidade,
            "cod_unidade_elo": teste_unidade.cod_unidade,
            "num_pedido": "COMP-002",
            "num_ano": 2026,
            "dat_emissao": "2026-03-15",
            "dsc_assunto": "Pedido complementar sem pai",
            "idn_processo": "PROC-COMP-002",
            "dat_prazo": "2026-04-15",
            "cod_pedido_status": teste_pedido_status.cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1,
        }

        response = client.post("/pedido/complementar", json=payload)

        assert_validation_error(response, fields=["body.cod_pedido_original"])

class TestListPedidosComplementares:
    def test_list_complementares_success(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]

        pedido_pai = PedidoModel(**PedidoFactory.build(
            cod_pedido_tipo=tipo.cod_pedido_tipo,
            cod_unidade_analise=unidade.cod_unidade,
            cod_pedido_status=status.cod_pedido_status,
            cod_pedido_original=None,
            num_pedido="PAI-100"
        ))
        db.add(pedido_pai)
        db.commit()
        db.refresh(pedido_pai)

        for i in range(3):
            filho = PedidoModel(**PedidoFactory.build(
                cod_pedido_tipo=tipo.cod_pedido_tipo,
                cod_unidade_analise=unidade.cod_unidade,
                cod_pedido_status=status.cod_pedido_status,
                cod_pedido_original=pedido_pai.cod_pedido,
                num_pedido=f"FILHO-{i}"
            ))
            db.add(filho)
        
        outro_pedido = PedidoModel(**PedidoFactory.build(num_pedido="OUTRO-999"))
        db.add(outro_pedido)
        
        db.commit()

        response = client.get(f"{PedidoFactory.URL}/complementares/{pedido_pai.cod_pedido}")

        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 3 
        
        for pedido in data:
            assert pedido["cod_pedido_original"] == pedido_pai.cod_pedido
            assert "FILHO-" in pedido["num_pedido"]
            assert "dsc_pedido_tipo" in pedido

    def test_list_complementares_empty(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        ppi = _seed_generic(db, PPIFactory, PPIModel, 1)[0]
        
        pedido_pai = PedidoModel(
            cod_ppi=ppi.cod_ppi,
            cod_pedido_tipo=tipo.cod_pedido_tipo,
            cod_pedido_original=None,
            cod_unidade_analise=unidade.cod_unidade,
            cod_unidade_elo=unidade.cod_unidade,
            num_pedido="PAI-VAZIO-001",
            num_ano=2026,
            dat_emissao=date(2026, 1, 1),
            dsc_assunto="Pedido pai sem filhos",
            idn_processo="PROC-PAI-VAZIO",
            dat_prazo=date(2026, 2, 1),
            cod_pedido_status=1,
            flg_reg_excluido=False,
            cif_usuario_inc=1,
            cif_usuario_alt=1,
        )
        db.add(pedido_pai)
        db.commit()
        db.refresh(pedido_pai)

        response = client.get(f"{PedidoFactory.URL}/complementares/{pedido_pai.cod_pedido}")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_success_com_pedido_pai(self, db: Session, client: TestClient):
        teste_ppi = _seed_generic(db, PPIFactory, PPIModel, 1)[0]
        teste_pedido_tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        teste_pedido_status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]

        pedido_pai = PedidoModel(
            cod_ppi=teste_ppi.cod_ppi,
            cod_pedido_tipo=teste_pedido_tipo.cod_pedido_tipo,
            cod_pedido_original=None,
            cod_unidade_analise=teste_unidade.cod_unidade,
            cod_unidade_elo=teste_unidade.cod_unidade,
            num_pedido="PAI-001",
            num_ano=2026,
            dat_emissao=date(2026, 3, 1),
            dsc_assunto="Pedido pai",
            idn_processo="PROC-PAI-001",
            dat_prazo=date(2026, 4, 1),
            cod_pedido_status=teste_pedido_status.cod_pedido_status,
            flg_reg_excluido=False,
            cif_usuario_inc=1,
            cif_usuario_alt=1,
        )
        db.add(pedido_pai)
        db.commit()
        db.refresh(pedido_pai)

        payload = {
            "cod_ppi": teste_ppi.cod_ppi,
            "cod_pedido_tipo": teste_pedido_tipo.cod_pedido_tipo,
            "cod_pedido_original": pedido_pai.cod_pedido,
            "cod_unidade_analise": teste_unidade.cod_unidade,
            "cod_unidade_elo": teste_unidade.cod_unidade,
            "num_pedido": "COMP-001",
            "num_ano": 2026,
            "dat_emissao": "2026-03-15",
            "dsc_assunto": "Pedido complementar",
            "idn_processo": "PROC-COMP-001",
            "dat_prazo": "2026-04-15",
            "cod_pedido_status": teste_pedido_status.cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1,
        }

        response = client.post("/pedido/complementar", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["cod_pedido_original"] == pedido_pai.cod_pedido

        db.refresh(pedido_pai)
        assert str(pedido_pai.dat_prazo) == "2026-04-15"

    def test_error_sem_pedido_pai(self, db: Session, client: TestClient):
        teste_pedido_tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        teste_unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        teste_pedido_status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]

        payload = {
            "cod_pedido_tipo": teste_pedido_tipo.cod_pedido_tipo,
            "cod_unidade_analise": teste_unidade.cod_unidade,
            "cod_unidade_elo": teste_unidade.cod_unidade,
            "num_pedido": "COMP-002",
            "num_ano": 2026,
            "dat_emissao": "2026-03-15",
            "dsc_assunto": "Pedido complementar sem pai",
            "idn_processo": "PROC-COMP-002",
            "dat_prazo": "2026-04-15",
            "cod_pedido_status": teste_pedido_status.cod_pedido_status,
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1,
        }

        response = client.post("/pedido/complementar", json=payload)

        assert_validation_error(response, fields=["body.cod_pedido_original"])

    def test_list_complementares_success(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        unidade = _seed_generic(db, UnidadeFactory, UnidadeModel, 1)[0]
        status = _seed_generic(db, StatusFactory, StatusModel, 1)[0]

        pedido_pai = PedidoModel(**PedidoFactory.build(
            cod_pedido_tipo=tipo.cod_pedido_tipo,
            cod_unidade_analise=unidade.cod_unidade,
            cod_pedido_status=status.cod_pedido_status,
            cod_pedido_original=None,
            num_pedido="PAI-100"
        ))
        db.add(pedido_pai)
        db.commit()
        db.refresh(pedido_pai)

        for i in range(3):
            filho = PedidoModel(**PedidoFactory.build(
                cod_pedido_tipo=tipo.cod_pedido_tipo,
                cod_unidade_analise=unidade.cod_unidade,
                cod_pedido_status=status.cod_pedido_status,
                cod_pedido_original=pedido_pai.cod_pedido,
                num_pedido=f"FILHO-{i}"
            ))
            db.add(filho)
        
        outro_pedido = PedidoModel(**PedidoFactory.build(num_pedido="OUTRO-999"))
        db.add(outro_pedido)
        
        db.commit()

        response = client.get(f"{PedidoFactory.URL}/complementares/{pedido_pai.cod_pedido}")

        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 3 
        
        for pedido in data:
            assert pedido["cod_pedido_original"] == pedido_pai.cod_pedido
            assert "FILHO-" in pedido["num_pedido"]
            assert "dsc_pedido_tipo" in pedido

    def test_list_complementares_empty(self, db: Session, client: TestClient):
        tipo = _seed_generic(db, TipoFactory, TipoModel, 1)[0]
        pedido_solitario = PedidoModel(**PedidoFactory.build(cod_pedido_tipo=tipo.cod_pedido_tipo, cod_pedido_original=None))
        db.add(pedido_solitario)
        db.commit()

        response = client.get(f"{PedidoFactory.URL}/complementares/{pedido_solitario.cod_pedido}")
        
        assert response.status_code == 200
        assert response.json() == []