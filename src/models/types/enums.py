from enum import Enum


class VerificationStatusType(str, Enum):
    Verified = "Verified"


class GenderType(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class FileType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class FileEntityType(str, Enum):
    NEWS = "NEWS"
    USER = "USER"
    ADS = "ADS"
    SLIDER = "SLIDER"


class FilePurposeType(str, Enum):
    PROFILE = "PROFILE"
    VIDEO_NEWS = "VIDEO_NEWS"
    PHOTO_NEWS = "PHOTO_NEWS"
    BANNER = "BANNER"
    THUMBNAIL = "THUMBNAIL"
    CONTENT_FILE = "CONTENT_FILE"


class UserType(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"


class DangerStatusType(str, Enum):
    SAFE = "SAFE"
    IN_DANGER = "IN_DANGER"
    POTENTIAL_DANGER = "POTENTIAL_DANGER"


class DangerTimerDurationType(str, Enum):
    MINUTES_5 = "MINUTES_5"
    MINUTES_15 = "MINUTES_15"
    MINUTES_30 = "MINUTES_30"
    HOURS_1 = "HOURS_1"
    HOURS_2 = "HOURS_2"
    HOURS_6 = "HOURS_6"
    HOURS_12 = "HOURS_12"
    HOURS_24 = "HOURS_24"


class ShelterRelationshipStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class TimelineMessageType(str, Enum):
    SAFE = "SAFE"
    HELP_REQUEST = "HELP_REQUEST"
    LOCATION_UPDATE = "LOCATION_UPDATE"
    GENERAL = "GENERAL"


class SubscriptionType(str, Enum):
    MONTHLY = "MONTHLY"
    QUARTER = "QUARTER"
    SEMIANNUAL = "SEMIANNUAL"
    ANNUAL = "ANNUAL"


class SubscriptionStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"


class NotificationType(str, Enum):
    DANGER_ALERT = "DANGER_ALERT"
    SHELTER_REQUEST = "SHELTER_REQUEST"
    TIMELINE_UPDATE = "TIMELINE_UPDATE"
    SYSTEM = "SYSTEM"
    SUBSCRIPTION = "SUBSCRIPTION"


class UpdateStatusType(str, Enum):
    FORCE_UPDATE = "FORCE_UPDATE"
    LATEST_UPDATE = "LATEST_UPDATE"
    OPTIONAL_UPDATE = "OPTIONAL_UPDATE"


class KYCLevelType(str, Enum):
    BASIC = "BASIC"
    ONE = "ONE"
    TWO = "TWO"
