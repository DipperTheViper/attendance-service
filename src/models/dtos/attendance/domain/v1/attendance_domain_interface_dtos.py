from archipy.models.dtos.base_dtos import BaseDTO
from pydantic import StrictStr
from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from datetime import datetime
from uuid import UUID

from src.models.types.enums import AttendanceMethodType


class CheckInInputDTOV1(BaseDTO):
    user_uuid: UUID


class CheckOutInputDTOV1(BaseDTO):
    user_uuid: UUID


class GeoCheckInInputRestDTOV1(BaseDTO):
    latitude: float
    longitude: float


class GeoCheckInInputDTOV1(GeoCheckInInputRestDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: GeoCheckInInputRestDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class GeoCheckOutInputRestDTOV1(BaseDTO):
    latitude: float
    longitude: float


class GeoCheckOutInputDTOV1(GeoCheckOutInputRestDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: GeoCheckOutInputRestDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class AttendanceOutputDTOV1(BaseDTO):
    attendance_uuid: UUID
    user_uuid: UUID
    check_in_at: datetime
    check_out_at: datetime | None = None
    method: AttendanceMethodType
    location: StrictStr | None = None


class SearchAttendanceInputDTOV1(BaseDTO):
    user_uuid: UUID | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]

    @classmethod
    def create(
        cls,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "check_in_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
        user_uuid: UUID | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(
            pagination=pagination,
            sort_info=sort_info,
            user_uuid=user_uuid,
            date_from=date_from,
            date_to=date_to,
        )


class SearchAttendanceOutputDTOV1(BaseDTO):
    records: list[AttendanceOutputDTOV1]
    total: int
