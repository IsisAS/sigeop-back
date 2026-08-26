from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

class MissaoTipoModel(Base):
    __tablename__ = "tb_missao_tipo"
    __table_args__ = {"schema": "sigeop"}
    
    cod_missao_tipo: Mapped[int] = mapped_column(Integer, primary_key=True)
    sig_missao_tipo: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    dsc_missao_tipo: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    missoes: Mapped[list["MissaoModel"]] = relationship(back_populates="tipo")
