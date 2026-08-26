from dataclasses import dataclass


@dataclass(frozen=True)
class _ErrorMessages:
    # Genéricos
    bad_request: str = "Requisição inválida."
    unauthorized: str = "Não autorizado."
    forbidden: str = "Acesso negado."
    not_found: str = "Recurso não encontrado."
    conflict: str = "Conflito de estado."
    internal_server_error: str = "Erro interno inesperado."
    validation_error: str = "Erro de validação nos dados enviados."

@dataclass(frozen=True)
class Messages:
    """
    Namespace de mensagens.
    Uso:
      msg.error.not_found
    """
    error: _ErrorMessages = _ErrorMessages()

msg = Messages()