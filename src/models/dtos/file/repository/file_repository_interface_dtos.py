from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from pydantic import StrictStr


class CreateFileCommandDTO(BaseDTO):
    file_name: StrictStr
    path: StrictStr
    is_secured: bool
    file_type: StrictStr
    entity_type: StrictStr
    purpose_type: StrictStr
    created_by: UUID | None = None
    updated_by: UUID | None = None


class CreateFileResponseDTO(BaseDTO):
    file_uuid: UUID


class GetFileQueryDTO(BaseDTO):
    file_uuid: UUID


class GetFileResponseDTO(BaseDTO):
    file_uuid: UUID
    file_name: StrictStr
    path: StrictStr
    is_secured: bool
    file_type: StrictStr
    entity_type: StrictStr
    purpose_type: StrictStr
    created_by: UUID | None = None
    updated_by: UUID | None = None


class UpdateFileCommandDTO(BaseDTO):
    file_uuid: UUID
    file_name: StrictStr | None = None
    path: StrictStr | None = None
    is_secured: bool | None = None
    file_type: StrictStr | None = None
    entity_type: StrictStr | None = None
    purpose_type: StrictStr | None = None
    created_by: UUID | None = None
    updated_by: UUID | None = None


class DeleteFileCommandDTO(BaseDTO):
    file_uuid: UUID


class SearchFileQueryDTO(BaseDTO):
    # Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchFileResponseDTO(BaseDTO):
    files: list[GetFileResponseDTO]
    total: int
