from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO
from archipy.models.types.sort_order_type import SortOrderType


class CreateReferralRestInputDTOV1(BaseDTO):
    pass


class CreateReferralInputDTOV1(CreateReferralRestInputDTOV1):
    user_uuid: UUID | None = None

    @classmethod
    def create(
        cls,
        user_uuid: UUID | None = None,
        input_dto: CreateReferralRestInputDTOV1 = None,
    ):
        if input_dto:
            return cls(user_uuid=user_uuid, **input_dto.model_dump(mode="json"))
        return cls(user_uuid=user_uuid)


class CreateReferralOutputDTOV1(BaseDTO):
    referral_uuid: UUID


class GetReferralInputDTOV1(BaseDTO):
    referral_uuid: UUID


class GetReferralOutputDTOV1(BaseDTO):
    referral_uuid: UUID
    referee_uuid: UUID
    referer_uuid: UUID


class UpdateReferralRestInputDTOV1(BaseDTO):
    pass


class UpdateReferralInputDTOV1(UpdateReferralRestInputDTOV1):
    referral_uuid: UUID


class DeleteReferralInputDTOV1(BaseDTO):
    referral_uuid: UUID


class SearchReferralInputDTOV1(BaseDTO):
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


class ReferralItemDTOV1(BaseDTO):
    referral_uuid: UUID
    referee_uuid: UUID
    referer_uuid: UUID


class SearchReferralOutputDTOV1(BaseDTO):
    referrals: list[ReferralItemDTOV1]
    total: int
