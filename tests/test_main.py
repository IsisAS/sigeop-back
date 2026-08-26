from fastapi.testclient import TestClient


class TestDocs:
    def test_swagger_ui(self, client: TestClient):
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

    def test_redoc(self, client: TestClient):
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()
