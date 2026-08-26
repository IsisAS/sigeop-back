from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class OperacaoPedidoModel(Base):
    __tablename__ = "tb_operacao_pedido"
    __table_args__ = {"schema": "sigeop"}

    cod_operacao: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_operacao.cod_operacao"),
        primary_key=True,
    )
    cod_pedido: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_pedido.cod_pedido"),
        primary_key=True,
    )
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(Integer, nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(Integer, nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
