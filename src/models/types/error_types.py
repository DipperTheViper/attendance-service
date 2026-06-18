from enum import Enum
from http import HTTPStatus

from archipy.models.dtos.error_dto import ErrorDetailDTO, HTTP_AVAILABLE


class CustomErrorMessageType(Enum):
    SUBSCRIPTION_NEEDED = ErrorDetailDTO.create_error_detail(
        code="SUBSCRIPTION_NEEDED",
        message_en="subscription needed for this feature",
        message_fa="استفاده از این اشتراک میخواد",
        http_status=HTTPStatus.PAYMENT_REQUIRED if HTTP_AVAILABLE else None,
    )

    INVALID_SECURITY_PIN = ErrorDetailDTO.create_error_detail(
        code="INVALID_SECURITY_PIN",
        message_en="your entered pin code is invalid",
        message_fa="کد پین وارد شده اشتباه است.",
        http_status=HTTPStatus.BAD_REQUEST if HTTP_AVAILABLE else None,
    )
