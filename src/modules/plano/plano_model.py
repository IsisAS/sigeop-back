from sqlalchemy import String, Text, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Numeric, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime, date, timezone
from decimal import Decimal
from src.db.base import Base

from src.modules.plano.plano_equipe.plano_equipe_model import PlanoEquipeModel
from src.modules.plano.plano_local.plano_local_model import PlanoLocalModel

class PlanoModel(Base):
    __tablename__ = 'tb_plano'
    __table_args__ = (
        UniqueConstraint("num_plano", "num_ano", name="uq_tb_plano_num_ano"),
        {"schema": "sigeop"}
    )

    cod_plano: Mapped[int] = mapped_column(primary_key=True)
    cod_plano_tipo: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_plano_tipo.cod_plano_tipo"), nullable=False)
    tip_plano_contexto: Mapped[str] = mapped_column(String(10), nullable=False)
    cod_unidade: Mapped[int] = mapped_column(nullable=True)
    sig_unidade: Mapped[str] = mapped_column(String(50), nullable=True)
    nom_unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    dsc_arvore_unidade: Mapped[str] = mapped_column(String(1000), nullable=True)
    num_plano: Mapped[str] = mapped_column(String(20), nullable=False)
    num_equipe: Mapped[int] = mapped_column(Integer, nullable=False)
    num_ano: Mapped[int] = mapped_column(nullable=False)
    dat_emissao: Mapped[date] = mapped_column(Date, nullable=False)
    dat_aprovacao: Mapped[date] = mapped_column(Date, nullable=True)
    dat_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    dat_termino: Mapped[date] = mapped_column(Date, nullable=False)
    dat_baixa: Mapped[date] = mapped_column(Date, nullable=True)
    dsc_assunto: Mapped[str] = mapped_column(Text)
    idn_processo: Mapped[str] = mapped_column(String(40), nullable=True)
    vlr_custo_estimado: Mapped[Decimal] = mapped_column(Numeric(precision=14, scale=2), nullable=True)
    vlr_verba_sigilosa_aprovada: Mapped[Decimal] = mapped_column(Numeric(precision=14, scale=2), nullable=True)
    vlr_verba_ostensiva_aprovada: Mapped[Decimal] = mapped_column(Numeric(precision=14, scale=2), nullable=True)
    cod_plano_status: Mapped[int] = mapped_column(ForeignKey("sigeop.tb_plano_status.cod_plano_status"))
    flg_reg_excluido: Mapped[bool] = mapped_column(Boolean, default=False)
    cif_usuario_inc: Mapped[int] = mapped_column(nullable=False)
    cif_usuario_alt: Mapped[int] = mapped_column(nullable=False)
    dat_hor_inclusao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).astimezone())
    dat_hor_alteracao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).astimezone()) 
    plano_tipo: Mapped["PlanoTipoModel"] = relationship()
    plano_status: Mapped["PlanoStatusModel"] = relationship()
    
    plano_equipe: Mapped[list["PlanoEquipeModel"]] = relationship(back_populates="plano")
    local: Mapped[list["PlanoLocalModel"]] = relationship(back_populates="plano")

    
    # TODO: Relacionamentos comentados pois as models de Operação e Missão sofreram alterações
    # e não fazem parte do escopo/demanda atual. Responsável pela demanda das respectivas 
    # telas deve mapear a tabela associativa corretamente.
    # operacao: Mapped[list["OperacaoModel"]] = relationship(secondary="sigeop.tb_plano_operacao")
    # missao: Mapped[list["MissaoModel"]] = relationship(secondary="sigeop.tb_plano_missao")
