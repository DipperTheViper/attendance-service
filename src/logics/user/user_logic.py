from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    CreateUserInputDTOV1,
    CreateUserOutputDTOV1,
    DeleteUserInputDTOV1,
    GetUserByUsernameInputDTOV1,
    GetUserInputDTOV1,
    GetUserOutputDTOV1,
    SearchUserInputDTOV1,
    SearchUserOutputDTOV1,
    UpdateUserInputDTOV1,
    GetUserByUsernameOutputDTOV1,
)
from src.models.dtos.user.repository.user_repository_interface_dtos import (
    CreateUserCommandDTO,
    CreateUserResponseDTO,
    DeleteUserCommandDTO,
    GetUserByUsernameQueryDTO,
    GetUserQueryDTO,
    GetUserResponseDTO,
    SearchUserQueryDTO,
    SearchUserResponseDTO,
    UpdateUserCommandDTO,
)
from src.repositories.user.user_repository import UserRepository


class UserLogic:
    def __init__(self, repository: UserRepository) -> None:
        self._repository: UserRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_user(self, input_dto: CreateUserInputDTOV1) -> CreateUserOutputDTOV1:
        command = CreateUserCommandDTO.model_validate(input_dto)
        response: CreateUserResponseDTO = await self._repository.create_user(input_dto=command)
        return CreateUserOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_user(self, input_dto: GetUserInputDTOV1) -> GetUserOutputDTOV1:
        query = GetUserQueryDTO.model_validate(obj=input_dto)
        response: GetUserResponseDTO = await self._repository.get_user(input_dto=query)
        return GetUserOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_user_by_username(self, input_dto: GetUserByUsernameInputDTOV1) -> GetUserByUsernameOutputDTOV1:
        query = GetUserByUsernameQueryDTO.model_validate(obj=input_dto)
        response: GetUserResponseDTO = await self._repository.get_user_by_username(input_dto=query)
        return GetUserByUsernameOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_users(self, input_dto: SearchUserInputDTOV1) -> SearchUserOutputDTOV1:
        repository_dto = SearchUserQueryDTO.model_validate(input_dto)
        response: SearchUserResponseDTO = await self._repository.search_users(input_dto=repository_dto)
        return SearchUserOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_user(self, input_dto: UpdateUserInputDTOV1) -> None:
        command = UpdateUserCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_user(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_user(self, input_dto: DeleteUserInputDTOV1) -> None:
        command = DeleteUserCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_user(input_dto=command)
