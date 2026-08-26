from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.errors.errors import NotFoundError
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository
from src.modules.plano.plano_local.plano_local_schema import PlanoLocalCreateDTO, PlanoLocalUpdateDTO
from src.modules.plano.plano_missao.plano_missao_model import PlanoMissaoModel
from src.modules.plano.plano_missao.plano_missao_schema import (
    PlanoMissaoCreateDTO,
    PlanoMissaoReadDTO,
    PlanoMissaoUpdateDTO,
)
from src.modules.plano.plano_repository import PlanoRepository
from src.modules.plano.plano_schema import PlanoCreateDTO, PlanoReadDTO, PlanoUpdateDTO


class PlanoMissaoService:
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

    def list_by_missao(self, cod_missao: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        rows = self.db.execute(
            select(self.plano_repository.model, PlanoMissaoModel.cod_missao)
            .join(
                PlanoMissaoModel,
                PlanoMissaoModel.cod_plano == self.plano_repository.model.cod_plano,
            )
            .where(
                PlanoMissaoModel.cod_missao == cod_missao,
                PlanoMissaoModel.flg_reg_excluido.is_(False),
                self.plano_repository.model.flg_reg_excluido.is_(False),
            )
            .order_by(self.plano_repository.model.cod_plano.desc())
            .limit(limit)
            .offset(offset)
        ).all()

        plano_list = []
        for plano, cod_missao_encontrado in rows:
            setattr(plano, "cod_missao", cod_missao_encontrado)
            plano_list.append(plano)
        return [self.read_dto.from_model(plano) for plano in plano_list]

    def get(self, cod_plano: int) -> PlanoReadDTO:
        result = self.db.execute(
            select(self.plano_repository.model, PlanoMissaoModel.cod_missao)
            .join(
                PlanoMissaoModel,
                PlanoMissaoModel.cod_plano == self.plano_repository.model.cod_plano,
                isouter=True,
            )
            .where(self.plano_repository.model.cod_plano == cod_plano)
        ).first()

        if not result:
            raise NotFoundError(f"Plano({cod_plano}) não encontrado.")

        plano, cod_missao = result
        setattr(plano, "cod_missao", cod_missao)
        return self.read_dto.from_model(plano)

    def create(self, dto: PlanoMissaoCreateDTO) -> PlanoMissaoReadDTO:
        cod_missao = dto.cod_missao

        plano_data = dto.model_dump(exclude={"cod_missao"}, exclude_unset=True)
        plano_dto = PlanoCreateDTO(**plano_data)
        plano_model = self.plano_repository.create(plano_dto)

        self._sync_locais(plano_model.cod_plano, dto.local)
        self._sync_missao(plano_model.cod_plano, cod_missao)
        self.plano_repository.commit()
        return self.get(plano_model.cod_plano)

    def update(self, cod_plano: int, dto: PlanoMissaoUpdateDTO) -> PlanoMissaoReadDTO:
        cod_missao = dto.cod_missao

        plano_data = dto.model_dump(exclude={"cod_missao"}, exclude_unset=True)
        plano_dto = PlanoUpdateDTO(**plano_data)
        plano_model = self.plano_repository.update(cod_plano, plano_dto)

        self._sync_locais(plano_model.cod_plano, dto.local)
        self._sync_missao(plano_model.cod_plano, cod_missao)
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

    def _sync_missao(self, cod_plano: int, cod_missao: int | None) -> None:
        if not cod_missao:
            return

        vinculo = self.db.query(PlanoMissaoModel).filter(
            PlanoMissaoModel.cod_plano == cod_plano,
            PlanoMissaoModel.flg_reg_excluido.is_(False),
        ).first()

        agora = datetime.utcnow()
        if vinculo:
            vinculo.cod_missao = cod_missao
            vinculo.dat_hor_alteracao = agora
            vinculo.flg_reg_excluido = False
            self.db.add(vinculo)
            return

        self.db.add(
            PlanoMissaoModel(
                cod_plano=cod_plano,
                cod_missao=cod_missao,
                flg_reg_excluido=False,
                cif_usuario_inc=1,
                cif_usuario_alt=1,
                dat_hor_inclusao=agora,
                dat_hor_alteracao=agora,
            )
        )
