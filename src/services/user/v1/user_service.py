from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from uuid import UUID

from src.configs.containers import ServiceContainer
from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import (
    GetUserInputDTOV1,
    GetUserOutputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.USER])


@routerV1.get(
    path="/{user_uuid}",
    response_model=GetUserOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_user(
    user_uuid: UUID,
    logic: UserLogic = Depends(Provide[ServiceContainer.user_logic]),
) -> GetUserOutputDTOV1:
    input_dto = GetUserInputDTOV1(user_uuid=user_uuid)
    return await logic.get_user(input_dto=input_dto)
