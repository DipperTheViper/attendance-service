from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

from src.models.dtos.referral.domain.v1.referral_domain_interface_dtos import (
    CreateReferralInputDTOV1,
    CreateReferralOutputDTOV1,
    GetReferralInputDTOV1,
    GetReferralOutputDTOV1,
    UpdateReferralInputDTOV1,
    DeleteReferralInputDTOV1,
    SearchReferralInputDTOV1,
    SearchReferralOutputDTOV1,
)
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
from src.repositories.referral.referral_repository import ReferralRepository


class ReferralLogic:
    def __init__(
        self,
        repository: ReferralRepository,
    ) -> None:
        self._repository: ReferralRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_referral(self, input_dto: CreateReferralInputDTOV1) -> CreateReferralOutputDTOV1:
        command = CreateReferralCommandDTO.model_validate(input_dto)
        response: CreateReferralResponseDTO = await self._repository.create_referral(input_dto=command)
        return CreateReferralOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_referral(self, input_dto: GetReferralInputDTOV1) -> GetReferralOutputDTOV1:
        query = GetReferralQueryDTO.model_validate(obj=input_dto)
        response: GetReferralResponseDTO = await self._repository.get_referral(input_dto=query)
        return GetReferralOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_referrals(self, input_dto: SearchReferralInputDTOV1) -> SearchReferralOutputDTOV1:
        repository_dto = SearchReferralQueryDTO.model_validate(input_dto)
        response: SearchReferralResponseDTO = await self._repository.search_referrals(input_dto=repository_dto)
        return SearchReferralOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_referral(self, input_dto: UpdateReferralInputDTOV1) -> None:
        command = UpdateReferralCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_referral(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_referral(self, input_dto: DeleteReferralInputDTOV1) -> None:
        command = DeleteReferralCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_referral(input_dto=command)
