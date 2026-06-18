from uuid import UUID

from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from src.configs.containers import ServiceContainer
from src.logics.referral.referral_logic import ReferralLogic
from src.models.dtos.referral.domain.v1.referral_domain_interface_dtos import (
    CreateReferralInputDTOV1,
    CreateReferralOutputDTOV1,
    CreateReferralRestInputDTOV1,
    DeleteReferralInputDTOV1,
    GetReferralInputDTOV1,
    GetReferralOutputDTOV1,
    SearchReferralInputDTOV1,
    SearchReferralOutputDTOV1,
    UpdateReferralInputDTOV1,
    UpdateReferralRestInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.REFERRAL])


@routerV1.post(
    path="/{user_uuid}/referrals",
    response_model=CreateReferralOutputDTOV1,
)
@inject
async def create_referral(
    user_uuid: UUID,
    input_dto: CreateReferralRestInputDTOV1,
    logic: ReferralLogic = Depends(Provide[ServiceContainer.referral_logic]),
) -> CreateReferralOutputDTOV1:
    input_dto = CreateReferralInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_referral(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/referrals/{referral_uuid}",
    response_model=GetReferralOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_referral(
    user_uuid: UUID,
    referral_uuid: UUID,
    logic: ReferralLogic = Depends(Provide[ServiceContainer.referral_logic]),
) -> GetReferralOutputDTOV1:
    input_dto = GetReferralInputDTOV1(referral_uuid=referral_uuid)
    return await logic.get_referral(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/referrals",
    response_model=SearchReferralOutputDTOV1,
)
@inject
async def search_referrals(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: ReferralLogic = Depends(Provide[ServiceContainer.referral_logic]),
) -> SearchReferralOutputDTOV1:
    input_dto = SearchReferralInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_referrals(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/referrals/{referral_uuid}",
)
@inject
async def update_referral(
    user_uuid: UUID,
    referral_uuid: UUID,
    input_dto: UpdateReferralRestInputDTOV1,
    logic: ReferralLogic = Depends(Provide[ServiceContainer.referral_logic]),
) -> None:
    update_dto = UpdateReferralInputDTOV1(**input_dto.model_dump(), referral_uuid=referral_uuid)
    await logic.update_referral(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/referrals/{referral_uuid}",
)
@inject
async def delete_referral(
    user_uuid: UUID,
    referral_uuid: UUID,
    logic: ReferralLogic = Depends(Provide[ServiceContainer.referral_logic]),
) -> None:
    input_dto = DeleteReferralInputDTOV1(referral_uuid=referral_uuid)
    await logic.delete_referral(input_dto=input_dto)
