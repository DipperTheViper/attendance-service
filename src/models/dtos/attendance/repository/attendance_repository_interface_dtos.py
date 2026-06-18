from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreateAttendanceRecordCommandDTO(BaseDTO):
    user_uuid: UUID
    check_in_at: datetime
    check_out_at: datetime | None = None
    method: StrictStr
    latitude: float | None = None
    longitude: float | None = None


class CreateAttendanceRecordResponseDTO(BaseDTO):
    attendance_uuid: UUID


class GetAttendanceRecordQueryDTO(BaseDTO):
    attendance_uuid: UUID


class GetAttendanceRecordResponseDTO(BaseDTO):
    attendance_uuid: UUID
    user_uuid: UUID
    check_in_at: datetime
    check_out_at: datetime | None = None
    method: StrictStr
    latitude: float | None = None
    longitude: float | None = None


class UpdateAttendanceRecordCommandDTO(BaseDTO):
    attendance_uuid: UUID
    user_uuid: UUID | None = None
    check_in_at: datetime | None = None
    check_out_at: datetime | None = None
    method: StrictStr | None = None
    latitude: float | None = None
    longitude: float | None = None


class DeleteAttendanceRecordCommandDTO(BaseDTO):
    attendance_uuid: UUID


class SearchAttendanceRecordQueryDTO(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchAttendanceRecordResponseDTO(BaseDTO):
    attendance_records: list[GetAttendanceRecordResponseDTO]
    total: int
