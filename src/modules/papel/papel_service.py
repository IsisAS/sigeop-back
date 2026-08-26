from datetime import datetime

from src.common.service import AbstractService
from src.core.errors.errors import NotFoundError
from src.modules.papel.papel_model import PapelModel 
from src.modules.papel.papel_repository import PapelRepository
from src.modules.papel.papel_schema import PapelCreateDTO, PapelReadDTO, PapelUpdateDTO

#Marcador simulador
SIMULAR_PAPEL = False
_PAPEIS_MOCK: list[dict] = [
    {
        "cod_papel": 1,
        "dsc_papel": "Papel 1",
        "flg_ativo": True,
        "flg_reg_excluido": False,
        "cif_usuario_inc": 0,
        "cif_usuario_alt": 0,
        "dat_hor_inclusao": datetime.utcnow(),
        "dat_hor_alteracao": datetime.utcnow()      
    },
    {
        "cod_papel": 2,
        "dsc_papel": "Papel 2",
        "flg_ativo": True,
        "flg_reg_excluido": False,
        "cif_usuario_inc": 0,
        "cif_usuario_alt": 0,
        "dat_hor_inclusao": datetime.utcnow(),
        "dat_hor_alteracao": datetime.utcnow()        
    },
    {
        "cod_papel": 3,
        "dsc_papel": "Papel 3",
        "flg_ativo": True,
        "flg_reg_excluido": False,
        "cif_usuario_inc": 0,
        "cif_usuario_alt": 0,
        "dat_hor_inclusao": datetime.utcnow(),
        "dat_hor_alteracao": datetime.utcnow()        
    }
]


class PapelService(AbstractService[PapelModel, PapelCreateDTO, PapelUpdateDTO, PapelReadDTO]):
    read_dto = PapelReadDTO
    
    def __init__(self, repository: PapelRepository):
        self.repository = repository
    
    @staticmethod
    def _status_texto(item: PapelModel | dict) -> str:
        flg_ativo = item["flg_ativo"] if isinstance(item, dict) else item.flg_ativo
        flg_reg_excluido = item["flg_reg_excluido"] if isinstance(item, dict) else item.flg_reg_excluido
        return "Ativo" if flg_ativo and not flg_reg_excluido else "Inativo"
    
    def _to_read_dto(self, item: PapelModel | dict) -> PapelReadDTO:
        if isinstance(item, dict):
            return self.read_dto(
                cod_papel=item["cod_papel"],
                dsc_papel=item["dsc_papel"],
                flg_ativo=item["flg_ativo"],
                flg_reg_excluido=item["flg_reg_excluido"],
                status=self._status_texto(item),
                cif_usuario_inc=item["cif_usuario_inc"],
                cif_usuario_alt=item["cif_usuario_alt"],
                dat_hor_inclusao=item["dat_hor_inclusao"],
                dat_hor_alteracao=item["dat_hor_alteracao"],
            )
        
        return self.read_dto(            
            cod_papel=item.cod_papel,
            dsc_papel=item.dsc_papel,
            flg_ativo=item.flg_ativo,
            flg_reg_excluido=item.flg_reg_excluido,
            status=self._status_texto(item),
            cif_usuario_inc=item.cif_usuario_inc,
            cif_usuario_alt=item.cif_usuario_alt,
            dat_hor_inclusao=item.dat_hor_inclusao,
            dat_hor_alteracao=item.dat_hor_alteracao,
        )
    
    def list(self, *, limit: int = 50, offset: int = 0) -> list[PapelReadDTO]:
        if SIMULAR_PAPEL: 
            items = sorted(
                _PAPEIS_MOCK,
                key=lambda item: (
                    0 if item["flg_ativo"] and not item["flg_reg_excluido"] else 1,
                    item["dsc_papel"].lower(),
                    item["cod_papel"],
                ),
            )
            return [self._to_read_dto(item) for item in items[offset:offset + limit]]
        
        items = self.repository.list(limit=limit, offset=offset)
        return [self._to_read_dto(item) for item in items]
    
    def get(self, entity_id: int) -> PapelReadDTO:
        if SIMULAR_PAPEL: 
            item = next((papel for papel in _PAPEIS_MOCK if papel["cod_papel"] == entity_id), None)
            if not item: 
                raise NotFoundError(f"Papel([entity_id]) não encontrado.")
            return self._to_read_dto(item)
        
        item = self.repository.get(entity_id)
        return self._to_read_dto(item)
    
    def create(self, dto: PapelCreateDTO) -> PapelReadDTO:
        if SIMULAR_PAPEL: 
            next_id = max((papel["cod_papel"] for papel in _PAPEIS_MOCK), default=0) + 1
            now = datetime.utcnow()
            item = {
                "cod_papel": next_id,
                "dsc_papel": dto.dsc_papel,
                "flg_ativo": dto.flg_ativo,
                "flg_reg_excluido": dto.flg_reg_excluido,
                "cif_usuario_inc": dto.cif_usuario_inc,
                "cif_usuario_alt": dto.cif_usuario_alt,
                "dat_hor_inclusao": now,
                "dat_hor_alteracao": now,
            }
            _PAPEIS_MOCK.append(item)
            return self._to_read_dto(item)
        
        item = self.repository.create(dto)
        return self._to_read_dto(item)
    
    def update(self, entity_id: int, dto: PapelUpdateDTO) -> PapelReadDTO:
        if SIMULAR_PAPEL:
            item = next((papel for papel in _PAPEIS_MOCK if papel["cod_papel"] == entity_id), None)
            if not item: 
                raise NotFoundError(f"Papel([entity_id]) não encontrado.")

            item["dsc_papel"] = dto.dsc_papel
            item["flg_ativo"] =  dto.flg_ativo
            item["flg_reg_excluido"] = dto.flg_reg_excluido
            item["cif_usuario_inc"] = dto.cif_usuario_inc
            item["cif_usuario_alt"] = dto.cif_usuario_alt
            item["dat_hor_alteracao"] = datetime.utcnow()
            return self._to_read_dto(item)
        
        item = self.repository.update(entity_id, dto)
        return self._to_read_dto(item) 