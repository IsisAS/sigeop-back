from sqlalchemy import String, Text, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Numeric, event
from datetime import datetime, date
from sqlalchemy.orm import Mapped, relationship, mapped_column, object_session
from src.common.sql_mixins import TimestampMixin
from src.db.base import Base
from datetime import datetime, timezone
from decimal import Decimal
from src.core.errors.errors import ConflictError

class PPIModel(Base):
    __tablename__ = 'tb_ppi'
    __table_args__ = (
        UniqueConstraint("cod_ppi"),
        {"schema": "sigeop"}
    )

    cod_ppi: Mapped[int] = mapped_column(primary_key=True)
    num_ppi: Mapped[int] = mapped_column(nullable=False)
    cod_unidade: Mapped[int] = mapped_column(nullable=False)
    sig_unidade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_unidade: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    num_ano: Mapped[int] = mapped_column(nullable=False)
    nom_ppi: Mapped[str] = mapped_column(String, nullable=False)
    idn_codigo_poa_sigiloso: Mapped[str] = mapped_column(String(60), nullable=False)
    idn_codigo_poa_ostensivo: Mapped[str] = mapped_column(String(60), nullable=False)
    val_orcamento_sigiloso: Mapped[Decimal] = mapped_column(Numeric(precision=14, scale=2),nullable=True)
    val_orcamento_ostensivo: Mapped[Decimal] = mapped_column(Numeric(precision=14, scale=2),nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc).astimezone())

@event.listens_for(PPIModel, 'before_insert')
@event.listens_for(PPIModel, 'before_update')
def validar_ppi(mapper, connection, target):
    if not all([target.num_ppi, target.num_ano, target.cod_unidade]):
        return

    session = object_session(target)
    if not session:
        return
    
    existing = session.query(PPIModel).filter(
        PPIModel.num_ppi == target.num_ppi,
        PPIModel.num_ano == target.num_ano,
        PPIModel.cod_unidade == target.cod_unidade,
    )

    if target.cod_ppi:
        existing = existing.filter(PPIModel.cod_ppi != target.cod_ppi)
    
    if existing.first():
        raise ConflictError("Já existe um PPI com essa combinação de número, unidade e ano.")
