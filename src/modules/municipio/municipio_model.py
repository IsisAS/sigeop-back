from sqlalchemy import String, Text, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Numeric
from datetime import datetime, date
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.common.sql_mixins import TimestampMixin
from src.db.base import Base
from datetime import datetime, timezone
from decimal import Decimal

class MunicipioModel(Base):
    __tablename__ = 'tb_municipio'
    __table_args__ = (
        UniqueConstraint("cod_municipio"),
        {"schema": "sigeop"}
    )

    cod_municipio: Mapped[int] = mapped_column(primary_key=True)
    cod_uf: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_uf.cod_uf"), nullable = False)
    nom_municipio: Mapped[str] = mapped_column(nullable = False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone()) 

    uf: Mapped["UfModel"] = relationship(back_populates="municipios")