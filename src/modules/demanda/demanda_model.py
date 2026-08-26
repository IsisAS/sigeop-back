from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Identity, Integer, Text 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base 

class DemandaModel(Base):
    __tablename__ = "tb_demanda"
    __table_args__ = {"schema": "sigeop"}
    
    cod_demanda: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cod_operacao: Mapped[int | None] = mapped_column(ForeignKey("sigeop.tb_operacao.cod_operacao"), nullable=True)
    cod_tipo_evento_demanda: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_evento_tipo.cod_evento_tipo"), nullable=False)
    dsc_responsavel: Mapped[str] = mapped_column(Text, nullable=False)
    dsc_atividade: Mapped[str] = mapped_column(Text, nullable=False)
    dat_inicio_evento: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dat_fim_evento: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    dsc_justificativa_exclusao: Mapped[str | None] = mapped_column(Text, nullable=True)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    tipo_evento: Mapped["EventoTipoModel"] = relationship(back_populates="demandas")

    demanda_local: Mapped[list["DemandaLocalModel"]] = relationship(
        back_populates="demanda", cascade="all, delete-orphan"
    )
