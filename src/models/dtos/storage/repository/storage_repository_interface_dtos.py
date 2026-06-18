from archipy.models.dtos.base_dtos import BaseDTO
from fastapi import UploadFile

from src.models.types.file_types import WriteModeType, FileType, FileEntityType, FilePurposeType


class CreateFileCommandDTO(BaseDTO):
    file_name: str
    file: UploadFile
    path: str
    is_secured: bool
    write_mode: WriteModeType
    file_type: FileType
    entity_type: FileEntityType
    purpose_type: FilePurposeType


class CreateFileResponseDTO(BaseDTO):
    path: str
