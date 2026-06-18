from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from pydantic import StrictStr
from uuid import UUID

from src.models.types.enums import UserType


class CreateUserCommandDTO(BaseDTO):
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: UserType = UserType.USER


class CreateUserResponseDTO(BaseDTO):
    user_uuid: UUID


class GetUserQueryDTO(BaseDTO):
    user_uuid: UUID


class GetUserByUsernameQueryDTO(BaseDTO):
    username: StrictStr


class GetUserResponseDTO(BaseDTO):
    user_uuid: UUID
    username: StrictStr
    hashed_password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None
    user_type: UserType


class UpdateUserCommandDTO(BaseDTO):
    user_uuid: UUID
    phone_number: StrictStr | None = None
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None


class DeleteUserCommandDTO(BaseDTO):
    user_uuid: UUID


class SearchUserQueryDTO(BaseDTO):
    user_type: UserType | None = None
    phone_number: StrictStr | None = None
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchUserResponseDTO(BaseDTO):
    users: list[GetUserResponseDTO]
    total: int
