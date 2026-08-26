from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base

class MissaoEncarregadoModel(Base):
    __tablename__ = "tb_missao_encarregado"
    __table_args__ = {"schema": "sigeop"}
    
    cod_missao_encarregado: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_missao: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_missao.cod_missao"), nullable=False)
    flg_titular: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tip_papel: Mapped[str] = mapped_column(String(30), nullable=False, default="ENCARREGADO_SUPLENTE")
    dat_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    dat_fim: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    missao: Mapped["MissaoModel"] = relationship(back_populates="encarregados")
    cod_agente: Mapped[int] = mapped_column(nullable=False)
