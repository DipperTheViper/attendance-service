from archipy.models.errors import BaseError
from src.models.types.error_types import CustomErrorMessageType


class AlreadyCheckedInError(BaseError):
    def __init__(self):
        super().__init__(error=CustomErrorMessageType.ALREADY_CHECKED_IN.value)


class NoActiveCheckInError(BaseError):
    def __init__(self) -> None:
        super().__init__(error=CustomErrorMessageType.NO_ACTIVE_CHECK_IN.value)


class OutsideGeofenceError(BaseError):
    def __init__(self):
        super().__init__(error=CustomErrorMessageType.OUTSIDE_GEOFENCE.value)


class InsideGeofenceError(BaseError):
    def __init__(self):
        super().__init__(error=CustomErrorMessageType.INSIDE_GEOFENCE.value)
