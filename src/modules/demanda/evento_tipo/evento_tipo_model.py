from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base 

class EventoTipoModel(Base):
    __tablename__ = "tb_evento_tipo"
    __table_args__ = {"schema": "sigeop"}
    
    cod_evento_tipo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sig_evento_tipo: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    dsc_evento_tipo: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    demandas: Mapped[list["DemandaModel"]] = relationship(back_populates="tipo_evento")
