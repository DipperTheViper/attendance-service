from uuid import UUID

from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.configs.containers import ServiceContainer
from src.logics.file.file_logic import FileLogic
from src.models.dtos.file.domain.v1.file_domain_interface_dtos import (
    CreateFileInputDTOV1,
    CreateFileOutputDTOV1,
    CreateFileRestInputDTOV1,
    DeleteFileInputDTOV1,
    GetFileInputDTOV1,
    GetFileOutputDTOV1,
    SearchFileInputDTOV1,
    SearchFileOutputDTOV1,
    UpdateFileInputDTOV1,
    UpdateFileRestInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.FILE])


@routerV1.post(
    path="/{user_uuid}/files",
    response_model=CreateFileOutputDTOV1,
)
@inject
async def create_file(
    user_uuid: UUID,
    input_dto: CreateFileRestInputDTOV1,
    logic: FileLogic = Depends(Provide[ServiceContainer.file_logic]),
) -> CreateFileOutputDTOV1:
    input_dto = CreateFileInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_file(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/files/{file_uuid}",
    response_model=GetFileOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_file(
    user_uuid: UUID,
    file_uuid: UUID,
    logic: FileLogic = Depends(Provide[ServiceContainer.file_logic]),
) -> GetFileOutputDTOV1:
    input_dto = GetFileInputDTOV1(file_uuid=file_uuid)
    return await logic.get_file(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/files",
    response_model=SearchFileOutputDTOV1,
)
@inject
async def search_files(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: FileLogic = Depends(Provide[ServiceContainer.file_logic]),
) -> SearchFileOutputDTOV1:
    input_dto = SearchFileInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_files(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/files/{file_uuid}",
)
@inject
async def update_file(
    user_uuid: UUID,
    file_uuid: UUID,
    input_dto: UpdateFileRestInputDTOV1,
    logic: FileLogic = Depends(Provide[ServiceContainer.file_logic]),
) -> None:
    update_dto = UpdateFileInputDTOV1(**input_dto.model_dump(), file_uuid=file_uuid)
    await logic.update_file(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/files/{file_uuid}",
)
@inject
async def delete_file(
    user_uuid: UUID,
    file_uuid: UUID,
    logic: FileLogic = Depends(Provide[ServiceContainer.file_logic]),
) -> None:
    input_dto = DeleteFileInputDTOV1(file_uuid=file_uuid)
    await logic.delete_file(input_dto=input_dto)
