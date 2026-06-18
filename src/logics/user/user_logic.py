from uuid import UUID

from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from archipy.models.errors import NotFoundError, UnauthenticatedError

from src.logics.referral.referral_logic import ReferralLogic
from src.models.dtos.referral.domain.v1.referral_domain_interface_dtos import CreateReferralInputDTOV1
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    AdminUpdateUserInputDTOV1,
    CreateUserInputDTOV1,
    CreateUserOutputDTOV1,
    DeleteUserInputDTOV1,
    GetAdminUserInputDTOV1,
    GetAdminUserOutputDTOV1,
    GetUserInputDTOV1,
    GetUserOutputDTOV1,
    GetUserInfoInputDTOV1,
    GetUserInfoOutputDTOV1,
    GetUserWithPhoneNumberInputDTOV1,
    GetUserWithPhoneNumberOutputDTOV1,
    SearchAuthUserInputDTOV1,
    SearchAuthUsersOutputDTOV1,
    SearchUserInputDTOV1,
    SearchUserOutputDTOV1,
    UpdateUserInputDTOV1,
    UpdateUserInternalsInputDTOV1,
)
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
from src.repositories.user.user_repository import UserRepository


class UserLogic:
    def __init__(
        self,
        repository: UserRepository,
        referral_logic: ReferralLogic = None,
    ) -> None:
        self._repository: UserRepository = repository
        self._referral_logic: ReferralLogic = referral_logic

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_user(self, input_dto: CreateUserInputDTOV1) -> CreateUserOutputDTOV1:
        command = CreateUserCommandDTO(
            phone_number=input_dto.phone_number,
        )
        response: CreateUserResponseDTO = await self._repository.create_user(input_dto=command)
        return CreateUserOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_user(self, input_dto: GetUserInputDTOV1) -> GetUserOutputDTOV1:
        query: GetUserQueryDTO = GetUserQueryDTO.model_validate(obj=input_dto)
        response: GetUserResponseDTO = await self._repository.get_user(input_dto=query)
        return GetUserOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_auth_user(self, input_dto: GetUserInputDTOV1) -> GetUserOutputDTOV1:
        query: GetUserQueryDTO = GetUserQueryDTO.model_validate(obj=input_dto)
        try:
            response: GetUserResponseDTO = await self._repository.get_user(input_dto=query)
        except NotFoundError as e:
            raise UnauthenticatedError()
        return GetUserOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_admin_auth_user(self, input_dto: GetAdminUserInputDTOV1) -> GetUserOutputDTOV1:
        query = GetUserQueryDTO.model_validate(obj=input_dto)
        try:
            response: GetUserResponseDTO = await self._repository.get_admin_auth_user(input_dto=query)
        except NotFoundError as e:
            raise UnauthenticatedError()
        return GetUserOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_admin_user(self, input_dto: GetAdminUserInputDTOV1) -> GetAdminUserOutputDTOV1:
        query = GetAdminUserQueryDTO.model_validate(obj=input_dto)
        response: GetAdminUserResponseDTO = await self._repository.get_admin_user(input_dto=query)
        return GetAdminUserOutputDTOV1.model_validate(obj=response)

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

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_user_with_phone_number(
        self,
        input_dto: GetUserWithPhoneNumberInputDTOV1,
    ) -> GetUserWithPhoneNumberOutputDTOV1:
        query = GetUserWithPhoneNumberQueryDTO.model_validate(obj=input_dto)
        response: GetUserWithPhoneNumberResponseDTO = await self._repository.get_user_with_phone_number(input_dto=query)
        return GetUserWithPhoneNumberOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_auth_users(self, input_dto: SearchAuthUserInputDTOV1) -> SearchAuthUsersOutputDTOV1:
        try:
            get_user_dto = GetUserWithPhoneNumberInputDTOV1.model_validate(obj=input_dto)
            response: GetUserWithPhoneNumberOutputDTOV1 = await self.get_user_with_phone_number(input_dto=get_user_dto)
        except NotFoundError:
            _input_dto = CreateUserInputDTOV1.model_validate(obj=input_dto)
            response = await self.create_user(input_dto=_input_dto)
            if input_dto.referer_uuid:
                await self._referral_logic.create_referral(
                    CreateReferralInputDTOV1(referer_uuid=input_dto.referer_uuid, referee_uuid=response.user_uuid),
                )
        return SearchAuthUsersOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_user_phone_number(self, user_uuid: UUID) -> str:
        query = GetUserPhoneNumberQueryDTO(user_uuid=user_uuid)
        response: GetUserPhoneNumberResponseDTO = await self._repository.get_user_phone_number(input_dto=query)
        return response.phone_number

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_user_info(self, input_dto: GetUserInfoInputDTOV1) -> GetUserInfoOutputDTOV1:
        query = GetUserInfoQueryDTO(user_uuid=input_dto.user_uuid)
        response: GetUserInfoResponseDTO = await self._repository.get_user_info(input_dto=query)
        return GetUserInfoOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_user_internals(self, input_dto: UpdateUserInternalsInputDTOV1) -> None:
        command = UpdateUserInternalsCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_user_internals(command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def admin_update_user(self, input_dto: AdminUpdateUserInputDTOV1) -> None:
        command = AdminUpdateUserCommandDTO.model_validate(obj=input_dto)
        await self._repository.admin_update_user(command=command)
