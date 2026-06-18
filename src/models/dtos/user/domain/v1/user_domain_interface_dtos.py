from datetime import datetime, date
from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from pydantic import StrictStr

from src.models.types.enums import *


class CreateUserRestInputDTOV1(BaseDTO):
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    phone_number: StrictStr
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    profile_picture_path: StrictStr | None = None
    date_of_birth: date | None = None
    user_type: UserType | None = None
    user_status: UserStatusType | None = None
    gender_type: StrictStr | None = None


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
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    phone_number: StrictStr
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    profile_picture_path: StrictStr | None = None
    user_type: UserType
    user_status: UserStatusType
    gender_type: StrictStr | None = None


class UpdateUserRestInputDTOV1(BaseDTO):
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    phone_number: StrictStr | None = None
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    profile_picture_path: StrictStr | None = None
    user_type: UserType | None = None
    user_status: UserStatusType | None = None
    gender_type: StrictStr | None = None


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
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    phone_number: StrictStr
    username: StrictStr | None = None
    hashed_password: StrictStr | None = None
    profile_picture_path: StrictStr | None = None
    user_type: UserType
    user_status: UserStatusType
    gender_type: StrictStr | None = None


class SearchUserOutputDTOV1(BaseDTO):
    users: list[UserItemDTOV1]
    total: int


class GetAdminUserInputDTOV1(BaseDTO):
    username: StrictStr | None = None
    user_uuid: UUID | None = None


class SearchAuthUserInputDTOV1(BaseDTO):
    phone_number: str
    referer_uuid: UUID | None = None


class SearchAuthUsersOutputDTOV1(BaseDTO):
    user_uuid: UUID


class GetAdminUserOutputDTOV1(BaseDTO):
    user_uuid: UUID
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    birth_date: datetime | None = None
    user_status: UserStatusType
    created_at: datetime
    hashed_password: StrictStr


class GetUserWithPhoneNumberInputDTOV1(BaseDTO):
    phone_number: str


class GetUserWithPhoneNumberOutputDTOV1(BaseDTO):
    user_uuid: UUID


class UpdateUserInternalsInputDTOV1(BaseDTO):
    user_uuid: UUID
    user_type: UserType | None = None
    user_status: UserStatusType | None = None
    gender_type: GenderType | None = None


class GetUserInfoInputDTOV1(BaseDTO):
    user_uuid: UUID


class GetUserInfoOutputDTOV1(BaseDTO):
    birth_date: datetime


class UpdateUserKYCTypeInputDTOV1(BaseDTO):
    user_uuid: UUID


class AdminUpdateUserRestInputDTOV1(BaseDTO):
    user_status: UserStatusType | None = None


class AdminUpdateUserInputDTOV1(AdminUpdateUserRestInputDTOV1):
    user_uuid: UUID
