from uuid import UUID

from archipy.models.errors import NotFoundError
from archipy.models.types import SortOrderType
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.configs.containers import ServiceContainer
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    CreateUserInputDTOV1,
    CreateUserOutputDTOV1,
    CreateUserRestInputDTOV1,
    DeleteUserInputDTOV1,
    GetUserInputDTOV1,
    GetUserOutputDTOV1,
    SearchUserInputDTOV1,
    SearchUserOutputDTOV1,
    UpdateUserInputDTOV1,
    UpdateUserRestInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.USER])


@routerV1.post(
    path="/{user_uuid}/users",
    response_model=CreateUserOutputDTOV1,
)
@inject
async def create_user(
    user_uuid: UUID,
    input_dto: CreateUserRestInputDTOV1,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> CreateUserOutputDTOV1:
    input_dto = CreateUserInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_user(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}",
    response_model=GetUserOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses(
        [
            NotFoundError,
        ],
    ),
)
@inject
async def get_user(
    user_uuid: UUID,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> GetUserOutputDTOV1:
    input_dto = GetUserInputDTOV1(user_uuid=user_uuid)
    return await logic.get_user(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/users",
    response_model=SearchUserOutputDTOV1,
)
@inject
async def search_users(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> SearchUserOutputDTOV1:
    input_dto = SearchUserInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_users(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}",
    responses=Utils.get_fastapi_exception_responses(
        [
            NotFoundError,
        ],
    ),
)
@inject
async def update_user(
    user_uuid: UUID,
    input_dto: UpdateUserRestInputDTOV1,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> None:
    update_dto = UpdateUserInputDTOV1(**input_dto.model_dump(), user_uuid=user_uuid)
    await logic.update_user(input_dto=update_dto)


@routerV1.delete(
    path="/users/{user_uuid}",
)
@inject
async def delete_user(
    user_uuid: UUID,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> None:
    input_dto = DeleteUserInputDTOV1(user_uuid=user_uuid)
    await logic.delete_user(input_dto=input_dto)
