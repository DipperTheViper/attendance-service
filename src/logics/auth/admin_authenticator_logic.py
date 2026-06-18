from typing import Any
from uuid import UUID

from async_lru import alru_cache
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.configs.runtime_config import RuntimeConfig
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    GetUserOutputDTOV1,
    GetAdminUserInputDTOV1,
)
from src.models.exceptions.auth import (
    MissingCredentialsError,
    InvalidSchemeError,
    AuthInvalidTokenError,
    AuthTokenExpiredError,
)
from src.utils.utils import Utils


class AdminAuthenticator(HTTPBearer):
    def __init__(self, user_logic: UserLogic, auto_error: bool = True) -> None:
        super().__init__(auto_error=auto_error)
        self._user_logic = user_logic

    async def __call__(self, request: Request) -> GetUserOutputDTOV1:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request=request)

        if not credentials:
            raise MissingCredentialsError()

        if credentials.scheme.lower() != "bearer":
            raise InvalidSchemeError()

        return await self._get_authenticated_user(token=credentials.credentials)

    async def _get_authenticated_user(self, token: str) -> GetUserOutputDTOV1:
        payload: dict[str, Any] = Utils.decode_token(token=token)
        if not payload:
            raise AuthInvalidTokenError()

        user_uuid: UUID | None = Utils.extract_user_uuid(payload=payload)
        if not user_uuid:
            AuthInvalidTokenError()

        token_expiry: int = Utils.get_token_expiry(token=token)
        if Utils.get_datetime_utc_now().timestamp() > token_expiry:
            raise AuthTokenExpiredError()
        user_output_dto = await self._get_cached_user(user_uuid=user_uuid)
        return user_output_dto

    @alru_cache(ttl=RuntimeConfig.global_config().AUTH_GET_USER_CACHE_EXPIRATION_SECONDS)
    async def _get_cached_user(self, user_uuid: UUID) -> GetUserOutputDTOV1:
        user_input_dto = GetAdminUserInputDTOV1(user_uuid=user_uuid)
        return await self._user_logic.get_admin_auth_user(input_dto=user_input_dto)
