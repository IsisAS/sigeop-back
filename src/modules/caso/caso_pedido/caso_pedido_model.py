from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from src.db.base import Base

class CasoPedidoModel(Base):
    __tablename__ = 'tb_caso_pedido'
    __table_args__ = {"schema": "sigeop"}

    cod_caso: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_caso.cod_caso"), primary_key=True)
    cod_pedido: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_pedido.cod_pedido"), primary_key=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).astimezone())

    caso: Mapped["CasoModel"] = relationship(back_populates="pedidos_vinculados")
    pedido: Mapped["PedidoModel"] = relationship(back_populates="casos_vinculados")