from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Identity, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base

class PedidoModel(Base):
    __tablename__ = 'tb_pedido'
    __table_args__ = (
        UniqueConstraint("num_pedido", "num_ano", "cod_unidade_analise", name="uq_tb_pedido_num_ano_unidade"),
        {"schema": "sigeop"}
    )
    
    cod_pedido: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    cod_ppi: Mapped[int] = mapped_column(Integer, ForeignKey("sigeop.tb_ppi.cod_ppi"), nullable=False)
    cod_pedido_relacionado: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("sigeop.tb_pedido.cod_pedido"),
        nullable=True,
    )
    
    cod_unidade_analise: Mapped[int] = mapped_column(nullable=False)
    sig_unidade_analise: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_unidade_analise: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade_analise: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    cod_unidade_elo: Mapped[int | None] = mapped_column(nullable=True)
    sig_unidade_elo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_unidade_elo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade_elo: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    num_pedido: Mapped[str] = mapped_column(String(20), nullable=False)
    num_ano: Mapped[int] = mapped_column(nullable=False)
    dat_emissao: Mapped[date] = mapped_column(Date, nullable=False)
    dsc_assunto: Mapped[str | None] = mapped_column(Text, nullable=True)
    dsc_tematica: Mapped[str | None] = mapped_column(Text, nullable=True)
    idn_processo: Mapped[str | None] = mapped_column(String(40), nullable=True)
    dat_prazo: Mapped[date] = mapped_column(Date, nullable=False)
    
    cod_pedido_status: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey("sigeop.tb_pedido_status.cod_pedido_status"), 
        nullable=True
    )

    pedido_status: Mapped["StatusModel | None"] = relationship()
    
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dsc_justificativa_exclusao: Mapped[str] = mapped_column(Text, nullable=True)
    casos_abertos: Mapped[list["CasoModel"]] = relationship(foreign_keys="[CasoModel.cod_pedido_abertura]", back_populates="pedido_abertura")
    missoes: Mapped[list["MissaoModel"]] = relationship(back_populates="pedido")
    casos_vinculados: Mapped[list["CasoPedidoModel"]] = relationship(back_populates="pedido")

