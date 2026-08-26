from sqlalchemy import String, Text, Boolean
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class StatusModel(Base):
    __tablename__ = 'tb_pedido_status'
    __table_args__ = {"schema": "sigeop"}

    cod_pedido_status: Mapped[int] = mapped_column(primary_key=True)
    sig_pedido_status: Mapped[str] = mapped_column(String(60), nullable=False)
    dsc_pedido_status: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)