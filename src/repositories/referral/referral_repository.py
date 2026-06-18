from src.models.dtos.referral.repository.referral_repository_interface_dtos import (
    CreateReferralCommandDTO,
    CreateReferralResponseDTO,
    GetReferralQueryDTO,
    GetReferralResponseDTO,
    UpdateReferralCommandDTO,
    DeleteReferralCommandDTO,
    SearchReferralQueryDTO,
    SearchReferralResponseDTO,
)
from src.repositories.referral.adapters.referral_postgres_adapter import ReferralPostgresAdapter


class ReferralRepository:
    def __init__(self, postgres_adapter: ReferralPostgresAdapter):
        self._postgres_adapter: ReferralPostgresAdapter = postgres_adapter

    async def create_referral(self, input_dto: CreateReferralCommandDTO) -> CreateReferralResponseDTO:
        return await self._postgres_adapter.create_referral(input_dto=input_dto)

    async def get_referral(self, input_dto: GetReferralQueryDTO) -> GetReferralResponseDTO:
        return await self._postgres_adapter.get_referral(input_dto=input_dto)

    async def search_referrals(self, input_dto: SearchReferralQueryDTO) -> SearchReferralResponseDTO:
        return await self._postgres_adapter.search_referrals(input_dto=input_dto)

    async def update_referral(self, input_dto: UpdateReferralCommandDTO) -> None:
        await self._postgres_adapter.update_referral(input_dto=input_dto)

    async def delete_referral(self, input_dto: DeleteReferralCommandDTO) -> None:
        await self._postgres_adapter.delete_referral(input_dto=input_dto)
