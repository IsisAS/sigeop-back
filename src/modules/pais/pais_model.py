from sqlalchemy import String, Text, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Numeric
from datetime import datetime, date
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.common.sql_mixins import TimestampMixin
from src.db.base import Base
from datetime import datetime, timezone
from decimal import Decimal

class PaisModel(Base):
    __tablename__ = 'tb_pais'
    __table_args__ = (
        UniqueConstraint("cod_pais", "sig_pais", "nom_pais"),
        {"schema": "sigeop"}
    )

    cod_pais: Mapped[int] = mapped_column(primary_key=True)
    sig_pais: Mapped[str] = mapped_column(String(3), nullable = False)
    nom_pais: Mapped[str] = mapped_column(nullable = False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone()) 

    ufs: Mapped[list["UfModel"]] = relationship(back_populates="pais")