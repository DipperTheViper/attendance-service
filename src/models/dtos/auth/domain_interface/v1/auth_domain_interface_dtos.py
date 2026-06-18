from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from pydantic import StrictStr


class RegisterInputDTOV1(BaseDTO):
    username: StrictStr
    password: StrictStr
    phone_number: StrictStr
    first_name: StrictStr | None = None
    last_name: StrictStr | None = None


class RegisterOutputDTOV1(BaseDTO):
    user_uuid: UUID
    access_token: StrictStr


class LoginInputDTOV1(BaseDTO):
    username: StrictStr
    password: StrictStr


class LoginOutputDTOV1(BaseDTO):
    user_uuid: UUID
    access_token: StrictStr


class LogoutInputDTOV1(BaseDTO):
    access_token: StrictStr
