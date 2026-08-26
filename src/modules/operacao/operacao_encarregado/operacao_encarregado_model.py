from sqlalchemy import Text, Boolean, DateTime, Date, ForeignKey, Identity, Integer
from datetime import datetime, date
from src.common.sql_mixins import TimestampMixin
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base

class OperacaoEncarregadoModel(Base):
    __tablename__ = 'tb_operacao_encarregado'
    __table_args__ = {"schema": "sigeop"}
    
    cod_operacao_encarregado: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    cod_operacao: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_operacao.cod_operacao"), nullable = False)
    cod_agente: Mapped[int] = mapped_column(nullable = False)
    flg_titular: Mapped[bool] = mapped_column(Boolean, nullable = False, default = False)
    dat_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable = False, default=datetime.utcnow)
    dat_fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable = False, default = False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable = False) 
    cif_usuario_alt: Mapped[int] = mapped_column(nullable = False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    operacao: Mapped["OperacaoModel"] = relationship(back_populates="encarregados")
