from sqlalchemy import String, Text, Boolean, DateTime, Date
from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.sql_mixins import TimestampMixin
from src.db.base import Base
from src.modules.ppi.ppi_model import PPIModel


class UnidadeModel(Base):
    __tablename__ = 'tb_unidade'
    __table_args__ = {"schema": "sigeop"}

    cod_unidade: Mapped[int] = mapped_column(primary_key=True)
    idn_codigo_unidade: Mapped[str] = mapped_column(String(30), nullable=False)
    nom_unidade: Mapped[str] = mapped_column(Text, nullable=False)
    sig_unidade: Mapped[str] = mapped_column(String(30), nullable=False)
    cod_unidade_superior: Mapped[int] = mapped_column(nullable=True)
    dat_inicio_vig: Mapped[date] = mapped_column(Date, nullable=False)
    dat_fim_vig: Mapped[date] = mapped_column(Date, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
