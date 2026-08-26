from typing import TypeVar, Callable, Any, Type, Generic, Literal

from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.orm import Session

from src.core.deps import get_db

CreateDTOT = TypeVar("CreateDTOT")
UpdateDTOT = TypeVar("UpdateDTOT")
ReadDTOT = TypeVar("ReadDTOT")
ServiceT = TypeVar("ServiceT")

Operation = Literal["list", "get", "create", "update", "delete"]
ALL_OPERATIONS: set[Operation] = {"list", "get", "create", "update", "delete"}


class CrudRouter(Generic[CreateDTOT, UpdateDTOT, ReadDTOT, ServiceT]):
    def __init__(
        self,
        *,
        prefix: str,
        tags: list[str],
        create_dto: Type[CreateDTOT] | None = None,
        update_dto: Type[UpdateDTOT] | None = None,
        read_dto: Type[ReadDTOT],
        get_service: Callable[[Session], ServiceT],
        id_param: str = "id",
        id_description: str = "ID do recurso",
        operations: set[Operation] | None = None,
        exclude: set[Operation] | None = None,
    ):
        if operations is not None and exclude is not None:
            raise ValueError("Forneça 'operations' ou 'exclude', não ambos.")

        if operations is not None:
            active = operations
        elif exclude is not None:
            active = ALL_OPERATIONS - exclude
        else:
            active = ALL_OPERATIONS

        if "create" in active and create_dto is None:
            raise ValueError("create_dto é obrigatório quando a operação 'create' está ativa.")
        if "update" in active and update_dto is None:
            raise ValueError("update_dto é obrigatório quando a operação 'update' está ativa.")

        self.router = APIRouter(prefix=prefix, tags=tags)

        CreateDTO = create_dto
        UpdateDTO = update_dto
        ReadDTO = read_dto

        def _svc(db: Session = Depends(get_db)) -> ServiceT:
            return get_service(db)

        if "list" in active:
            @self.router.get("", response_model=list[ReadDTO])
            def list_(limit: int = 50, offset: int = 0, service: ServiceT = Depends(_svc)):
                return service.list(limit=limit, offset=offset)  # type: ignore[attr-defined]

        if "get" in active:
            @self.router.get("/{" + id_param + "}", response_model=ReadDTO)
            def get_(
                resource_id: int = Path(..., alias=id_param, description=id_description),
                service: ServiceT = Depends(_svc),
            ):
                return service.get(resource_id)  # type: ignore[attr-defined]

        if "create" in active:
            @self.router.post("", response_model=ReadDTO, status_code=201)
            def create_(dto: CreateDTO = Body(...), service: ServiceT = Depends(_svc)):
                return service.create(dto)  # type: ignore[attr-defined]

        if "update" in active:
            @self.router.put("/{" + id_param + "}", response_model=ReadDTO)
            def update_(
                resource_id: int = Path(..., alias=id_param, description=id_description),
                dto: UpdateDTO = Body(...),
                service: ServiceT = Depends(_svc),
            ):
                return service.update(resource_id, dto)  # type: ignore[attr-defined]

        if "delete" in active:
            @self.router.delete("/{" + id_param + "}", status_code=204)
            def delete_(
                resource_id: int = Path(..., alias=id_param, description=id_description),
                service: ServiceT = Depends(_svc),
            ):
                service.delete(resource_id)  # type: ignore[attr-defined]
                return None
