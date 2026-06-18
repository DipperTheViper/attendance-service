from uuid import UUID

from archipy.models.dtos.base_dtos import BaseDTO
from archipy.models.dtos.pagination_dto import PaginationDTO
from archipy.models.dtos.sort_dto import SortDTO


class CreateReferralCommandDTO(BaseDTO):
    referee_uuid: UUID
    referer_uuid: UUID


class CreateReferralResponseDTO(BaseDTO):
    referral_uuid: UUID


class GetReferralQueryDTO(BaseDTO):
    referral_uuid: UUID


class GetReferralResponseDTO(BaseDTO):
    referral_uuid: UUID
    referee_uuid: UUID
    referer_uuid: UUID


class UpdateReferralCommandDTO(BaseDTO):
    referral_uuid: UUID
    referee_uuid: UUID | None = None
    referer_uuid: UUID | None = None


class DeleteReferralCommandDTO(BaseDTO):
    referral_uuid: UUID


class SearchReferralQueryDTO(BaseDTO):
    # Add search fields as needed
    pagination: PaginationDTO
    sort_info: SortDTO[str]


class SearchReferralResponseDTO(BaseDTO):
    referrals: list[GetReferralResponseDTO]
    total: int
