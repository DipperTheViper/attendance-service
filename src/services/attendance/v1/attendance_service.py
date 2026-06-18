from archipy.models.errors import NotFoundError
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from src.configs.containers import ServiceContainer
from src.logics.attendance.attendance_logic import AttendanceLogic
from src.models.dtos.attendance.domain.v1.attendance_domain_interface_dtos import (
    CreateAttendanceRecordInputDTOV1,
    CreateAttendanceRecordOutputDTOV1,
    CreateAttendanceRecordRestInputDTOV1,
    DeleteAttendanceRecordInputDTOV1,
    GetAttendanceRecordInputDTOV1,
    GetAttendanceRecordOutputDTOV1,
    SearchAttendanceRecordInputDTOV1,
    SearchAttendanceRecordOutputDTOV1,
    UpdateAttendanceRecordInputDTOV1,
    UpdateAttendanceRecordRestInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType
from src.utils.utils import Utils

routerV1: APIRouter = APIRouter(tags=[ApiRouterType.ATTENDANCE])


@routerV1.post(
    path="/{user_uuid}/attendance-records",
    response_model=CreateAttendanceRecordOutputDTOV1,
)
@inject
async def create_attendance_record(
    user_uuid: UUID,
    input_dto: CreateAttendanceRecordRestInputDTOV1,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> CreateAttendanceRecordOutputDTOV1:
    input_dto = CreateAttendanceRecordInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    return await logic.create_attendance_record(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/attendance-records/{attendance_uuid}",
    response_model=GetAttendanceRecordOutputDTOV1,
    responses=Utils.get_fastapi_exception_responses([NotFoundError]),
)
@inject
async def get_attendance_record(
    user_uuid: UUID,
    attendance_uuid: UUID,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> GetAttendanceRecordOutputDTOV1:
    input_dto = GetAttendanceRecordInputDTOV1(attendance_uuid=attendance_uuid)
    return await logic.get_attendance_record(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/attendance-records",
    response_model=SearchAttendanceRecordOutputDTOV1,
)
@inject
async def search_attendance_records(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> SearchAttendanceRecordOutputDTOV1:
    input_dto = SearchAttendanceRecordInputDTOV1.create(
        page=page,
        page_size=page_size,
    )
    return await logic.search_attendance_records(input_dto=input_dto)


@routerV1.put(
    path="/{user_uuid}/attendance-records/{attendance_uuid}",
)
@inject
async def update_attendance_record(
    user_uuid: UUID,
    attendance_uuid: UUID,
    input_dto: UpdateAttendanceRecordRestInputDTOV1,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    update_dto = UpdateAttendanceRecordInputDTOV1(**input_dto.model_dump(), attendance_uuid=attendance_uuid)
    await logic.update_attendance_record(input_dto=update_dto)


@routerV1.delete(
    path="/{user_uuid}/attendance-records/{attendance_uuid}",
)
@inject
async def delete_attendance_record(
    user_uuid: UUID,
    attendance_uuid: UUID,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    input_dto = DeleteAttendanceRecordInputDTOV1(attendance_uuid=attendance_uuid)
    await logic.delete_attendance_record(input_dto=input_dto)
