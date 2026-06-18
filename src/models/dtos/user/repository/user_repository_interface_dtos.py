from datetime import datetime, date
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from pydantic import StrictStr

from src.models.types.enums import *


class CreateUserCommandDTO(BaseDTO):
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    phone_number: StrictStr
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    profile_picture_path: StrictStr | None = None
    user_type: UserType | None = None
    user_status: UserStatusType | None = None
    gender_type: StrictStr | None = None


class CreateUserResponseDTO(BaseDTO):
    user_uuid: UUID


class GetUserQueryDTO(BaseDTO):
    user_uuid: UUID


class GetUserResponseDTO(BaseDTO):
    user_uuid: UUID
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    phone_number: StrictStr
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    profile_picture_path: StrictStr | None = None
    user_type: UserType
    user_status: UserStatusType
    gender_type: StrictStr | None = None


class UpdateUserCommandDTO(BaseDTO):
    user_uuid: UUID
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    phone_number: StrictStr | None = None
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    profile_picture_path: StrictStr | None = None
    user_type: UserType | None = None
    user_status: UserStatusType | None = None
    gender_type: StrictStr | None = None


class DeleteUserCommandDTO(BaseDTO):
    user_uuid: UUID


class SearchUserQueryDTO(BaseDTO):
    # Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchUserResponseDTO(BaseDTO):
    users: list[GetUserResponseDTO]
    total: int


class GetAdminUserQueryDTO(BaseDTO):
    username: StrictStr | None = None
    user_uuid: UUID | None = None


class GetAdminUserResponseDTO(BaseDTO):
    user_uuid: UUID
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    birth_date: datetime | None = None
    user_status: UserStatusType
    created_at: datetime
    hashed_password: StrictStr


class GetUserWithPhoneNumberQueryDTO(BaseDTO):
    phone_number: StrictStr


class GetUserWithPhoneNumberResponseDTO(BaseDTO):
    user_uuid: UUID


class GetUserPhoneNumberQueryDTO(BaseDTO):
    user_uuid: UUID


class GetUserPhoneNumberResponseDTO(BaseDTO):
    phone_number: StrictStr


class GetUserInfoQueryDTO(BaseDTO):
    user_uuid: UUID


class GetUserInfoResponseDTO(BaseDTO):
    birth_date: datetime


class UpdateUserInternalsCommandDTO(BaseDTO):
    user_uuid: UUID
    user_type: UserType | None = None
    user_status: UserStatusType | None = None
    gender_type: GenderType | None = None


class UpdateUserKYCTypeCommandDTO(BaseDTO):
    user_uuid: UUID


class AdminUpdateUserCommandDTO(BaseDTO):
    user_uuid: UUID
    user_status: UserStatusType | None = None


class GetBaseUserResponseDTO(BaseDTO):
    user_uuid: UUID
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_status: UserStatusType
    created_at: datetime
    gender_type: GenderType | None = None
    phone_number: StrictStr
    user_type: UserType
