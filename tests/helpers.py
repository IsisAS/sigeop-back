"""
Helpers reutilizáveis para testes.
"""

from src.core.config import settings
from src.db.base import Base
from datetime import datetime, date
from typing import Any
from src.modules.pedido.status.status_model import StatusModel
from src.modules.unidade.unidade_model import UnidadeModel
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped

BASE_URL = f"{settings.PREFIX_ROUTER}"

# =============================================================================
# Models de Teste (Mock)
# =============================================================================

class PedidoTematicaTestModel(Base):
    __tablename__ = "tb_pedido_tematica"
    __table_args__ = {"extend_existing": True}

    cod_tematica: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_tematica: Mapped[str] = mapped_column(String(120), nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow)

# =============================================================================
# Factories
# =============================================================================

class StatusFactory:
    """Factory para criar status dos pedidos via API."""
    URL = f"{BASE_URL}/pedido/status"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_pedido_status": n,
            "sig_pedido_status": f"status_{n}",
            "dsc_pedido_status": f"Status {n} desc",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class TipoFactory:
    """Factory para criar tipo de pedido via API."""
    URL = f"{BASE_URL}/pedido/tipo"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_pedido_tipo": n,
            "sig_pedido_tipo": f"TESTE_{n}",
            "dsc_pedido_tipo": f"Teste {n}",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class PPIFactory:
    """Factory para criar PPI (Plano Plurianual de Investimento) via API."""
    URL = f"{BASE_URL}/ppi"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        n = cls._next()
        payload = {
            "cod_unidade": 1,
            "num_ano": 2026,
            "nom_ppi": f"PPI Teste {n}",
            "idn_codigo_poa_sigiloso": f"POA-SIG-{n}",
            "idn_codigo_poa_ostensivo": f"POA-OST-{n}",
            "val_orcamento_sigiloso": 1000.00,
            "val_orcamento_ostensivo": 2000.00,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        payload.update(overrides)
        return payload

    @classmethod
    def reset(cls):
        cls._counter = 0
    
class PedidoFactory:
    """Factory para criar pedido via API."""
    URL = f"{BASE_URL}/pedido"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides: Any) -> dict[str, Any]:
        n = cls._next()
        payload = {
            "cod_ppi": 1,
            "cod_pedido_tipo": n,
            "cod_pedido_original": n,
            "cod_unidade_analise": n,
            "cod_unidade_elo": n,
            "num_pedido": f"PED-{n}",
            "num_ano": 2000 + n,
            "dat_emissao": date(2026, 1, 1),
            "dsc_assunto": f"Assunto teste {n}",
            "idn_processo": f"Processo SEI {n}",
            "dat_prazo": date(2026, 1, 1),
            "flg_reg_excluido": False,
            "cod_pedido_status": n,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
            "dat_hor_inclusao": datetime.utcnow(),
            "dat_hor_alteracao": datetime.utcnow(),
        }
        payload.update(overrides)
        return payload

    @classmethod
    def reset(cls):
        cls._counter = 0

