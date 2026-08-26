from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Identity, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


def _now() -> datetime:
    return datetime.now(timezone.utc).astimezone()


class RelatorioTipoModel(Base):
    __tablename__ = "tb_relatorio_tipo"
    __table_args__ = {"schema": "sigeop"}

    cod_relatorio_tipo: Mapped[int] = mapped_column(Integer, primary_key=True)
    sig_relatorio_tipo: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    dsc_relatorio_tipo: Mapped[str] = mapped_column(Text, nullable=False)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(Integer, nullable=False, default=-1)
    cif_usuario_alt: Mapped[int] = mapped_column(Integer, nullable=False, default=-1)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class RelatorioStatusModel(Base):
    __tablename__ = "tb_relatorio_status"
    __table_args__ = {"schema": "sigeop"}

    cod_relatorio_status: Mapped[int] = mapped_column(
        Integer, Identity(always=True), primary_key=True
    )
    sig_relatorio_status: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    dsc_relatorio_status: Mapped[str] = mapped_column(Text, nullable=False)
    num_ordem: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    flg_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(Integer, nullable=False, default=-1)
    cif_usuario_alt: Mapped[int] = mapped_column(Integer, nullable=False, default=-1)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class RelatorioModel(Base):
    __tablename__ = "tb_relatorio"
    __table_args__ = (
        UniqueConstraint("num_relatorio", "num_ano", name="uq_tb_relatorio_num_ano"),
        {"schema": "sigeop"},
    )

    cod_relatorio: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    cod_relatorio_tipo: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_relatorio_tipo.cod_relatorio_tipo"), nullable=False
    )
    cod_relatorio_status: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_relatorio_status.cod_relatorio_status"), nullable=False
    )
    cod_unidade: Mapped[int] = mapped_column(Integer, nullable=False)
    sig_unidade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_unidade: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    num_relatorio: Mapped[str] = mapped_column(String(20), nullable=False)
    num_ano: Mapped[int] = mapped_column(Integer, nullable=False)
    dat_emissao: Mapped[date] = mapped_column(Date, nullable=False)
    dsc_assunto: Mapped[str] = mapped_column(Text, nullable=False)
    idn_processo: Mapped[str] = mapped_column(String(40), nullable=False)
    idn_agente_nao_organico: Mapped[str | None] = mapped_column(Text, nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(Integer, nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(Integer, nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    tipo: Mapped[RelatorioTipoModel] = relationship()
    status: Mapped[RelatorioStatusModel] = relationship()
    difusoes: Mapped[list["RelatorioDifusaoModel"]] = relationship(
        back_populates="relatorio", cascade="all, delete-orphan"
    )
    pedidos: Mapped[list["RelatorioPedidoModel"]] = relationship(
        back_populates="relatorio", cascade="all, delete-orphan"
    )


class RelatorioDifusaoModel(Base):
    __tablename__ = "tb_relatorio_difusao"
    __table_args__ = {"schema": "sigeop"}

    cod_relatorio_difusao: Mapped[int] = mapped_column(
        Integer, Identity(always=True), primary_key=True
    )
    cod_relatorio: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_relatorio.cod_relatorio", ondelete="CASCADE"), nullable=False
    )
    cod_unidade: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sig_unidade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_unidade: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    dsc_destinatario_externo: Mapped[str | None] = mapped_column(Text, nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(Integer, nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(Integer, nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    relatorio: Mapped[RelatorioModel] = relationship(back_populates="difusoes")


class RelatorioPedidoModel(Base):
    __tablename__ = "tb_relatorio_pedido"
    __table_args__ = {"schema": "sigeop"}

    cod_relatorio: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_relatorio.cod_relatorio", ondelete="CASCADE"), primary_key=True
    )
    cod_pedido: Mapped[int] = mapped_column(
        ForeignKey("sigeop.tb_pedido.cod_pedido"), primary_key=True
    )
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(Integer, nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(Integer, nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    relatorio: Mapped[RelatorioModel] = relationship(back_populates="pedidos")
    pedido: Mapped["PedidoModel"] = relationship()
