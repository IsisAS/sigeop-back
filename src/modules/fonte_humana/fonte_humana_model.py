from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class FonteHumanaModel(Base):
    __tablename__ = "tb_fonte_humana"
    __table_args__ = {"schema": "sigeop"}
    
    cod_fonte_humana: Mapped[int] = mapped_column(Integer, primary_key=True)
    sig_fonte_humana: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    cod_agente_controlador: Mapped[int] = mapped_column(nullable=False)
    cod_agente_controlador_substituto: Mapped[int | None] = mapped_column(nullable=True)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)    
