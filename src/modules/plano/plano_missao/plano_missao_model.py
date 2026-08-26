from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class PlanoMissaoModel(Base):
    __tablename__ = "tb_plano_missao"
    __table_args__ = {"schema": "sigeop"}

    cod_plano: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_plano.cod_plano"), primary_key=True)
    cod_missao: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_missao.cod_missao"), primary_key=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(Integer, nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(Integer, nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
