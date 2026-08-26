from sqlalchemy import String, Text, Boolean, DateTime, UniqueConstraint, Date, ForeignKey
from datetime import datetime, date, timezone
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.db.base import Base
from src.modules.pais.pais_model import PaisModel
from src.modules.uf.uf_model import UfModel
from src.modules.municipio.municipio_model import MunicipioModel

class PlanoLocalModel(Base):
    __tablename__ = 'tb_plano_local'
    __table_args__ = (
        UniqueConstraint("cod_plano_local"),
        {"schema": "sigeop"}
    )

    cod_plano_local: Mapped[int] = mapped_column(primary_key=True)
    cod_plano: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_plano.cod_plano"), nullable = False)
    cod_pais: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_pais.cod_pais"), nullable = False)
    cod_uf: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_uf.cod_uf"), nullable = True)
    cod_municipio: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_municipio.cod_municipio"), nullable = True)
    dsc_local: Mapped[str]=mapped_column(String, nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone()) 

    plano: Mapped["PlanoModel"] = relationship(back_populates="local")