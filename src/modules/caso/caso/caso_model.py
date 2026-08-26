from sqlalchemy import Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from src.db.base import Base

class CasoModel(Base):
    __tablename__ = 'tb_caso'
    __table_args__ = {"schema": "sigeop"}

    cod_caso: Mapped[int] = mapped_column(primary_key=True)
    cod_pedido_abertura: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_pedido.cod_pedido"), nullable=False, unique=True)
    nom_caso: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    dsc_caso: Mapped[str] = mapped_column(Text)
    cod_caso_status: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_caso_status.cod_caso_status"))
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).astimezone()) 

    pedido_abertura: Mapped["PedidoModel"] = relationship(foreign_keys=[cod_pedido_abertura], back_populates="casos_abertos")
    pedidos_vinculados: Mapped[list["CasoPedidoModel"]] = relationship(back_populates="caso")
    
    caso_status: Mapped["CasoStatusModel"] = relationship(back_populates="casos")
    encarregados: Mapped[list["CasoEncarregadoModel"]] = relationship(back_populates="caso")
    operacoes: Mapped[list["OperacaoModel"]] = relationship(back_populates="caso")
    missoes: Mapped[list["MissaoModel"]] = relationship(back_populates="caso")
    
