from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType
from pydantic import StrictStr

from src.models.types.enums import *


class CreateAppConfigRestInputDTOV1(BaseDTO):
    force_update_version: StrictStr
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None


class CreateAppConfigInputDTOV1(CreateAppConfigRestInputDTOV1): ...


class CreateAppConfigOutputDTOV1(BaseDTO):
    app_config_uuid: UUID


class GetAppConfigInputDTOV1(BaseDTO):
    app_config_uuid: UUID


class GetAppConfigOutputDTOV1(BaseDTO):
    app_config_uuid: UUID
    force_update_version: StrictStr
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None
    is_active: bool


class UpdateAppConfigRestInputDTOV1(BaseDTO):
    force_update_version: StrictStr | None = None
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr | None = None
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None
    is_active: bool | None = None


class UpdateAppConfigInputDTOV1(UpdateAppConfigRestInputDTOV1):
    app_config_uuid: UUID


class DeleteAppConfigInputDTOV1(BaseDTO):
    app_config_uuid: UUID


class SearchAppConfigInputDTOV1(BaseDTO):
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


class AppConfigItemDTOV1(BaseDTO):
    app_config_uuid: UUID
    force_update_version: StrictStr
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None
    is_active: bool


class SearchAppConfigOutputDTOV1(BaseDTO):
    app_configs: list[AppConfigItemDTOV1]
    total: int


class GetStartupConfigOutputDTOV1(BaseDTO):
    force_update_version: StrictStr
    force_update_message: StrictStr | None = None
    optional_update_version: StrictStr
    optional_update_message: StrictStr | None = None
    update_link: StrictStr | None = None
    update_status: UpdateStatusType | None = None
