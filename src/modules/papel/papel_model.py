from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class PapelModel(Base):
    __tablename__ = "tb_papel"
    __table_args__ = {"schema": "sigeop"}
    
    cod_papel: Mapped[int] = mapped_column(Integer, primary_key=True)
    dsc_papel: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    