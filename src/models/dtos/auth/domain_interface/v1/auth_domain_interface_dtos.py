from datetime import datetime

from archipy.models.dtos.base_dtos import BaseDTO
from pydantic import StrictStr, field_validator

from src.utils.utils import Utils


class CreateTOTPInputDTOV1(BaseDTO):
    phone_number: StrictStr
    referral_code: StrictStr | None = None

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        Utils.validate_iranian_phone_number(v)
        return v


class CreateTOTPOutputDTOV1(BaseDTO):
    expires_in: datetime
    phone_number: StrictStr
    nonce_code: StrictStr


class VerifyTOTPInputDTOV1(BaseDTO):
    totp_code: StrictStr
    phone_number: StrictStr
    nonce_code: StrictStr

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        Utils.validate_iranian_phone_number(v)
        return v


class VerifyTOTPOutputDTOV1(BaseDTO):
    access_token: StrictStr
    refresh_token: StrictStr


class RefreshTokenInputDTOV1(BaseDTO):
    refresh_token: StrictStr


class RefreshTokenOutputDTOV1(BaseDTO):
    access_token: StrictStr


class LoginInputDTOV1(BaseDTO):
    username: StrictStr
    password: StrictStr


class LoginOutputDTOV1(BaseDTO):
    access_token: StrictStr
    refresh_token: StrictStr
