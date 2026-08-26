from sqlalchemy import String, Text, Boolean, DateTime, UniqueConstraint, Date
from datetime import datetime, date, timezone
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.db.base import Base

class PlanoTipoModel(Base):
    __tablename__ = 'tb_plano_tipo'
    __table_args__ = (
        UniqueConstraint("cod_plano_tipo"),
        {"schema": "sigeop"}
    )

    cod_plano_tipo: Mapped[int] = mapped_column(primary_key=True)
    sig_plano_tipo: Mapped[str] = mapped_column(String(60), nullable=False)
    dsc_plano_tipo: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone()) 

    planos: Mapped[list["PlanoModel"]] = relationship(back_populates="plano_tipo")