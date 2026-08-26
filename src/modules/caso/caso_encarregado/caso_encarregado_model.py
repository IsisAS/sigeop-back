from sqlalchemy import String, Text, Boolean, DateTime, Date
from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.common.sql_mixins import TimestampMixin
from src.db.base import Base
from datetime import datetime, timezone 

class CasoEncarregadoModel(Base):
    __tablename__ = 'tb_caso_encarregado'
    __table_args__ = {"schema": "sigeop"}

    cod_caso_encarregado: Mapped[int] = mapped_column(primary_key=True)
    cod_caso: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_caso.cod_caso"))
    cod_agente: Mapped[int] = mapped_column(nullable=False)
    flg_titular: Mapped[bool] = mapped_column(Boolean, default=False)
    dat_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone()) 

    caso: Mapped["CasoModel"] = relationship(back_populates="encarregados")
