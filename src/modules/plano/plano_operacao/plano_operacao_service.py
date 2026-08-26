from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.errors.errors import NotFoundError
from src.modules.plano.plano_operacao.plano_operacao_model import PlanoOperacaoModel
from src.modules.plano.plano_operacao.plano_operacao_schema import (
    PlanoOperacaoCreateDTO,
    PlanoOperacaoReadDTO,
    PlanoOperacaoUpdateDTO,
)
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository
from src.modules.plano.plano_local.plano_local_schema import PlanoLocalCreateDTO, PlanoLocalUpdateDTO
from src.modules.plano.plano_repository import PlanoRepository
from src.modules.plano.plano_schema import PlanoCreateDTO, PlanoUpdateDTO, PlanoReadDTO


class PlanoOperacaoService:
    read_dto = PlanoReadDTO

    def __init__(
        self,
        db: Session,
        plano_repository: PlanoRepository,
        plano_local_repository: PlanoLocalRepository,
    ) -> None:
        self.db = db
        self.plano_repository = plano_repository
        self.plano_local_repository = plano_local_repository

    def list_by_operacao(self, cod_operacao: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        rows = self.db.execute(
            select(self.plano_repository.model, PlanoOperacaoModel.cod_operacao)
            .join(
                PlanoOperacaoModel,
                PlanoOperacaoModel.cod_plano == self.plano_repository.model.cod_plano,
            )
            .where(
                PlanoOperacaoModel.cod_operacao == cod_operacao,
                PlanoOperacaoModel.flg_reg_excluido.is_(False),
                self.plano_repository.model.flg_reg_excluido.is_(False),
            )
            .order_by(self.plano_repository.model.cod_plano.desc())
            .limit(limit)
            .offset(offset)
        ).all()

        plano_list = []
        for plano, cod_operacao_encontrado in rows:
            setattr(plano, "cod_operacao", cod_operacao_encontrado)
            plano_list.append(plano)
        return [self.read_dto.from_model(plano) for plano in plano_list]

    def get(self, cod_plano: int) -> PlanoReadDTO:
        result = self.db.execute(
            select(self.plano_repository.model, PlanoOperacaoModel.cod_operacao)
            .join(
                PlanoOperacaoModel,
                PlanoOperacaoModel.cod_plano == self.plano_repository.model.cod_plano,
                isouter=True,
            )
            .where(self.plano_repository.model.cod_plano == cod_plano)
        ).first()

        if not result:
            raise NotFoundError(f"Plano({cod_plano}) não encontrado.")

        plano, cod_operacao = result
        setattr(plano, "cod_operacao", cod_operacao)
        return self.read_dto.from_model(plano)

    def create(self, dto: PlanoOperacaoCreateDTO) -> PlanoOperacaoReadDTO:
        cod_operacao = dto.cod_operacao

        plano_data = dto.model_dump(exclude={"cod_operacao"}, exclude_unset=True)
        plano_dto = PlanoCreateDTO(**plano_data)
        plano_model = self.plano_repository.create(plano_dto)

        self._sync_locais(plano_model.cod_plano, dto.local)
        self._sync_operacao(plano_model.cod_plano, cod_operacao)
        self.plano_repository.commit()
        return self.get(plano_model.cod_plano)

    def update(self, cod_plano: int, dto: PlanoOperacaoUpdateDTO) -> PlanoOperacaoReadDTO:
        cod_operacao = dto.cod_operacao

        plano_data = dto.model_dump(exclude={"cod_operacao"}, exclude_unset=True)
        plano_dto = PlanoUpdateDTO(**plano_data)
        plano_model = self.plano_repository.update(cod_plano, plano_dto)

        self._sync_locais(plano_model.cod_plano, dto.local)
        self._sync_operacao(plano_model.cod_plano, cod_operacao)
        self.plano_repository.commit()
        return self.get(plano_model.cod_plano)

    def _sync_locais(self, cod_plano: int, locais_dto: list) -> None:
        locais_banco = self.plano_local_repository.get_by_plano_id(cod_plano)

        ids_banco = {local.cod_plano_local for local in locais_banco}
        ids_recebidos = {
            local.cod_plano_local for local in locais_dto if getattr(local, "cod_plano_local", None) is not None
        }

        ids_para_remover = ids_banco - ids_recebidos

        for cod_plano_local in ids_para_remover:
            self.plano_local_repository.delete(cod_plano_local)

        for local in locais_dto:
            if getattr(local, "cod_plano_local", None):
                self.plano_local_repository.update(
                    local.cod_plano_local,
                    PlanoLocalUpdateDTO(
                        cod_plano=cod_plano,
                        cod_pais=local.cod_pais,
                        cod_uf=local.cod_uf,
                        cod_municipio=local.cod_municipio,
                        dsc_local=local.dsc_local,
                        cif_usuario_inc=1,
                        cif_usuario_alt=1,
                    ),
                )
            else:
                self.plano_local_repository.create(
                    PlanoLocalCreateDTO(
                        cod_plano=cod_plano,
                        cod_pais=local.cod_pais,
                        cod_uf=local.cod_uf,
                        cod_municipio=local.cod_municipio,
                        dsc_local=local.dsc_local,
                        cif_usuario_inc=1,
                        cif_usuario_alt=1,
                    )
                )

    def _sync_operacao(self, cod_plano: int, cod_operacao: int | None) -> None:
        if not cod_operacao:
            return

        vinculo = self.db.query(PlanoOperacaoModel).filter(
            PlanoOperacaoModel.cod_plano == cod_plano,
            PlanoOperacaoModel.flg_reg_excluido.is_(False),
        ).first()

        agora = datetime.utcnow()
        if vinculo:
            vinculo.cod_operacao = cod_operacao
            vinculo.dat_hor_alteracao = agora
            vinculo.flg_reg_excluido = False
            self.db.add(vinculo)
            return

        self.db.add(
            PlanoOperacaoModel(
                cod_plano=cod_plano,
                cod_operacao=cod_operacao,
                flg_reg_excluido=False,
                cif_usuario_inc=1,
                cif_usuario_alt=1,
                dat_hor_inclusao=agora,
                dat_hor_alteracao=agora,
            )
        )
