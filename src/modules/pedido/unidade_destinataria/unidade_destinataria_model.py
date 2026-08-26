from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base 

class UnidadeDestinatariaModel(Base):
    __tablename__ = 'tb_pedido_unidade_destinataria'
    __table_args__ = { "schema": "sigeop" }
    
    cod_pedido_unidade_destinataria: Mapped[int] = mapped_column(primary_key=True)
    cod_pedido: Mapped[int] = mapped_column(nullable=False)
    cod_unidade_destinataria: Mapped[int] = mapped_column(nullable=False)
    sig_unidade_destinataria: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_unidade_destinataria: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade_destinataria: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)