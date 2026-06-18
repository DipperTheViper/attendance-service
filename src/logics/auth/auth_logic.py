import secrets

from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

from src.logics.user.user_logic import UserLogic
from src.models.dtos.auth.domain_interface.v1.auth_domain_interface_dtos import (
    LoginInputDTOV1,
    LoginOutputDTOV1,
    LogoutInputDTOV1,
    RegisterInputDTOV1,
    RegisterOutputDTOV1,
)
from src.models.dtos.auth.repository_interface.auth_repository_interface_dtos import (
    CreateSessionCommandDTO,
    DeleteSessionCommandDTO,
    GetSessionQueryDTO,
)
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    GetUserByUsernameInputDTOV1,
    GetUserOutputDTOV1,
    CreateUserInputDTOV1,
    GetUserByUsernameOutputDTOV1,
    GetUserInputDTOV1,
)
from src.models.exceptions.auth import AuthPermissionDeniedError
from src.repositories.auth.auth_repository import AuthRepository
from src.utils.utils import Utils


class AuthLogic:
    def __init__(
        self,
        repository: AuthRepository,
        user_logic: UserLogic,
    ) -> None:
        self._repository = repository
        self._user_logic = user_logic

    @async_postgres_sqlalchemy_atomic_decorator
    async def register(self, input_dto: RegisterInputDTOV1) -> RegisterOutputDTOV1:
        create_user_dto = CreateUserInputDTOV1(
            username=Utils.encrypt_username(input_dto.username),
            hashed_password=Utils.hash_password(input_dto.password),
            phone_number=input_dto.phone_number,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
        )
        response = await self._user_logic.create_user(input_dto=create_user_dto)
        access_token = secrets.token_hex(32)
        await self._repository.create_session(
            command=CreateSessionCommandDTO(user_uuid=response.user_uuid, access_token=access_token),
        )
        return RegisterOutputDTOV1(access_token=access_token, user_uuid=response.user_uuid)

    @async_postgres_sqlalchemy_atomic_decorator
    async def login(self, input_dto: LoginInputDTOV1) -> LoginOutputDTOV1:
        encrypted_username = Utils.encrypt_username(input_dto.username)
        user: GetUserByUsernameOutputDTOV1 = await self._user_logic.get_user_by_username(
            input_dto=GetUserByUsernameInputDTOV1(username=encrypted_username),
        )

        if not Utils.verify_password(input_dto.password, user.hashed_password):
            raise AuthPermissionDeniedError()

        access_token = secrets.token_hex(32)
        await self._repository.create_session(
            command=CreateSessionCommandDTO(user_uuid=user.user_uuid, access_token=access_token),
        )
        return LoginOutputDTOV1(access_token=access_token, user_uuid=user.user_uuid)

    @async_postgres_sqlalchemy_atomic_decorator
    async def logout(self, input_dto: LogoutInputDTOV1) -> None:
        await self._repository.delete_session(command=DeleteSessionCommandDTO(access_token=input_dto.access_token))

    async def get_session_user(self, token: str) -> GetUserOutputDTOV1:
        session = await self._repository.get_session(query=GetSessionQueryDTO(access_token=token))
        return await self._user_logic.get_user(input_dto=GetUserInputDTOV1(user_uuid=session.user_uuid))
