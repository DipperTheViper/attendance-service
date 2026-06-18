from enum import Enum
from http import HTTPStatus

from archipy.models.dtos.error_dto import ErrorDetailDTO, HTTP_AVAILABLE


class CustomErrorMessageType(Enum):
    ALREADY_CHECKED_IN = ErrorDetailDTO.create_error_detail(
        code="ALREADY_CHECKED_IN",
        message_en="You already have an active check-in.",
        message_fa="شما قبلاً ثبت ورود داشته‌اید.",
        http_status=HTTPStatus.CONFLICT if HTTP_AVAILABLE else None,
    )

    NO_ACTIVE_CHECK_IN = ErrorDetailDTO.create_error_detail(
        code="NO_ACTIVE_CHECK_IN",
        message_en="No active check-in found.",
        message_fa="ثبت ورود فعالی یافت نشد.",
        http_status=HTTPStatus.NOT_FOUND if HTTP_AVAILABLE else None,
    )

    OUTSIDE_GEOFENCE = ErrorDetailDTO.create_error_detail(
        code="OUTSIDE_GEOFENCE",
        message_en="You are outside the company geofence.",
        message_fa="شما خارج از محدوده مکانی شرکت هستید.",
        http_status=HTTPStatus.BAD_REQUEST if HTTP_AVAILABLE else None,
    )

    INSIDE_GEOFENCE = ErrorDetailDTO.create_error_detail(
        code="INSIDE_GEOFENCE",
        message_en="You are still inside the company geofence.",
        message_fa="شما هنوز در محدوده مکانی شرکت هستید.",
        http_status=HTTPStatus.BAD_REQUEST if HTTP_AVAILABLE else None,
    )

    INVALID_CREDENTIALS = ErrorDetailDTO.create_error_detail(
        code="INVALID_CREDENTIALS",
        message_en="Username or password is incorrect.",
        message_fa="نام کاربری یا رمز عبور اشتباه است.",
        http_status=HTTPStatus.UNAUTHORIZED if HTTP_AVAILABLE else None,
    )
