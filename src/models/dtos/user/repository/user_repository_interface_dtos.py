from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import *


class CreateUserCommandDTO(BaseDTO):
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: StrictStr


class CreateUserResponseDTO(BaseDTO):
    user_uuid: UUID


class GetUserQueryDTO(BaseDTO):
    user_uuid: UUID


class GetUserResponseDTO(BaseDTO):
    user_uuid: UUID
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: StrictStr


class UpdateUserCommandDTO(BaseDTO):
    user_uuid: UUID
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    phone_number: StrictStr | None = None
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: StrictStr | None = None


class DeleteUserCommandDTO(BaseDTO):
    user_uuid: UUID


class SearchUserQueryDTO(BaseDTO):
    # TODO: Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchUserResponseDTO(BaseDTO):
    users: list[GetUserResponseDTO]
    total: int
