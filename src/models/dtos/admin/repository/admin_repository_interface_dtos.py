from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from pydantic import StrictStr


class CreateAppConfigCommandDTO(BaseDTO):
    force_update_version: StrictStr
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None


class CreateAppConfigResponseDTO(BaseDTO):
    app_config_uuid: UUID


class GetAppConfigQueryDTO(BaseDTO):
    app_config_uuid: UUID


class GetAppConfigResponseDTO(BaseDTO):
    app_config_uuid: UUID
    force_update_version: StrictStr
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None
    is_active: bool


class UpdateAppConfigCommandDTO(BaseDTO):
    app_config_uuid: UUID
    force_update_version: StrictStr | None = None
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr | None = None
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None
    is_active: bool | None = None


class DeleteAppConfigCommandDTO(BaseDTO):
    app_config_uuid: UUID


class SearchAppConfigQueryDTO(BaseDTO):
    # Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchAppConfigResponseDTO(BaseDTO):
    app_configs: list[GetAppConfigResponseDTO]
    total: int


class GetStartupConfigResponseDTO(BaseDTO):
    force_update_version: StrictStr | None = None
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr | None = None
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None
