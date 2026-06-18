from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from sqlalchemy import delete, select, update, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select, Update

from src.models.dtos.attendance.repository.attendance_repository_interface_dtos import (
    CreateAttendanceRecordCommandDTO,
    CreateAttendanceRecordResponseDTO,
    GetAttendanceRecordQueryDTO,
    GetAttendanceRecordResponseDTO,
    UpdateAttendanceRecordCommandDTO,
    DeleteAttendanceRecordCommandDTO,
    SearchAttendanceRecordQueryDTO,
    SearchAttendanceRecordResponseDTO,
)
from src.models.entities import AttendanceRecordEntity


class AttendancePostgresAdapter(SQLAlchemyFilterMixin):
    def __init__(self, adapter: AsyncPostgresSQLAlchemyAdapter) -> None:
        self._adapter: AsyncPostgresSQLAlchemyAdapter = adapter

    async def create_attendance_record(
        self,
        input_dto: CreateAttendanceRecordCommandDTO,
    ) -> CreateAttendanceRecordResponseDTO:
        _entity = AttendanceRecordEntity(**input_dto.model_dump())
        result = await self._adapter.create(entity=_entity)
        return CreateAttendanceRecordResponseDTO.model_validate(obj=result)

    async def get_attendance_record(self, input_dto: GetAttendanceRecordQueryDTO) -> GetAttendanceRecordResponseDTO:
        select_query = select(AttendanceRecordEntity).where(AttendanceRecordEntity.is_deleted.is_(False))
        _query = self._apply_filter(
            query=select_query,
            field=AttendanceRecordEntity.attendance_uuid,
            value=input_dto.attendance_uuid,
            operation=FilterOperationType.EQUAL,
        )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()

        if not entity:
            raise NotFoundError(resource_type=AttendanceRecordEntity.__name__)

        return GetAttendanceRecordResponseDTO.model_validate(obj=entity)

    async def search_attendance_records(
        self,
        input_dto: SearchAttendanceRecordQueryDTO,
    ) -> SearchAttendanceRecordResponseDTO:
        query: Select = select(AttendanceRecordEntity).where(AttendanceRecordEntity.is_deleted.is_(False))

        if input_dto.user_uuid:
            query = self._apply_filter(
                query=query,
                field=AttendanceRecordEntity.user_uuid,
                value=input_dto.user_uuid,
                operation=FilterOperationType.EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=AttendanceRecordEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        return SearchAttendanceRecordResponseDTO(attendance_records=entities, total=total)

    async def update_attendance_record(self, input_dto: UpdateAttendanceRecordCommandDTO) -> None:
        update_data = input_dto.model_dump(exclude={"attendance_uuid"}, exclude_none=True)
        if not update_data:
            return

        update_query: Update = (
            update(AttendanceRecordEntity)
            .where(
                AttendanceRecordEntity.attendance_uuid == input_dto.attendance_uuid,
                AttendanceRecordEntity.is_deleted.is_(False),
            )
            .values(**update_data)
        )

        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=AttendanceRecordEntity.__name__)

    async def delete_attendance_record(self, input_dto: DeleteAttendanceRecordCommandDTO) -> None:
        delete_query = (
            update(AttendanceRecordEntity)
            .where(
                AttendanceRecordEntity.attendance_uuid == input_dto.attendance_uuid,
                AttendanceRecordEntity.is_deleted.is_(False),
            )
            .values(is_deleted=True)
        )

        result = await self._adapter.execute(statement=delete_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=AttendanceRecordEntity.__name__)
