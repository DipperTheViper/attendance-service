from datetime import datetime

from archipy.models.dtos.base_dtos import BaseDTO
from pydantic import StrictBool, StrictStr


class CreateTOTPCommandDTO(BaseDTO):
    totp_code: StrictStr
    nonce_code: StrictStr
    phone_number: StrictStr
    is_expire: StrictBool = False
    expire_time: datetime


class CreateTOTPResponseDTO(BaseDTO):
    nonce_code: StrictStr


class VerifyTOTPCommandDTO(BaseDTO):
    phone_number: StrictStr
    totp_code: StrictStr
    nonce_code: StrictStr
