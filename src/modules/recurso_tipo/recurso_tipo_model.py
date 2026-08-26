from sqlalchemy import String, Text, Boolean, DateTime, Date, ForeignKey, Identity, Integer, UniqueConstraint
from datetime import datetime, date
from src.common.sql_mixins import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base

class RecursoTipoModel(Base):
    __tablename__ = 'tb_recurso_tipo'
    __table_args__ = (
        UniqueConstraint("cod_recurso_tipo"),
        {"schema": "sigeop"}
    )
     
     
    cod_recurso_tipo: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    sig_recurso_tipo: Mapped[str] = mapped_column(String(60), nullable=False, unique = True)
    dsc_recurso_tipo: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable = False, default = True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable = False, default = False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable = False) 
    cif_usuario_alt: Mapped[int] = mapped_column(nullable = False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    operacoes: Mapped[list["OperacaoModel"]] = relationship()
    missoes: Mapped[list["MissaoModel"]] = relationship(back_populates="recurso_tipo")
