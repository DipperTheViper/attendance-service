from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import delete, select, update, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select, Update

from src.models.dtos.admin.repository.admin_repository_interface_dtos import (
    CreateAppConfigCommandDTO,
    CreateAppConfigResponseDTO,
    GetAppConfigQueryDTO,
    GetAppConfigResponseDTO,
    UpdateAppConfigCommandDTO,
    DeleteAppConfigCommandDTO,
    SearchAppConfigQueryDTO,
    SearchAppConfigResponseDTO,
    GetStartupConfigResponseDTO,
)
from src.models.entities import AppConfigEntity


class AdminPostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_app_config(self, input_dto: CreateAppConfigCommandDTO) -> CreateAppConfigResponseDTO:
        _entity = AppConfigEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateAppConfigResponseDTO.model_validate(obj=result)

    async def get_app_config(self, input_dto: GetAppConfigQueryDTO) -> GetAppConfigResponseDTO:
        select_query = select(AppConfigEntity)
        _query = self._apply_filter(
            query=select_query,
            field=AppConfigEntity.app_config_uuid,
            value=input_dto.app_config_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=AppConfigEntity.__name__)

        return GetAppConfigResponseDTO.model_validate(obj=entity)

    async def search_app_configs(self, input_dto: SearchAppConfigQueryDTO) -> SearchAppConfigResponseDTO:
        query: Select = select(AppConfigEntity)
        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=AppConfigEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )
        # Add search filters here as needed

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=AppConfigEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchAppConfigResponseDTO(app_configs=entities, total=total)

    async def update_app_config(self, input_dto: UpdateAppConfigCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"app_config_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(AppConfigEntity)
            .where(AppConfigEntity.app_config_uuid == input_dto.app_config_uuid)
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=AppConfigEntity.__name__)

    async def delete_app_config(self, input_dto: DeleteAppConfigCommandDTO) -> None:
        delete_query = (
            update(AppConfigEntity)
            .where(
                AppConfigEntity.app_config_uuid == input_dto.app_config_uuid,
                AppConfigEntity.is_deleted._is(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=AppConfigEntity.__name__)

    async def get_startup_config(
        self,
    ) -> GetStartupConfigResponseDTO:
        select_query = select(AppConfigEntity)
        _query = self._apply_filter(
            query=select_query,
            field=AppConfigEntity.is_active,
            value=True,
            operation=FilterOperationType.EQUAL,
        )
        _query = _query.order_by(AppConfigEntity.created_at.desc())
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=AppConfigEntity.__name__)

        return GetStartupConfigResponseDTO.model_validate(obj=entity)
