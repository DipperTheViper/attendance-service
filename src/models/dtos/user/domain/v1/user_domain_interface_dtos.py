from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreateUserRestInputDTOV1(BaseDTO):
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: StrictStr


class CreateUserInputDTOV1(CreateUserRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreateUserRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreateUserOutputDTOV1(BaseDTO):
    user_uuid: UUID


class GetUserInputDTOV1(BaseDTO):
    user_uuid: UUID


class GetUserOutputDTOV1(BaseDTO):
    user_uuid: UUID
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: StrictStr


class UpdateUserRestInputDTOV1(BaseDTO):
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    phone_number: StrictStr | None = None
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: StrictStr | None = None


class UpdateUserInputDTOV1(UpdateUserRestInputDTOV1):
    user_uuid: UUID


class DeleteUserInputDTOV1(BaseDTO):
    user_uuid: UUID


class SearchUserInputDTOV1(BaseDTO):
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


class UserItemDTOV1(BaseDTO):
    user_uuid: UUID
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: StrictStr


class SearchUserOutputDTOV1(BaseDTO):
    users: list[UserItemDTOV1]
    total: int
