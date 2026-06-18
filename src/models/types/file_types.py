from archipy.models.types.base_types import BaseType


class WriteModeType(BaseType):
    WRITE = "WRITE"
    REWRITE = "REWRITE"


class FileType(BaseType):
    """Types of files that can be stored in the system."""

    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class FileEntityType(BaseType):
    """Entity types associated with files."""

    KYC_VIDEO = "KYC_VIDEO"
    FIAT_DEPOSIT = "FIAT_DEPOSIT"


class FilePurposeType(BaseType):
    """Purpose types for files."""

    PROFILE = "PROFILE"
    VERIFICATION = "VERIFICATION"
    IDENTITY = "IDENTITY"
    RECEIPT = "RECEIPT"
