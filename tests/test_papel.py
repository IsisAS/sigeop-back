from fastapi.testclient import TestClient 
from tests.helpers import PapelFactory, assert_not_found

class TestPapel:
    def test_list_papeis(self, client: TestClient):
        # Criamos 03 papeis para garantir que a lista não esteja vazia
        client. post(PapelFactory.URL, json=PapelFactory.build(dsc_papel="Papel A"))
        client. post(PapelFactory.URL, json=PapelFactory.build(dsc_papel="Papel B"))
        client. post(PapelFactory.URL, json=PapelFactory.build(dsc_papel="Papel C"))        
        
        response = client.get(PapelFactory.URL)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3
        # Como o seu repository ordena por dsc_papel, o "Papel A" deve ser o primeiro
        assert data[0]["dsc_papel"] == "Papel A"
    
    def test_create_papel(self, client: TestClient):
        payload = PapelFactory.build(dsc_papel = "Novo Papel")
        response = client.post(PapelFactory.URL, json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["dsc_papel"] == "Novo Papel"
        assert "cod_papel" in data
        assert data["status"] == "Ativo"
        
    def test_get_papel(self, client: TestClient):
        # Primeiro criamos um papel para pegar um ID válido
        create_res = client.post(PapelFactory.URL, json=PapelFactory.build(dsc_papel="Buscar Teste"))
        papel_id = create_res.json()["cod_papel"]   
        
        # Agora buscarmos por ID real
        response = client.get(f"{PapelFactory.URL}/{papel_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["cod_papel"] == papel_id
        assert data["dsc_papel"] == "Buscar Teste"
        
    def test_get_papel_not_found(self, client: TestClient):
        response = client.get(f"{PapelFactory.URL}/9999")
        assert_not_found(response)
        
    def test_update_papel(self, client: TestClient):
        # Primeiro criamos um papel para poder alterá-lo
        create_res = client.post(PapelFactory.URL, json=PapelFactory.build(dsc_papel="Original"))
        papel_id = create_res.json()["cod_papel"]
        
        payload = PapelFactory.build(
            dsc_papel="Alterado",
            flg_ativo=False,
            flg_reg_excluido=True
        )
        response = client.put(f"{PapelFactory.URL}/{papel_id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["dsc_papel"] == "Alterado"
        assert data["status"] == "Inativo"
        
    def test_update_papel_not_found(self, client: TestClient):
        payload = PapelFactory.build()
        response = client.put(f"{PapelFactory.URL}/9999", json=payload)
        assert_not_found(response)