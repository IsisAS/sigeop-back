from src.cache.redis import CacheService
from src.core.config import settings
from src.integrations.ciclo.ciclo_client import CicloClient
from src.integrations.ciclo.ciclo_schema import UnidadeSchema, ServidorSchema


class CicloService:
    def __init__(self, client: CicloClient, cache: CacheService):
        self.client = client
        self.cache = cache

    # ---------- Unidades ---------- ciclo nao comporta busca por mais de 1 id
    def sync_unidades(self) -> list[dict]:
        return self._unidades_list()

     # ---------- Unidades PPI ---------- ciclo nao comporta busca por mais de 1 id
    def get_unidades_ppi(self) -> list[dict]:
        return self._unidades_list()
    
    def _unidades_list(self) -> list[dict]:
        unidades = []

        unidadeDci = self.client.fetch_unidade_por_cod(122000)
        unidadeDint = self.client.fetch_unidade_por_cod(121000)
        unidadeDiex = self.client.fetch_unidade_por_cod(123000)
        unidadeDoint = self.client.fetch_unidade_por_cod(124000)

        unidades = [unidadeDci, unidadeDint, unidadeDiex, unidadeDoint]

        return unidades

    def get_unidades_analise(self, *, codigo: int | None = None) -> list[dict]:
        unidades = []
        
        if codigo == None:
            unidades = self.sync_unidades()
        else:
            unidade = self.client.fetch_unidade_por_cod(codigo)
            unidades.append(unidade)

        return unidades

    def get_unidades_destinatarias(self, *,  nome: str | None = "SUPER") -> list[dict]:
        unidadesDestinatarias = []
        unidadeDoint = self.client.get_unidade_hierarquia_by_cod(124200) # Codigo Doint
        superintendencias = self.client.fetch_superintendencias(nome)

        return [*self._unidades(unidadeDoint),*self._unidades(superintendencias)]

    @staticmethod
    def _unidades(resp: dict) -> list[dict]:
        return (resp or {}).get("_embedded", {}).get("unidades", [])

    def get_superintendencias(self, *,  nome: int | None = "SUPER") -> list[dict]:
        return self.client.fetch_superintendencias(nome)

    def get_unidades(self, *, codigo: int | None = None) -> list[dict]:
        unidades = []
        
        if codigo == None:
            unidades = self.sync_unidades()
        else:
            unidade = self.client.fetch_unidade_por_cod(codigo)
            unidades.append(unidade)

        return unidades

    def get_unidade_hierarquia(self, *, codigo: int | None = None) -> list[dict]:
        unidades = []
        if codigo != None:
            unidade = self.client.get_unidade_hierarquia_by_cod(codigo)
            unidades.append(unidade)

        return unidades

    # ---------- Servidores ----------
    def sync_servidores(self, codigo_unidade: str) -> list[dict]:
        raw = self.client.fetch_servidores_by_unidade(codigo_unidade)
        servidores_raw = raw.get("_embedded", {}).get("servidores", [])
        servidores = [
            ServidorSchema(**item).model_dump()
            for item in servidores_raw
        ]
        #self.cache.set("ciclo:servidores", servidores, ttl=settings.CICLO_CACHE_TTL)
        return servidores

    def get_servidores_by_unidade(self, codigo_unidade: int) -> list[dict]:
        #servidores = self.cache.get("ciclo:servidores")
        cod_unidade_str = str(codigo_unidade)
        servidores = self.sync_servidores(cod_unidade_str)
        return servidores

    def get_servidor_by_cif(self, cod_agente: int) -> dict:
        cif = str(cod_agente)
        servidor = self.client.get_servidor_by_cif(cif)
        if(servidor):
            return servidor