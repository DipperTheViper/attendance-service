from archipy.models.dtos.base_dtos import BaseDTO
from fastapi import UploadFile
from pydantic import field_validator

from src.models.types.file_types import WriteModeType, FileType, FileEntityType, FilePurposeType


class CreateFileInputDTOV1(BaseDTO):
    file_name: str
    file: UploadFile
    path: str
    is_secured: bool
    write_mode: WriteModeType
    file_type: FileType
    entity_type: FileEntityType
    purpose_type: FilePurposeType

    @field_validator("file_name")
    def validate_file_name(cls, value: str) -> str | None:
        if not value:
            raise ValueError("Name cannot be empty")
        # if not StorageUtils.validate_file_name(value):
        #     raise InvalidArgumentError(f"file extension must be in {RuntimeConfig().FILE.ALLOWED_EXTENSIONS}")
        stripped_name = value.replace(" ", "_")
        return stripped_name

    @field_validator("path")
    def validate_file_path(cls, value: str) -> str | None:
        if not value:
            raise ValueError("Path cannot be empty")
        stripped_path = value.replace(" ", "_")
        if not stripped_path.startswith("/"):
            return "/" + stripped_path
        return stripped_path


class CreateFileOutputDTOV1(BaseDTO):
    path: str
