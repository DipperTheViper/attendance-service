from enum import Enum
from http import HTTPStatus

from archipy.models.dtos.error_dto import ErrorDetailDTO, HTTP_AVAILABLE


class CustomErrorMessageType(Enum):
    INVALID_SECURITY_PIN = ErrorDetailDTO.create_error_detail(
        code="INVALID_SECURITY_PIN",
        message_en="your entered pin code is invalid",
        message_fa="کد پین وارد شده اشتباه است.",
        http_status=HTTPStatus.BAD_REQUEST if HTTP_AVAILABLE else None,
    )
