import httpx

from src.core.config import settings
from src.core.errors.errors import InternalServerError

class CicloClient:
    def __init__(self):
        self.base_url = settings.CICLO_BASE_URL
        self.headers = {"X-API-Key": settings.CICLO_API_KEY}

    def fetch_unidade_por_cod(self, codigo: int) -> dict:
        url = f"{self.base_url}/unidades/{codigo}"
        return self._get(url)

    def fetch_all_unidades(self) -> dict:
        url = f"{self.base_url}/unidades?size=10000"
        return self._get(url)

    def fetch_all_unidades(self) -> dict:
        url = f"{self.base_url}/unidades?size=10000"
        return self._get(url)

    def fetch_servidores(self) -> dict:
        url = f"{self.base_url}/servidores"
        return self._get(url)

    def fetch_servidores_by_unidade(self, cod_unidade: str) -> dict:
        url = f"{self.base_url}/servidores?unidade={cod_unidade}"
        return self._get(url)

    def get_servidor_by_cif(self, cif: str) -> dict:
        url = f"{self.base_url}/servidores?cif={cif}"
        return self._get(url)

    def get_unidade_hierarquia_by_cod(self, codigo: int) -> dict:
        url = f"{self.base_url}/unidades/{codigo}/hierarquia"
        return self._get(url)

    def fetch_superintendencias(self, nome: str | None = None) -> dict:
        url = f"{self.base_url}/unidades?size=10000"
        if nome:
            url += f"&nome={nome}"
        return self._get(url)

    def health_check(self) -> bool:
        url = f"{self.base_url}/health"
        try:
            with httpx.Client(verify=False) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                return data.get("status") == "ok"
        except Exception:
            return False

    def _get(self, url: str) -> dict:
        try:
            with httpx.Client(verify=False) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise InternalServerError(
                f"Ciclo API retornou status {e.response.status_code}"
            )
        except httpx.RequestError as e:
            raise InternalServerError(
                f"Falha ao conectar com Ciclo API: {e}"
            )