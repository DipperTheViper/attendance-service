from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.configs.containers import ServiceContainer
from src.logics.auth.auth_logic import AuthLogic
from src.models.dtos.auth.domain_interface.v1.auth_domain_interface_dtos import (
    LoginInputDTOV1,
    LoginOutputDTOV1,
    LogoutInputDTOV1,
    RegisterInputDTOV1,
    RegisterOutputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType

routerV1 = APIRouter(tags=[ApiRouterType.AUTHENTICATION])


@routerV1.post(
    path="/register",
    response_model=RegisterOutputDTOV1,
    status_code=201,
)
@inject
async def register(
    input_dto: RegisterInputDTOV1,
    logic: AuthLogic = Depends(Provide[ServiceContainer.auth_logic]),
) -> RegisterOutputDTOV1:
    return await logic.register(input_dto=input_dto)


@routerV1.post(
    path="/login",
    response_model=LoginOutputDTOV1,
)
@inject
async def login(
    input_dto: LoginInputDTOV1,
    logic: AuthLogic = Depends(Provide[ServiceContainer.auth_logic]),
) -> LoginOutputDTOV1:
    return await logic.login(input_dto=input_dto)


@routerV1.post(
    path="/logout",
)
@inject
async def logout(
    input_dto: LogoutInputDTOV1,
    logic: AuthLogic = Depends(Provide[ServiceContainer.auth_logic]),
) -> None:
    await logic.logout(input_dto=input_dto)
