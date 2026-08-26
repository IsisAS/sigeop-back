from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base 

class MissaoModel(Base):
    __tablename__ = "tb_missao"
    __table_args__ = {"schema": "sigeop"}
    
    cod_missao: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_missao_tipo: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_missao_tipo.cod_missao_tipo"), nullable=False)
    dsc_missao: Mapped[str | None] = mapped_column(Text, nullable=True)
    idn_agente_nao_organico: Mapped[str | None] = mapped_column(Text, nullable=True)
    cod_missao_status: Mapped[int | None] = mapped_column(
        ForeignKey("sigeop.tb_missao_status.cod_missao_status"), nullable=True
    )
    cod_recurso_tipo: Mapped[int | None] = mapped_column(ForeignKey("sigeop.tb_recurso_tipo.cod_recurso_tipo"), nullable=True)
    idn_agente_nao_organico: Mapped[ str | None] = mapped_column(Text, nullable=True)
    cod_unidade_responsavel: Mapped[int | None] = mapped_column(nullable=True)
    sig_unidade_responsavel: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_unidade_responsavel: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade_responsavel: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    dsc_justificativa_exclusao: Mapped[str | None] = mapped_column(Text, nullable=True)
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    tipo: Mapped["MissaoTipoModel"] = relationship(back_populates="missoes")
    status: Mapped["MissaoStatusModel"] = relationship(back_populates="missoes")
    recurso_tipo: Mapped["RecursoTipoModel"] = relationship(back_populates="missoes")
    encarregados: Mapped[list["MissaoEncarregadoModel"]] = relationship(back_populates="missao")
    
    fontes_humanas: Mapped[list["MissaoFonteHumanaModel"]] = relationship(back_populates="missao")
    
    cod_pedido: Mapped[int | None] = mapped_column(ForeignKey("sigeop.tb_pedido.cod_pedido"), nullable=True)
    pedido: Mapped["PedidoModel"] = relationship(back_populates="missoes")
    
    cod_operacao: Mapped[int | None] = mapped_column(ForeignKey("sigeop.tb_operacao.cod_operacao"), nullable=True)
    operacao: Mapped["OperacaoModel"] = relationship(back_populates="missoes")
    
    cod_caso: Mapped[int | None] = mapped_column(ForeignKey("sigeop.tb_caso.cod_caso"), nullable=True)
    caso: Mapped["CasoModel"] = relationship(back_populates="missoes")

    # planos: Mapped[list["PlanoModel"]] = relationship(back_populates="missao")
