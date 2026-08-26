from typing import List
from sqlalchemy import select
from src.common.repository import AbstractRepository
from src.modules.plano.plano_missao.plano_missao_model import PlanoMissaoModel
from src.modules.plano.plano_model import PlanoModel
from src.modules.plano.plano_operacao.plano_operacao_model import PlanoOperacaoModel
from src.modules.plano.plano_schema import PlanoUpdateDTO, PlanoCreateDTO, PlanoReadDTO

class PlanoRepository(AbstractRepository[PlanoModel, PlanoCreateDTO, PlanoUpdateDTO]):
    model = PlanoModel

    def create(self, dto: PlanoCreateDTO) -> model:
            data = dto.model_dump(exclude={"plano_equipe", "local", "cod_caso", "cod_operacao", "cod_missao"}, exclude_unset=True)
            obj = self.model(**data) 
            self.db.add(obj)
            self.db.flush()
            return obj
    
    
    def update(self, plano_id: int, dto: PlanoUpdateDTO) -> model:
        obj = self.get(plano_id)
        data = dto.model_dump(exclude={"plano_equipe", "local", "cod_caso", "cod_operacao", "cod_missao"},exclude_unset=True)

        for k, v in data.items():
            setattr(obj, k, v)

        self.db.add(obj)
        self.db.flush()
        return obj
    
    def commit(self) -> None:
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def get_by_caso_id(self, cod_caso: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        stmt = select(self.model).where(
            self.model.cod_caso == cod_caso
        )

        return self.db.execute(stmt).scalars().all()

    def get_by_operacao_id(self, cod_operacao: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        rows = self.db.execute(
            select(self.model, PlanoOperacaoModel.cod_operacao)
            .join(
                PlanoOperacaoModel,
                PlanoOperacaoModel.cod_plano == self.model.cod_plano,
            )
            .where(
                PlanoOperacaoModel.cod_operacao == cod_operacao,
                PlanoOperacaoModel.flg_reg_excluido.is_(False),
                self.model.flg_reg_excluido.is_(False),
            )
            .limit(limit)
            .offset(offset)
        ).all()

        plano_list = []
        for plano, cod_operacao_encontrado in rows:
            setattr(plano, "cod_operacao", cod_operacao_encontrado)
            plano_list.append(plano)

        return plano_list

    def get_by_missao_id(self, cod_missao: int, *, limit: int = 50, offset: int = 0) -> List[PlanoReadDTO]:
        rows = self.db.execute(
            select(self.model, PlanoMissaoModel.cod_missao)
            .join(
                PlanoMissaoModel,
                PlanoMissaoModel.cod_plano == self.model.cod_plano,
            )
            .where(
                PlanoMissaoModel.cod_missao == cod_missao,
                PlanoMissaoModel.flg_reg_excluido.is_(False),
                self.model.flg_reg_excluido.is_(False),
            )
            .limit(limit)
            .offset(offset)
        ).all()

        plano_list = []
        for plano, cod_missao_encontrado in rows:
            setattr(plano, "cod_missao", cod_missao_encontrado)
            plano_list.append(plano)

        return plano_list
        

