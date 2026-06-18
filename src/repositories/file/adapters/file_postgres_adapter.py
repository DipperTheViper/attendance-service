from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import select, update
from sqlalchemy.sql.expression import Select, Update

from src.models.dtos.file.repository.file_repository_interface_dtos import (
    CreateFileCommandDTO,
    CreateFileResponseDTO,
    GetFileQueryDTO,
    GetFileResponseDTO,
    UpdateFileCommandDTO,
    DeleteFileCommandDTO,
    SearchFileQueryDTO,
    SearchFileResponseDTO,
)
from src.models.entities import FileEntity


class FilePostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_file(self, input_dto: CreateFileCommandDTO) -> CreateFileResponseDTO:
        _entity = FileEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateFileResponseDTO.model_validate(obj=result)

    async def get_file(self, input_dto: GetFileQueryDTO) -> GetFileResponseDTO:
        select_query = select(FileEntity)
        _query = self._apply_filter(
            query=select_query,
            field=FileEntity.file_uuid,
            value=input_dto.file_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=FileEntity.__name__)

        return GetFileResponseDTO.model_validate(obj=entity)

    async def search_files(self, input_dto: SearchFileQueryDTO) -> SearchFileResponseDTO:
        query: Select = select(FileEntity)
        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=FileEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )
        # Add search filters here as needed

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=FileEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchFileResponseDTO(files=entities, total=total)

    async def update_file(self, input_dto: UpdateFileCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"file_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(FileEntity).where(FileEntity.file_uuid == input_dto.file_uuid).values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=FileEntity.__name__)

    async def delete_file(self, input_dto: DeleteFileCommandDTO) -> None:
        delete_query = (
            update(FileEntity)
            .where(
                FileEntity.file_uuid == input_dto.file_uuid,
                FileEntity.is_deleted._is(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=FileEntity.__name__)
