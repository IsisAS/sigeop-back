from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base 

class MissaoFonteHumanaModel(Base):
    __tablename__ = "tb_missao_fonte_humana"
    __table_args__ = {"schema": "sigeop"}
    
    cod_missao: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_missao.cod_missao"), primary_key=True)
    cod_fonte_humana: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_fonte_humana.cod_fonte_humana"), primary_key=True
    )
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    missao: Mapped["MissaoModel"] = relationship(back_populates="fontes_humanas")
    fonte_humana: Mapped["FonteHumanaModel"] = relationship()   