from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from pydantic import StrictStr


class CreateFileRestInputDTOV1(BaseDTO):
    file_name: StrictStr
    path: StrictStr
    is_secured: bool
    file_type: StrictStr
    entity_type: StrictStr
    purpose_type: StrictStr


class CreateFileInputDTOV1(CreateFileRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreateFileRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreateFileOutputDTOV1(BaseDTO):
    file_uuid: UUID


class GetFileInputDTOV1(BaseDTO):
    file_uuid: UUID


class GetFileOutputDTOV1(BaseDTO):
    file_uuid: UUID
    file_name: StrictStr
    path: StrictStr
    is_secured: bool
    file_type: StrictStr
    entity_type: StrictStr
    purpose_type: StrictStr
    created_by: UUID | None = None
    updated_by: UUID | None = None


class UpdateFileRestInputDTOV1(BaseDTO):
    file_name: StrictStr | None = None
    path: StrictStr | None = None
    is_secured: bool | None = None
    file_type: StrictStr | None = None
    entity_type: StrictStr | None = None
    purpose_type: StrictStr | None = None


class UpdateFileInputDTOV1(UpdateFileRestInputDTOV1):
    file_uuid: UUID


class DeleteFileInputDTOV1(BaseDTO):
    file_uuid: UUID


class SearchFileInputDTOV1(BaseDTO):
    # Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]  # Replace with appropriate sort enum

    @classmethod
    def create(
        cls,
        page: int = 1,
        page_size: int = 10,
        sort_column: str = "created_at",
        sort_order: SortOrderType = SortOrderType.DESCENDING,
    ):
        pagination = PaginationDTO(page=page, page_size=page_size)
        sort_info = SortDTO[str](column=sort_column, order=sort_order)
        return cls(pagination=pagination, sort_info=sort_info)


class FileItemDTOV1(BaseDTO):
    file_uuid: UUID
    file_name: StrictStr
    path: StrictStr
    is_secured: bool
    file_type: StrictStr
    entity_type: StrictStr
    purpose_type: StrictStr
    created_by: UUID | None = None
    updated_by: UUID | None = None


class SearchFileOutputDTOV1(BaseDTO):
    files: list[FileItemDTOV1]
    total: int
