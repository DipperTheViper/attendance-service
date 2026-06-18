from fastapi import Request
from src.logics.auth.authenticator_logic import Authenticator
from src.logics.auth.auth_logic import AuthLogic
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import GetUserOutputDTOV1
from src.models.exceptions.auth import AuthPermissionDeniedError
from src.models.types.enums import UserType


class AdminAuthenticator(Authenticator):
    def __init__(self, user_logic: UserLogic, auth_logic: AuthLogic, auto_error: bool = True) -> None:
        super().__init__(user_logic=user_logic, auth_logic=auth_logic, auto_error=auto_error)

    async def __call__(self, request: Request) -> GetUserOutputDTOV1:
        user = await super().__call__(request=request)
        if user.user_type != UserType.ADMIN:
            raise AuthPermissionDeniedError()
        return user
