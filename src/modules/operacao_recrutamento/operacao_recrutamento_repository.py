from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from src.modules.operacao.operacao_model import OperacaoModel
from src.modules.operacao.operacao_encarregado.operacao_encarregado_model import OperacaoEncarregadoModel
from src.modules.operacao.operacao_tipo.operacao_tipo_model import OperacaoTipoModel
from src.modules.operacao.operacao_status.operacao_status_model import OperacaoStatusModel
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel
from src.modules.caso.caso.caso_model import CasoModel

_SIG_OPERACAO_TIPO_RECRUTAMENTO = "AMPLIACAO_RECURSOS"
_SIG_RECURSO_TIPO_AGENTE_NAO_ORGANICO = "AGENTE_NAO_ORGANICO"


class OperacaoRecrutamentoRepository:
    """
    filtra por operacao_tipo.sig = 'AMPLIACAO_RECURSOS_OPERACIONAIS'
          E recurso_tipo.sig = 'AGENTE_NAO_ORGANICO'.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """
        Retorna a lista de operações de recrutamento já mapeadas como dicionários
        prontos para construção do DTO na camada de serviço.

        Cada dict contém:
          cod_operacao, nom_operacao, cod_caso, nom_caso,
          encarregado_cif, dsc_operacao_status, pode_editar
        """
        stmt = (
            select(
                OperacaoModel,
                OperacaoTipoModel.sig_operacao_tipo,
                OperacaoStatusModel.dsc_operacao_status,
                CasoModel.nom_caso,
            )
            .join(
                OperacaoTipoModel,
                OperacaoTipoModel.cod_operacao_tipo == OperacaoModel.cod_operacao_tipo,
            )
            .join(
                RecursoTipoModel,
                RecursoTipoModel.cod_recurso_tipo == OperacaoModel.cod_recurso_tipo,
            )
            .outerjoin(
                OperacaoStatusModel,
                OperacaoStatusModel.cod_operacao_status == OperacaoModel.cod_operacao_status,
            )
            .outerjoin(
                CasoModel,
                CasoModel.cod_caso == OperacaoModel.cod_caso,
            )
            .where(
                and_(
                    OperacaoTipoModel.sig_operacao_tipo == _SIG_OPERACAO_TIPO_RECRUTAMENTO,
                    RecursoTipoModel.sig_recurso_tipo == _SIG_RECURSO_TIPO_AGENTE_NAO_ORGANICO,
                    OperacaoModel.flg_reg_excluido == False,
                )
            )
            .order_by(OperacaoModel.cod_operacao)
            .limit(limit)
            .offset(offset)
        )

        rows = self.db.execute(stmt).all()

        result = []
        for operacao, sig_tipo, dsc_status, nom_caso in rows:
            titular = (
                self.db.query(OperacaoEncarregadoModel)
                .filter(
                    OperacaoEncarregadoModel.cod_operacao == operacao.cod_operacao,
                    OperacaoEncarregadoModel.flg_titular == True,
                    OperacaoEncarregadoModel.flg_reg_excluido == False,
                )
                .first()
            )

            result.append(
                {
                    "cod_operacao": operacao.cod_operacao,
                    "nom_operacao": operacao.nom_operacao,
                    "cod_caso": operacao.cod_caso,
                    "nom_caso": nom_caso,
                    "encarregado_cif": titular.cod_agente if titular else None,
                    "dsc_operacao_status": dsc_status,
                    "pode_editar": operacao.cod_caso is None,
                }
            )

        return result

    def contar(self) -> int:
        from sqlalchemy import func

        stmt = (
            select(func.count(OperacaoModel.cod_operacao))
            .join(
                OperacaoTipoModel,
                OperacaoTipoModel.cod_operacao_tipo == OperacaoModel.cod_operacao_tipo,
            )
            .join(
                RecursoTipoModel,
                RecursoTipoModel.cod_recurso_tipo == OperacaoModel.cod_recurso_tipo,
            )
            .where(
                and_(
                    OperacaoTipoModel.sig_operacao_tipo == _SIG_OPERACAO_TIPO_RECRUTAMENTO,
                    RecursoTipoModel.sig_recurso_tipo == _SIG_RECURSO_TIPO_AGENTE_NAO_ORGANICO,
                    OperacaoModel.flg_reg_excluido == False,
                )
            )
        )
        return self.db.execute(stmt).scalar_one()
