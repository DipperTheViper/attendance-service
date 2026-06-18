from typing import Any

from archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler import FastAPIRestRateLimitHandler
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Body

from src.configs.containers import ServiceContainer
from src.configs.runtime_config import RuntimeConfig
from src.logics.auth.auth_logic import AuthLogic
from src.models.dtos.auth.domain_interface.v1.auth_domain_interface_dtos import (
    CreateTOTPInputDTOV1,
    CreateTOTPOutputDTOV1,
    RefreshTokenInputDTOV1,
    RefreshTokenOutputDTOV1,
    VerifyTOTPInputDTOV1,
    VerifyTOTPOutputDTOV1,
    LoginOutputDTOV1,
    LoginInputDTOV1,
)
from src.models.exceptions.auth import AuthInvalidTokenError, AuthUserNotFoundError
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1 = APIRouter(tags=[ApiRouterType.AUTHENTICATION])


@routerV1.post(
    path="/create-totp",
    response_model=CreateTOTPOutputDTOV1,
    dependencies=[
        Depends(
            FastAPIRestRateLimitHandler(
                calls_count=RuntimeConfig.global_config().AUTH_CREATE_TOTP_CALLS_COUNT_LIMIT,
                minutes=RuntimeConfig.global_config().AUTH_CREATE_TOTP_MINUTES_LIMIT,
            ),
        ),
    ],
)
@inject
async def create_totp(
    input_dto: CreateTOTPInputDTOV1,
    logic: AuthLogic = Depends(Provide[ServiceContainer.auth_logic]),
) -> CreateTOTPOutputDTOV1:
    return await logic.create_totp(input_dto=input_dto)


@routerV1.post(
    path="/verify-totp",
    response_model=VerifyTOTPOutputDTOV1,
    dependencies=[
        Depends(
            FastAPIRestRateLimitHandler(
                calls_count=RuntimeConfig.global_config().AUTH_VERIFY_TOTP_CALLS_COUNT_LIMIT,
                minutes=RuntimeConfig.global_config().AUTH_VERIFY_TOTP_MINUTES_LIMIT,
            ),
        ),
    ],
)
@inject
async def verify_totp(
    input_dto: VerifyTOTPInputDTOV1,
    logic: AuthLogic = Depends(Provide[ServiceContainer.auth_logic]),
) -> VerifyTOTPOutputDTOV1:
    return await logic.verify_totp(input_dto=input_dto)


@routerV1.post(
    path="/refresh-token",
    response_model=RefreshTokenOutputDTOV1,
)
@inject
async def refresh_token(
    input_dto: RefreshTokenInputDTOV1,
    logic: AuthLogic = Depends(Provide[ServiceContainer.auth_logic]),
) -> RefreshTokenOutputDTOV1:
    return await logic.refresh_token(input_dto=input_dto)


AdminRouterV1 = APIRouter(tags=[ApiRouterType.ADMIN_AUTH])


@AdminRouterV1.post(
    path="/login",
    response_model=LoginOutputDTOV1,
    dependencies=[
        Depends(
            FastAPIRestRateLimitHandler(
                calls_count=RuntimeConfig.global_config().ADMIN_AUTH_LOGIN_CALLS_COUNT_LIMIT,
                minutes=RuntimeConfig.global_config().ADMIN_AUTH_LOGIN_MINUTES_LIMIT,
            ),
        ),
    ],
)
@inject
async def login(
    data: LoginInputDTOV1 = Body(default={"username": "admin", "password": "123456789"}),
    auth_logic: AuthLogic = Depends(Provide[ServiceContainer.auth_logic]),
) -> LoginOutputDTOV1:
    return await auth_logic.login(input_dto=data)


@AdminRouterV1.post(
    path="/refresh-token",
    response_model=RefreshTokenOutputDTOV1,
)
async def refresh_token(input_data: RefreshTokenInputDTOV1) -> RefreshTokenOutputDTOV1:
    payload: dict[str, Any] = Utils.decode_token(token=input_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise AuthInvalidTokenError()

    if not (user_uuid := Utils.extract_user_uuid(payload=payload)):
        raise AuthUserNotFoundError()

    access_token: str = Utils.create_access_token(user_uuid=user_uuid)
    return RefreshTokenOutputDTOV1(access_token=access_token)
