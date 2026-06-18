from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreateAttendanceRecordRestInputDTOV1(BaseDTO):
    user_uuid: UUID
    check_in_at: datetime
    check_out_at: datetime | None = None
    method: StrictStr
    latitude: float | None = None
    longitude: float | None = None


class CreateAttendanceRecordInputDTOV1(CreateAttendanceRecordRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreateAttendanceRecordRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreateAttendanceRecordOutputDTOV1(BaseDTO):
    attendance_uuid: UUID


class GetAttendanceRecordInputDTOV1(BaseDTO):
    attendance_uuid: UUID


class GetAttendanceRecordOutputDTOV1(BaseDTO):
    attendance_uuid: UUID
    user_uuid: UUID
    check_in_at: datetime
    check_out_at: datetime | None = None
    method: StrictStr
    latitude: float | None = None
    longitude: float | None = None


class UpdateAttendanceRecordRestInputDTOV1(BaseDTO):
    user_uuid: UUID | None = None
    check_in_at: datetime | None = None
    check_out_at: datetime | None = None
    method: StrictStr | None = None
    latitude: float | None = None
    longitude: float | None = None


class UpdateAttendanceRecordInputDTOV1(UpdateAttendanceRecordRestInputDTOV1):
    attendance_uuid: UUID


class DeleteAttendanceRecordInputDTOV1(BaseDTO):
    attendance_uuid: UUID


class SearchAttendanceRecordInputDTOV1(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]  # Replace with appropriate sort enum

    @classmethod
    def create(
        cls,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(pagination=pagination, sort_info=sort_info)


class AttendanceRecordItemDTOV1(BaseDTO):
    attendance_uuid: UUID
    user_uuid: UUID
    check_in_at: datetime
    check_out_at: datetime | None = None
    method: StrictStr
    latitude: float | None = None
    longitude: float | None = None


class SearchAttendanceRecordOutputDTOV1(BaseDTO):
    attendance_records: list[AttendanceRecordItemDTOV1]
    total: int