class TematicaFactory:
    """Factory para criar tematica dos pedidos via API."""
    URL = f"{BASE_URL}/pedido/tematica"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_tematica": n,
            "nom_tematica": f"tematica {n}",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class UnidadeFactory:
    """Factory para criar unidade via API."""
    URL = f"{BASE_URL}/unidade"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_unidade": n,
            "idn_codigo_unidade": f"UNIT-{n}",
            "nom_unidade": f"Unidade Teste {n}",
            "sig_unidade": f"UT{n}",
            "cod_unidade_superior": None,
            "dat_inicio_vig": date(2026, 1, 1),
            "dat_fim_vig": date(2026, 1, 1),
            "flg_ativo": True,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class TematicaVinculoFactory:
    """Factory para criar tematicas do pedido via API."""
    URL = f"{BASE_URL}/pedido/tematica/vinculo"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 9
        return cls._counter
    
    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_pedido": n,
            "cod_tematica": n,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class AnalistaFactory:
    """Factory para criar analista via API."""
    URL = f"{BASE_URL}/pedido/analista"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 9
        return cls._counter
    
    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_pedido_analista": n,
            "cod_pedido": n,
            "cod_agente": n,
            "flg_titular": False,
            "dat_inicio": date.today(),
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class AgenteFactory:
    """Factory para criar um agente via API."""
    URL = f"{BASE_URL}/agente"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_unidade": n,
            "nom_agente": f"agente teste {n}",
            "cif_agente": f"CIF_{n}",
            "flg_ativo": True,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class CasoStatusFactory:
    """Factory para criar caso status via API."""

    URL = f"{BASE_URL}/caso/status"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        """Retorna um dict com dados do caso status (sem criar no banco)."""
        n = cls._next()
        defaults = {
            "cod_caso_status": n,
            "dsc_caso_status": f"caso status {n}",
            "sig_caso_status": f"caso status {n}",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        """Reseta o counter (chamado no conftest entre testes)."""
        cls._counter = 0

class CasoFactory:
    """Factory para criar caso via API."""

    URL = f"{BASE_URL}/caso"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        """Retorna um dict com dados do caso (sem criar no banco)."""
        n = cls._next()
        defaults = {
            "cod_pedido_abertura": n,
            "nom_caso": f"Teste do caso {n}",
            "dsc_caso": f"descricao caso {n}",
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
            "cod_caso_status": n,
            "encarregados": [],
            "pedidos_vinculados": []
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        """Reseta o counter (chamado no conftest entre testes)."""
        cls._counter = 0
        
class OperacaoTipoFactory:
    """Factory para listar um tipo via API."""
    URL = f"{BASE_URL}/operacao/tipo"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "sig_operacao_tipo": f"TIPO_OP_{n}",
            "dsc_operacao_tipo": f"Tipo Operação {n}",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class OperacaoStatusFactory:
    """Factory para listar um status via API."""
    URL = f"{BASE_URL}/operacao/status"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "sig_operacao_status": f"STATUS_OP_{n}",
            "dsc_operacao_status": f"Status Operação {n}",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n  
        }

        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class OperacaoFactory:
    """Factory para criar operacao via API."""
    URL = f"{BASE_URL}/operacao"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_operacao_tipo": n,
            "cod_caso": n,
            "cod_recurso_tipo": n,
            "cod_operacao_status": n,
            "nom_operacao": f"Operação Teste {n}",
            "dsc_operacao": f"Descrição da operação {n}",
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
            "encarregados": []
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class RecursoTipoFactory:
    """Factory para criar recurso tipo via API."""
    URL = f"{BASE_URL}/recurso/tipo"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "sig_recurso_tipo": f"RecursoTipo {n}",
            "dsc_recurso_tipo": f"RecursoTipo {n}",
            "flg_ativo": True,
            "flg_reg_excluido": False,
            "cif_usuario_inc": -1,
            "cif_usuario_alt": -1
        }
        defaults.update(overrides)
        return defaults


class MissaoTipoFactory:
    """Factory para criar tipo de missão via API."""
    URL = f"{BASE_URL}/missao/tipo"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_missao_tipo": n,
            "sig_missao_tipo": f"TIPO_MISSAO_{n}",
            "dsc_missao_tipo": f"Tipo Missão {n}",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class MissaoStatusFactory:
    """Factory para criar status de missão via API."""
    URL = f"{BASE_URL}/missao/status"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_missao_status": n,
            "sig_missao_status": f"STATUS_MISSAO_{n}",
            "dsc_missao_status": f"Status Missão {n}",
            "flg_ativo": True,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class MissaoFactory:
    """Factory para criar missão via API."""
    URL = f"{BASE_URL}/missao"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_missao_tipo": n,
            "cod_missao_status": n,
            "dsc_missao": f"Missao teste {n}",
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
            "encarregados": [],
            "fontes_humanas": []
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0
        

class PapelFactory:
    """FActory para cirar papel via API."""
    URL = f"{BASE_URL}/papel"
    _counter = 0
    
    @classmethod
    def _next(cls) -> int: 
        cls._counter += 1
        return cls._counter
    
    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "dsc_papel": f"Papel Teste{n}",
			"flg_ativo": True,
			"flg_reg_excluido": False,
			"cif_usuario_inc": n,
			"cif_usuario_alt": n
        }
        defaults.update(overrides)
        return defaults
    
    @classmethod
    def reset(cls):
        cls._counter = 0

