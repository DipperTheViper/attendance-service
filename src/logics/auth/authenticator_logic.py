from uuid import UUID

from async_lru import alru_cache
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.configs.runtime_config import RuntimeConfig
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import GetUserInputDTOV1, GetUserOutputDTOV1
from src.models.exceptions.auth import (
    MissingCredentialsError,
    InvalidSchemeError,
    AuthInvalidTokenError,
    AuthTokenExpiredError,
    AuthPermissionDeniedError,
)
from src.utils.utils import Utils


class Authenticator(HTTPBearer):
    def __init__(self, user_logic: UserLogic, auto_error: bool = True) -> None:
        super().__init__(auto_error=auto_error)
        self._user_logic = user_logic

    async def __call__(self, request: Request) -> GetUserOutputDTOV1:
        """
        Authenticate the request and return user information.

        Args:
            request: FastAPI request object

        Returns:
            GetUserOutputDTOV1: Authenticated user information

        Raises:
            HTTPException: When authentication fails
        """
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request=request)

        if not credentials:
            raise MissingCredentialsError()

        if credentials.scheme.lower() != "bearer":
            raise InvalidSchemeError()

        user = await self._get_authenticated_user(token=credentials.credentials)
        if request.path_params.get("user_uuid") != str(user.user_uuid):
            raise AuthPermissionDeniedError()
        return user

    async def _get_authenticated_user(self, token: str) -> GetUserOutputDTOV1:
        """
        Verify JWT token and get user information.

        Args:
            token: JWT token string

        Returns:
            GetUserOutputDTOV1: User information

        Raises:
            AuthInvalidTokenException: When token is invalid
            AuthTokenExpiredException: When token has expired
        """
        payload: dict[str, any] = Utils.decode_token(token=token)
        if not payload:
            raise AuthInvalidTokenError()

        user_uuid: UUID | None = Utils.extract_user_uuid(payload=payload)
        if not user_uuid:
            AuthInvalidTokenError()

        token_expiry: int = Utils.get_token_expiry(token=token)
        if Utils.get_datetime_utc_now().timestamp() > token_expiry:
            raise AuthTokenExpiredError()

        # Get user from cache or database
        user_output_dto = await self._get_cached_user(user_uuid=user_uuid)
        return user_output_dto

    @alru_cache(ttl=RuntimeConfig.global_config().AUTH_GET_USER_CACHE_EXPIRATION_SECONDS)
    async def _get_cached_user(self, user_uuid: UUID) -> GetUserOutputDTOV1:
        """
        Get user information with caching.

        Args:
            user_uuid: User UUID

        Returns:
            GetUserOutputDTOV1: User information

        Raises:
            UserNotFoundException: When user is not found
        """
        user_input_dto: GetUserInputDTOV1 = GetUserInputDTOV1(user_uuid=user_uuid)
        return await self._user_logic.get_auth_user(input_dto=user_input_dto)
