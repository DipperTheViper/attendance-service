from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from src.configs.containers import ServiceContainer
from src.logics.admin.admin_logic import AdminLogic
from src.models.dtos.admin.domain.v1.admin_domain_interface_dtos import (
    CreateAppConfigInputDTOV1,
    CreateAppConfigOutputDTOV1,
    CreateAppConfigRestInputDTOV1,
    DeleteAppConfigInputDTOV1,
    GetAppConfigInputDTOV1,
    GetAppConfigOutputDTOV1,
    SearchAppConfigInputDTOV1,
    SearchAppConfigOutputDTOV1,
    UpdateAppConfigInputDTOV1,
    UpdateAppConfigRestInputDTOV1,
    GetStartupConfigOutputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.ADMIN])


AdminRouterV1: APIRouter = APIRouter(tags=[ApiRouterType.ADMIN])


@AdminRouterV1.post(
    path="/app_configs",
    response_model=CreateAppConfigOutputDTOV1,
)
@inject
async def create_app_config(
    input_dto: CreateAppConfigRestInputDTOV1,
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> CreateAppConfigOutputDTOV1:
    input_dto = CreateAppConfigInputDTOV1.model_validate(input_dto)
    return await logic.create_app_config(input_dto=input_dto)


@AdminRouterV1.get(
    path="/app_configs",
    response_model=SearchAppConfigOutputDTOV1,
)
@inject
async def search_app_configs(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> SearchAppConfigOutputDTOV1:
    input_dto = SearchAppConfigInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_app_configs(input_dto=input_dto)


@AdminRouterV1.put(
    path="/app_configs/{app_config_uuid}",
)
@inject
async def update_app_config(
    app_config_uuid: UUID,
    input_dto: UpdateAppConfigRestInputDTOV1,
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> None:
    update_dto = UpdateAppConfigInputDTOV1(**input_dto.model_dump(), app_config_uuid=app_config_uuid)
    await logic.update_app_config(input_dto=update_dto)


@routerV1.get(
    path="/startup",
    response_model=GetStartupConfigOutputDTOV1,
)
@inject
async def get_startup_config(
    version: str = "0.0.1",
    logic: AdminLogic = Depends(Provide[ServiceContainer.admin_logic]),
) -> GetStartupConfigOutputDTOV1:
    return await logic.get_startup_config(version)
