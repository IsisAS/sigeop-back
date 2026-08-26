from sqlalchemy import String, Text, Boolean, DateTime, UniqueConstraint, Date, ForeignKey
from datetime import datetime, date, timezone
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.db.base import Base

class PlanoEquipeModel(Base):
    __tablename__ = 'tb_plano_equipe'
    __table_args__ = (
        UniqueConstraint("cod_plano_equipe"),
        {"schema": "sigeop"}
    )

    cod_plano_equipe: Mapped[int] = mapped_column(primary_key=True)
    cod_plano: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_plano.cod_plano"), nullable = False)
    cod_agente: Mapped[int] = mapped_column(nullable=False)
    cod_papel: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_papel.cod_papel"), nullable = False)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone()) 

    plano: Mapped["PlanoModel"] = relationship(back_populates="plano_equipe")