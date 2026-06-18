from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from uuid import UUID
from datetime import datetime

from src.configs.containers import ServiceContainer
from src.logics.attendance.attendance_logic import AttendanceLogic
from src.models.dtos.attendance.domain.v1.attendance_domain_interface_dtos import (
    CheckInInputDTOV1,
    CheckOutInputDTOV1,
    GeoCheckInInputDTOV1,
    GeoCheckOutInputDTOV1,
    SearchAttendanceInputDTOV1,
    SearchAttendanceOutputDTOV1,
    GeoCheckOutInputRestDTOV1,
    GeoCheckInInputRestDTOV1,
    GeoAttendanceInputRestDTOV1,
    GeoAttendanceInputDTOV1,
)
from src.models.types.api_router_type import ApiRouterType

adminRouterV1: APIRouter = APIRouter(tags=[ApiRouterType.ADMIN])
routerV1: APIRouter = APIRouter(tags=[ApiRouterType.ATTENDANCE])


@routerV1.post(path="/{user_uuid}/attendance/check-in")
@inject
async def check_in(
    user_uuid: UUID,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    await logic.check_in(input_dto=CheckInInputDTOV1(user_uuid=user_uuid))


@routerV1.post(path="/{user_uuid}/attendance/check-out")
@inject
async def check_out(
    user_uuid: UUID,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    await logic.check_out(input_dto=CheckOutInputDTOV1(user_uuid=user_uuid))


@routerV1.post(path="/{user_uuid}/attendance/geo-check-in")
@inject
async def geo_check_in(
    user_uuid: UUID,
    input_dto: GeoCheckInInputRestDTOV1,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    input_dto = GeoCheckInInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    await logic.geo_check_in(input_dto=input_dto)


@routerV1.post(path="/{user_uuid}/attendance/geo-check-out")
@inject
async def geo_check_out(
    user_uuid: UUID,
    input_dto: GeoCheckOutInputRestDTOV1,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    input_dto = GeoCheckOutInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    await logic.geo_check_out(input_dto=input_dto)


@routerV1.post(path="/{user_uuid}/attendance/geo")
@inject
async def geo_attendance(
    user_uuid: UUID,
    input_dto: GeoAttendanceInputRestDTOV1,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    input_dto = GeoAttendanceInputDTOV1.create(user_uuid=user_uuid, input_dto=input_dto)
    await logic.geo_attendance(input_dto=input_dto)


@routerV1.get(
    path="/{user_uuid}/attendance",
    response_model=SearchAttendanceOutputDTOV1,
)
@inject
async def search_attendance(
    user_uuid: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> SearchAttendanceOutputDTOV1:
    input_dto = SearchAttendanceInputDTOV1.create(
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
        date_from=date_from,
        date_to=date_to,
    )
    return await logic.search_attendance_records(input_dto=input_dto)


@adminRouterV1.get(
    path="/attendance",
    response_model=SearchAttendanceOutputDTOV1,
)
@inject
async def admin_search_attendance(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    user_uuid: UUID | None = Query(default=None),
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> SearchAttendanceOutputDTOV1:
    input_dto = SearchAttendanceInputDTOV1.create(
        page=page,
        page_size=page_size,
        user_uuid=user_uuid,
        date_from=date_from,
        date_to=date_to,
    )
    return await logic.search_attendance_records(input_dto=input_dto)


@adminRouterV1.delete(path="/attendance/{attendance_uuid}")
@inject
async def admin_delete_attendance(
    attendance_uuid: UUID,
    logic: AttendanceLogic = Depends(Provide[ServiceContainer.attendance_logic]),
) -> None:
    await logic.delete_attendance_record(input_dto=DeleteAttendanceInputDTOV1(attendance_uuid=attendance_uuid))
