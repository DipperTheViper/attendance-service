from enum import Enum


class UserType(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class AttendanceMethodType(str, Enum):
    MANUAL = "MANUAL"
    GEO = "GEO"
