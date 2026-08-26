from sqlalchemy import String, Text, Boolean, DateTime, Date
from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.common.sql_mixins import TimestampMixin
from src.db.base import Base
from datetime import datetime, timezone 

class CasoStatusModel(Base):
    __tablename__ = 'tb_caso_status'
    __table_args__ = {"schema": "sigeop"}

    cod_caso_status: Mapped[int] = mapped_column(primary_key=True)
    sig_caso_status: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    dsc_caso_status: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone()) 
    
    casos: Mapped[list["CasoModel"]] = relationship(back_populates="caso_status")