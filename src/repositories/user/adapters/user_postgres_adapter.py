from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import select, update
from sqlalchemy.sql.expression import Select, Update

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
from src.models.entities import UserEntity


class UserPostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_user(self, input_dto: CreateUserCommandDTO) -> CreateUserResponseDTO:
        _entity = UserEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateUserResponseDTO.model_validate(obj=result)

    async def get_user(self, input_dto: GetUserQueryDTO) -> GetUserResponseDTO:
        select_query = select(UserEntity).where(UserEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=UserEntity.user_uuid,
            value=input_dto.user_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()
        if not entity:
            raise NotFoundError(resource_type=UserEntity.__name__)
        return GetUserResponseDTO.model_validate(obj=entity)

    async def get_user_by_username(self, input_dto: GetUserByUsernameQueryDTO) -> GetUserResponseDTO:
        select_query = select(UserEntity).where(UserEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=UserEntity.username,
            value=input_dto.username,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()
        if not entity:
            raise NotFoundError(resource_type=UserEntity.__name__)
        return GetUserResponseDTO.model_validate(obj=entity)

    async def search_users(self, input_dto: SearchUserQueryDTO) -> SearchUserResponseDTO:
        query: Select = select(UserEntity).where(UserEntity.is_deleted.is_(False))

        if input_dto.user_type:
            query = self._apply_filter(
                query=query,
                field=UserEntity.user_type,
                value=input_dto.user_type,
                operation=FilterOperationType.EQUAL,
            )

        if input_dto.phone_number:
            query = self._apply_filter(
                query=query,
                field=UserEntity.phone_number,
                value=input_dto.phone_number,
                operation=FilterOperationType.EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=UserEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )
        return SearchUserResponseDTO(users=entities, total=total)

    async def update_user(self, input_dto: UpdateUserCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"user_uuid"}, exclude_none=True)
        if not update_data:
            return
        update_query: Update = (
            update(UserEntity)
            .where(
                UserEntity.user_uuid == input_dto.user_uuid,
                UserEntity.is_deleted.is_(False),
            )
            .values(**update_data)
        )
        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=UserEntity.__name__)

    async def delete_user(self, input_dto: DeleteUserCommandDTO) -> None:
        delete_query = (
            update(UserEntity)
            .where(
                UserEntity.user_uuid == input_dto.user_uuid,
                UserEntity.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )
        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=UserEntity.__name__)
