from sqlalchemy import Text, Boolean, DateTime, Date, ForeignKey, Identity, Integer, String, Text, UniqueConstraint
from datetime import datetime, date, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base

class PlanoStatusModel(Base):
    __tablename__ = 'tb_plano_status'
    __table_args__ = (
        UniqueConstraint("cod_plano_status"),
        {"schema": "sigeop"}
    )
    
    cod_plano_status: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    sig_plano_status: Mapped[str] = mapped_column(String(60), nullable=False, unique = True)
    dsc_plano_status: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable = False, default = True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable = False, default = False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable = False) 
    cif_usuario_alt: Mapped[int] = mapped_column(nullable = False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    
    
    planos: Mapped[list["PlanoModel"]] = relationship(back_populates="plano_status")