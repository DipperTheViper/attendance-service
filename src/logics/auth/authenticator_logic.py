from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.logics.auth.auth_logic import AuthLogic
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import GetUserOutputDTOV1
from src.models.exceptions.auth import MissingCredentialsError, InvalidSchemeError, AuthPermissionDeniedError


class Authenticator(HTTPBearer):
    def __init__(self, user_logic: UserLogic, auth_logic: AuthLogic, auto_error: bool = True) -> None:
        super().__init__(auto_error=auto_error)
        self._user_logic = user_logic
        self._auth_logic = auth_logic

    async def __call__(self, request: Request) -> GetUserOutputDTOV1:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request=request)

        if not credentials:
            raise MissingCredentialsError()

        if credentials.scheme.lower() != "bearer":
            raise InvalidSchemeError()

        user = await self._auth_logic.get_session_user(token=credentials.credentials)

        if request.path_params.get("user_uuid") and request.path_params.get("user_uuid") != str(user.user_uuid):
            raise AuthPermissionDeniedError()

        return user
