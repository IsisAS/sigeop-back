from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class _HttpCodes:
    """
    Catálogo central de HTTP Status Codes.
    Uso: http.code.conflict
    """
    ok: int = 200
    created: int = 201
    no_content: int = 204

    bad_request: int = 400
    unauthorized: int = 401
    forbidden: int = 403
    not_found: int = 404
    conflict: int = 409
    unprocessable_entity: int = 422

    internal_server_error: int = 500


@dataclass(frozen=True)
class Http:
    """
    Namespace para padrões HTTP.
    Mantém 'code' como atributo para seu uso:
      http.code.conflict
    """
    code: _HttpCodes = _HttpCodes()


http = Http()
