from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import UserType


class CreateUserInputDTOV1(BaseDTO):
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: UserType = UserType.USER


class CreateUserOutputDTOV1(BaseDTO):
    user_uuid: UUID


class GetUserInputDTOV1(BaseDTO):
    user_uuid: UUID


class GetUserOutputDTOV1(BaseDTO):
    user_uuid: UUID
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: UserType


class GetUserByUsernameInputDTOV1(BaseDTO):
    username: StrictStr


class GetUserByUsernameOutputDTOV1(BaseDTO):
    user_uuid: UUID
    hashed_password: StrictStr
    user_type: UserType


class UpdateUserRestInputDTOV1(BaseDTO):
    phone_number: StrictStr | None = None
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None


class UpdateUserInputDTOV1(UpdateUserRestInputDTOV1):
    user_uuid: UUID


class DeleteUserInputDTOV1(BaseDTO):
    user_uuid: UUID


class SearchUserInputDTOV1(BaseDTO):
    user_type: UserType | None = None
    phone_number: StrictStr | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]

    @classmethod
    def create(
        cls,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
        user_type: UserType | None = None,
        phone_number: StrictStr | None = None,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(pagination=pagination, sort_info=sort_info, user_type=user_type, phone_number=phone_number)


class UserItemDTOV1(BaseDTO):
    user_uuid: UUID
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: UserType


class SearchUserOutputDTOV1(BaseDTO):
    users: list[UserItemDTOV1]
    total: int
