from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.deps import get_db 
from src.modules.plano.plano_local.plano_local_repository import PlanoLocalRepository

router = APIRouter(
    prefix="/plano-local",
    tags=["Plano Local"]
)

@router.get("/descricoes", response_model=List[str])
def get_descricoes(
    cod_pais: int = Query(..., description="Código do país"),
    cod_uf: int | None = Query(None, description="Código da UF (opcional)"),
    cod_municipio: int | None = Query(None, description="Código do município (opcional)"),
    db: Session = Depends(get_db),
): 
    """
    Retornar descrições distintas de locais já cadastrados,
    filtradas por país, UF e município para uso em autocomplete.
    """
    
    repo = PlanoLocalRepository(db)
    return repo.get_descricoes(
        cod_pais=cod_pais,
        cod_uf=cod_uf,
        cod_municipio=cod_municipio,
    )