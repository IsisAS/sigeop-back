from sqlalchemy import String, Text, Boolean, DateTime, Date
from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class AnalistaModel(Base):
    __tablename__ = 'tb_pedido_analista'
    __table_args__ = {"schema": "sigeop"}

    cod_pedido_analista: Mapped[int] = mapped_column(primary_key=True)
    cod_pedido: Mapped[int] = mapped_column(nullable=False)
    cod_agente: Mapped[int] = mapped_column(nullable=False)
    flg_titular: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    dat_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)