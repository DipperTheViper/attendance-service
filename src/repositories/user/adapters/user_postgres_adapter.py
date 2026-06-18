from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import delete, select, update, func, or_
from sqlalchemy.sql.expression import Select, Update

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
    UpdateUserKYCTypeCommandDTO,
)
from src.models.entities import UserEntity
from src.models.types.enums import UserType, UserStatusType


class UserPostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_user(self, input_dto: CreateUserCommandDTO) -> CreateUserResponseDTO:
        user: UserEntity = UserEntity(phone_number=input_dto.phone_number)
        result = await self._adapter.create(entity=user)
        return CreateUserResponseDTO.model_validate(obj=result)

    async def get_user(self, input_dto: GetUserQueryDTO) -> GetUserResponseDTO:
        select_query = select(UserEntity)
        _query = self._apply_filter(
            query=select_query,
            field=UserEntity.user_uuid,
            value=input_dto.user_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        user = result.scalar()

        if not user:
            raise NotFoundError(resource_type=UserEntity.__name__)

        return GetUserResponseDTO.model_validate(obj=user)

    async def get_admin_auth_user(self, input_dto: GetUserQueryDTO) -> GetUserResponseDTO:
        _query = select(UserEntity)
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.user_uuid,
            value=input_dto.user_uuid,
            operation=FilterOperationType.EQUAL,
        )
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.username,
            operation=FilterOperationType.IS_NOT_NULL,
            value="",
        )
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.user_type,
            value=[
                UserType.ADMIN,
            ],
            operation=FilterOperationType.IN_LIST,
        )
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.is_deleted,
            value=False,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        user = result.scalar()

        if not user:
            raise NotFoundError(resource_type=UserEntity.__name__)

        return GetUserResponseDTO.model_validate(obj=user)

    async def get_admin_user(self, input_dto: GetAdminUserQueryDTO) -> GetAdminUserResponseDTO:
        _query = select(UserEntity)
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.username,
            value=input_dto.username,
            operation=FilterOperationType.EQUAL,
        )
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.user_status,
            value=UserStatusType.ACTIVE,
            operation=FilterOperationType.EQUAL,
        )
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.user_type,
            value=[UserType.ADMIN],
            operation=FilterOperationType.IN_LIST,
        )
        _query = self._apply_filter(
            query=_query,
            field=UserEntity.is_deleted,
            value=False,
            operation=FilterOperationType.EQUAL,
        )

        result = await self._adapter.execute(statement=_query)
        user = result.scalar()

        if not user:
            raise NotFoundError(resource_type=UserEntity.__name__)

        return GetAdminUserResponseDTO.model_validate(obj=user)

    async def search_users(self, input_dto: SearchUserQueryDTO) -> SearchUserResponseDTO:
        query: Select = select(UserEntity)

        if input_dto.first_name:
            query = self._apply_filter(
                query=query,
                field=UserEntity.first_name,
                value=f"%{input_dto.first_name}%",
                operation=FilterOperationType.ILIKE,
            )

        if input_dto.last_name:
            query = self._apply_filter(
                query=query,
                field=UserEntity.last_name,
                value=f"%{input_dto.last_name}%",
                operation=FilterOperationType.ILIKE,
            )
        if input_dto.full_name:
            full_name_filters = [
                func.concat(UserEntity.first_name, " ", UserEntity.last_name).ilike(
                    f"%{input_dto.full_name}%",
                ),
            ] + [
                func.concat(UserEntity.last_name, " ", UserEntity.first_name).ilike(
                    f"%{input_dto.full_name}%",
                ),
            ]
            query = query.filter(or_(*full_name_filters))

        users, total = await self._adapter.execute_search_query(
            query=query,
            entity=UserEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchUserResponseDTO(users=users, total=total)

    async def update_user(self, input_dto: UpdateUserCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"user_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(UserEntity).where(UserEntity.user_uuid == input_dto.user_uuid).values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=UserEntity.__name__)

    async def delete_user(self, input_dto: DeleteUserCommandDTO) -> None:
        delete_query = delete(UserEntity).where(UserEntity.user_uuid == input_dto.user_uuid)

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=UserEntity.__name__)

    async def get_user_with_phone_number(
        self,
        input_dto: GetUserWithPhoneNumberQueryDTO,
    ) -> GetUserWithPhoneNumberResponseDTO:
        select_query = select(UserEntity.user_uuid).where(UserEntity.phone_number == input_dto.phone_number)
        result = await self._adapter.execute(statement=select_query)
        user = result.mappings().first()
        if not user:
            raise NotFoundError(resource_type=UserEntity.__name__)
        return GetUserWithPhoneNumberResponseDTO.model_validate(obj=user)

    async def get_user_phone_number(self, input_dto: GetUserPhoneNumberQueryDTO) -> GetUserPhoneNumberResponseDTO:
        select_query = select(UserEntity.phone_number).where(UserEntity.user_uuid == input_dto.user_uuid)
        result = await self._adapter.execute(statement=select_query)
        user = result.mappings().first()
        if not user:
            raise NotFoundError(resource_type=UserEntity.__name__)
        return GetUserPhoneNumberResponseDTO.model_validate(obj=user)

    async def update_user_internals(self, command: UpdateUserInternalsCommandDTO) -> None:
        update_query = (
            update(UserEntity)
            .where(UserEntity.user_uuid == command.user_uuid)
            .values(**command.model_dump(exclude={"user_uuid"}, exclude_none=True))
        )
        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=UserEntity.__name__)

    async def get_user_info(self, input_dto: GetUserInfoQueryDTO) -> GetUserInfoResponseDTO:
        select_query = select(UserEntity.national_code, UserEntity.birth_date).where(
            UserEntity.user_uuid == input_dto.user_uuid,
        )
        result = await self._adapter.execute(statement=select_query)
        user = result.mappings().first()
        return GetUserInfoResponseDTO.model_validate(obj=user)

    async def admin_update_user(self, command: AdminUpdateUserCommandDTO) -> None:
        update_data = command.model_dump(exclude={"user_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = update(UserEntity).where(UserEntity.user_uuid == command.user_uuid).values(**update_data)

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=UserEntity.__name__)
