from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from datetime import datetime
from uuid import UUID

from src.models.types.enums import AttendanceMethodType


class CreateAttendanceRecordCommandDTO(BaseDTO):
    user_uuid: UUID
    check_in_at: datetime
    method: AttendanceMethodType
    location: str | None = None


class CreateAttendanceRecordResponseDTO(BaseDTO):
    attendance_uuid: UUID


class GetOpenAttendanceQueryDTO(BaseDTO):
    user_uuid: UUID
    method: AttendanceMethodType | None = None


class GetOpenAttendanceResponseDTO(BaseDTO):
    attendance_uuid: UUID
    user_uuid: UUID
    check_in_at: datetime


class CheckOutCommandDTO(BaseDTO):
    attendance_uuid: UUID
    check_out_at: datetime


class SearchAttendanceRecordQueryDTO(BaseDTO):
    user_uuid: UUID | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class AttendanceRecordResponseDTO(BaseDTO):
    attendance_uuid: UUID
    user_uuid: UUID
    check_in_at: datetime
    check_out_at: datetime | None = None
    method: AttendanceMethodType
    location: str | None = None


class SearchAttendanceRecordResponseDTO(BaseDTO):
    records: list[AttendanceRecordResponseDTO]
    total: int


class DeleteAttendanceRecordCommandDTO(BaseDTO):
    attendance_uuid: UUID
