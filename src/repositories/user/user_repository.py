from src.models.dtos.user.repository.user_repository_interface_dtos import (
    AdminUpdateUserCommandDTO,
    CreateUserCommandDTO,
    CreateUserResponseDTO,
    DeleteUserCommandDTO,
    GetAdminUserQueryDTO,
    GetAdminUserResponseDTO,
    GetUserInfoQueryDTO,
    GetUserInfoResponseDTO,
    GetUserQueryDTO,
    GetUserResponseDTO,
    GetUserPhoneNumberQueryDTO,
    GetUserPhoneNumberResponseDTO,
    GetUserWithPhoneNumberQueryDTO,
    GetUserWithPhoneNumberResponseDTO,
    SearchUserQueryDTO,
    SearchUserResponseDTO,
    UpdateUserCommandDTO,
    UpdateUserInternalsCommandDTO,
)
from src.repositories.user.adapters.user_postgres_adapter import UserPostgresAdapter


class UserRepository:
    def __init__(self, postgres_adapter: UserPostgresAdapter):
        self._postgres_adapter: UserPostgresAdapter = postgres_adapter

    async def create_user(self, input_dto: CreateUserCommandDTO) -> CreateUserResponseDTO:
        return await self._postgres_adapter.create_user(input_dto=input_dto)

    async def get_user(self, input_dto: GetUserQueryDTO) -> GetUserResponseDTO:
        return await self._postgres_adapter.get_user(input_dto=input_dto)

    async def get_admin_auth_user(self, input_dto: GetUserQueryDTO) -> GetUserResponseDTO:
        return await self._postgres_adapter.get_admin_auth_user(input_dto=input_dto)

    async def get_admin_user(self, input_dto: GetAdminUserQueryDTO) -> GetAdminUserResponseDTO:
        return await self._postgres_adapter.get_admin_user(input_dto=input_dto)

    async def search_users(self, input_dto: SearchUserQueryDTO) -> SearchUserResponseDTO:
        return await self._postgres_adapter.search_users(input_dto=input_dto)

    async def update_user(self, input_dto: UpdateUserCommandDTO) -> None:
        await self._postgres_adapter.update_user(input_dto=input_dto)

    async def delete_user(self, input_dto: DeleteUserCommandDTO) -> None:
        await self._postgres_adapter.delete_user(input_dto=input_dto)

    async def get_user_with_phone_number(
        self,
        input_dto: GetUserWithPhoneNumberQueryDTO,
    ) -> GetUserWithPhoneNumberResponseDTO:
        return await self._postgres_adapter.get_user_with_phone_number(input_dto=input_dto)

    async def get_user_phone_number(self, input_dto: GetUserPhoneNumberQueryDTO) -> GetUserPhoneNumberResponseDTO:
        return await self._postgres_adapter.get_user_phone_number(input_dto=input_dto)

    async def update_user_internals(self, command: UpdateUserInternalsCommandDTO) -> None:
        await self._postgres_adapter.update_user_internals(command)

    async def get_user_info(self, input_dto: GetUserInfoQueryDTO) -> GetUserInfoResponseDTO:
        return await self._postgres_adapter.get_user_info(input_dto=input_dto)

    async def admin_update_user(self, command: AdminUpdateUserCommandDTO) -> None:
        return await self._postgres_adapter.admin_update_user(command)
