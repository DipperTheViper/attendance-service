from archipy.adapters.base.sqlalchemy.adapters import SQLAlchemyFilterMixin
from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.models.errors import NotFoundError
from archipy.models.types.base_types import FilterOperationType
from geoalchemy2 import Geography
from geoalchemy2.functions import ST_DWithin, ST_MakePoint, ST_SetSRID
from geoalchemy2.shape import to_shape
from sqlalchemy import select, update, cast, literal
from sqlalchemy.sql.expression import Select, Update

from src.configs.runtime_config import RuntimeConfig
from src.models.dtos.attendance.repository.attendance_repository_interface_dtos import (
    CheckOutCommandDTO,
    CreateAttendanceRecordCommandDTO,
    CreateAttendanceRecordResponseDTO,
    GetOpenAttendanceQueryDTO,
    GetOpenAttendanceResponseDTO,
    SearchAttendanceRecordQueryDTO,
    SearchAttendanceRecordResponseDTO,
    AttendanceRecordResponseDTO,
    DeleteAttendanceRecordCommandDTO,
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

    async def get_open_attendance(self, input_dto: GetOpenAttendanceQueryDTO) -> GetOpenAttendanceResponseDTO | None:
        select_query = select(AttendanceRecordEntity).where(
            AttendanceRecordEntity.is_deleted.is_(False),
            AttendanceRecordEntity.check_out_at.is_(None),
        )
        _query = self._apply_filter(
            query=select_query,
            field=AttendanceRecordEntity.user_uuid,
            value=input_dto.user_uuid,
            operation=FilterOperationType.EQUAL,
        )
        if input_dto.method:
            _query = self._apply_filter(
                query=_query,
                field=AttendanceRecordEntity.method,
                value=input_dto.method,
                operation=FilterOperationType.EQUAL,
            )
        result = await self._adapter.execute(statement=_query)
        entity = result.scalar()
        if not entity:
            return None
        return GetOpenAttendanceResponseDTO.model_validate(obj=entity)

    async def check_out(self, input_dto: CheckOutCommandDTO) -> None:
        update_query: Update = (
            update(AttendanceRecordEntity)
            .where(
                AttendanceRecordEntity.attendance_uuid == input_dto.attendance_uuid,
                AttendanceRecordEntity.is_deleted.is_(False),
            )
            .values(check_out_at=input_dto.check_out_at)
        )
        result = await self._adapter.execute(statement=update_query)
        if result.rowcount == 0:
            raise NotFoundError(resource_type=AttendanceRecordEntity.__name__)

    async def is_within_geofence(self, latitude: float, longitude: float) -> bool:
        config = RuntimeConfig.global_config()

        user_point = cast(ST_SetSRID(ST_MakePoint(literal(longitude), literal(latitude)), 4326), Geography(srid=4326))
        company_point = cast(
            ST_SetSRID(ST_MakePoint(literal(config.COMPANY_LONGITUDE), literal(config.COMPANY_LATITUDE)), 4326),
            Geography(srid=4326),
        )

        query = select(ST_DWithin(user_point, company_point, literal(config.COMPANY_GEOFENCE_RADIUS_METERS)))
        result = await self._adapter.execute(statement=query)
        return result.scalar()

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

        if input_dto.date_from:
            query = self._apply_filter(
                query=query,
                field=AttendanceRecordEntity.check_in_at,
                value=input_dto.date_from,
                operation=FilterOperationType.GREATER_THAN_OR_EQUAL,
            )

        if input_dto.date_to:
            query = self._apply_filter(
                query=query,
                field=AttendanceRecordEntity.check_in_at,
                value=input_dto.date_to,
                operation=FilterOperationType.LESS_THAN_OR_EQUAL,
            )

        entities, total = await self._adapter.execute_search_query(
            query=query,
            entity=AttendanceRecordEntity,
            sort_info=input_dto.sort_info,
            pagination=input_dto.pagination,
        )

        records = []
        for entity in entities:
            location_str = None
            if entity.location is not None:
                location_str = to_shape(entity.location).wkt
            records.append(
                AttendanceRecordResponseDTO(
                    attendance_uuid=entity.attendance_uuid,
                    user_uuid=entity.user_uuid,
                    check_in_at=entity.check_in_at,
                    check_out_at=entity.check_out_at,
                    method=entity.method,
                    location=location_str,
                ),
            )

        return SearchAttendanceRecordResponseDTO(records=records, total=total)

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
