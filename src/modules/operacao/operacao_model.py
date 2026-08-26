from sqlalchemy import String, Text, Boolean, DateTime, Date, ForeignKey, Identity, Integer, UniqueConstraint
from datetime import datetime, date
from src.common.sql_mixins import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base
from src.modules.recurso_tipo.recurso_tipo_model import RecursoTipoModel
class OperacaoModel(Base):
    __tablename__ = 'tb_operacao'
    __table_args__ = (
        UniqueConstraint("cod_operacao"),
        {"schema": "sigeop"}
    )
     
    cod_operacao: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    cod_operacao_tipo: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_operacao_tipo.cod_operacao_tipo"), nullable = False)
    cod_caso: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_caso.cod_caso"), nullable = True)
    cod_recurso_tipo: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_recurso_tipo.cod_recurso_tipo"), nullable = True)
    nom_operacao: Mapped[str] = mapped_column(Text, nullable = False, unique=True)
    dsc_operacao: Mapped[str] = mapped_column(Text, nullable = True)
    cod_operacao_status: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_operacao_status.cod_operacao_status"), nullable = True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable = False, default = False)
    dsc_justificativa_exclusao: Mapped[str | None] = mapped_column(Text, nullable = True)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable = False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable = False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    caso: Mapped["CasoModel"] = relationship(back_populates = "operacoes")
    encarregados: Mapped[list["OperacaoEncarregadoModel"]] = relationship(back_populates="operacao")
    tipo_operacao = relationship("OperacaoTipoModel", back_populates = "operacoes")
    status_operacao = relationship("OperacaoStatusModel", back_populates = "operacoes")
    
    missoes: Mapped[list["MissaoModel"]] = relationship(back_populates="operacao")
    # planos: Mapped[list["PlanoModel"]] = relationship(back_populates="operacao")
    pedidos: Mapped[list["OperacaoPedidoModel"]] = relationship()
    recurso_tipo: Mapped[list["RecursoTipoModel"]] = relationship(back_populates="operacoes")