class PlanoStatusFactory:
    """Factory para criar plano status via API."""
    URL = f"{BASE_URL}/plano/status"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "sig_plano_status": f"PLANEJADO_{n}",
            "dsc_plano_status": f"Status Plano {n}",
            "flg_ativo": True,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class PlanoTipoFactory:
    """Factory para criar plano tipo via API."""
    URL = f"{BASE_URL}/plano/tipo"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "sig_plano_tipo": f"OPERACIONAL_{n}",
            "dsc_plano_tipo": f"Tipo Plano {n}",
            "flg_ativo": True,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class PlanoFactory:
    """Factory para criar missão via API."""
    URL = f"{BASE_URL}/plano"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_plano_tipo": n,
            "cod_plano_status": n,
            "num_plano": f'Plano teste {n}',
            "num_ano": f'202{n}',
            "dat_emissao": date(2026, 1, 1),
            "dat_inicio": date(2026, 1, 1),
            "dat_termino": date(2026, 1, 2),
            "dsc_assunto": f'Descrição do Plano {n}',
            "dsc_local": f'Local do Plano {n}',
            "num_equipe": n,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class PlanoMissaoFactory:
    """Factory para criar plano vinculado a missão via API."""
    URL = f"{BASE_URL}/plano-missao"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_plano_tipo": n,
            "cod_plano_status": n,
            "cod_missao": n,
            "cod_unidade": n,
            "tip_plano_contexto": "MISSAO",
            "num_plano": f"PLANO-MISSAO-{n}",
            "num_ano": 2026,
            "dat_emissao": date(2026, 7, 7),
            "dat_inicio": date(2026, 7, 8),
            "dat_termino": date(2026, 7, 9),
            "dsc_assunto": f"Assunto do plano missao {n}",
            "flg_reg_excluido": False,
            "cif_usuario_inc": 1,
            "cif_usuario_alt": 1,
            "plano_equipe": [],
            "local": [
                {
                    "cod_pais": n,
                    "cod_uf": n,
                    "cod_municipio": n,
                    "dsc_local": f"Local da missao {n}",
                    "flg_reg_excluido": False,
                    "cif_usuario_inc": 1,
                    "cif_usuario_alt": 1,
                }
            ],
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0

class PPIFactory:
    """Factory para criar PPI via API."""
    URL = f"{BASE_URL}/ppi"
    _counter = 0

    @classmethod
    def _next(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def build(cls, **overrides) -> dict:
        n = cls._next()
        defaults = {
            "cod_unidade": n,
            "num_ano": n,
            "nom_ppi":  f"PPI teste {n}",
            "idn_codigo_poa_sigiloso":  f"Codigo poa sigiloso {n}",
            "idn_codigo_poa_ostensivo":  f"Codigo poa ostensivo {n}",
            "val_orcamento_sigiloso":  10.00,
            "val_orcamento_ostensivo":  10.00,
            "flg_reg_excluido": False,
            "cif_usuario_inc": n,
            "cif_usuario_alt": n,
        }
        defaults.update(overrides)
        return defaults

    @classmethod
    def reset(cls):
        cls._counter = 0
        

# =============================================================================
# Assertions RFC 7807
# =============================================================================

def assert_problem_json(response, *, status: int, error_type: str):
    """Valida que a resposta segue RFC 7807."""
    assert response.status_code == status
    assert response.headers["content-type"] == "application/problem+json"
    data = response.json()
    assert data["type"] == error_type
    assert data["status"] == status
    assert "title" in data
    assert "detail" in data
    assert "instance" in data
    return data

def assert_not_found(response):
    return assert_problem_json(response, status=404, error_type="/errors/not-found")

def assert_conflict(response):
    return assert_problem_json(response, status=409, error_type="/errors/conflict")

def assert_validation_error(response, *, fields: list[str] | None = None):
    data = assert_problem_json(response, status=422, error_type="/errors/validation-error")
    assert "errors" in data
    assert isinstance(data["errors"], list)
    if fields:
        response_fields = [e["field"] for e in data["errors"]]
        for f in fields:
            assert f in response_fields, f"Campo '{f}' não encontrado em {response_fields}"
    return data

def assert_internal_error(response, *, has_debug: bool = True):
    data = assert_problem_json(response, status=500, error_type="/errors/internal-server-error")
    if has_debug:
        assert "debug" in data
        assert "exception" in data["debug"]
        assert "stacktrace" in data["debug"]
    return data
