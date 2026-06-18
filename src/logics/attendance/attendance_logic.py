from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from archipy.models.errors import InvalidArgumentError
from datetime import datetime, timezone

from src.models.dtos.attendance.domain.v1.attendance_domain_interface_dtos import (
    CheckInInputDTOV1,
    CheckOutInputDTOV1,
    GeoCheckInInputDTOV1,
    GeoCheckOutInputDTOV1,
    SearchAttendanceInputDTOV1,
    SearchAttendanceOutputDTOV1,
    GeoAttendanceInputDTOV1,
)
from src.models.dtos.attendance.repository.attendance_repository_interface_dtos import (
    CheckOutCommandDTO,
    CreateAttendanceRecordCommandDTO,
    GetOpenAttendanceQueryDTO,
    SearchAttendanceRecordQueryDTO,
)
from src.models.exceptions.attendance import (
    AlreadyCheckedInError,
    NoActiveCheckInError,
    OutsideGeofenceError,
    InsideGeofenceError,
)
from src.models.types.enums import AttendanceMethodType
from src.repositories.attendance.attendance_repository import AttendanceRepository
from src.utils.utils import Utils


class AttendanceLogic:
    def __init__(self, repository: AttendanceRepository) -> None:
        self._repository: AttendanceRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def check_in(self, input_dto: CheckInInputDTOV1) -> None:
        open_record = await self._repository.get_open_attendance(
            input_dto=GetOpenAttendanceQueryDTO(user_uuid=input_dto.user_uuid),
        )
        if open_record:
            raise AlreadyCheckedInError()

        command = CreateAttendanceRecordCommandDTO(
            user_uuid=input_dto.user_uuid,
            check_in_at=datetime.now(timezone.utc),
            method=AttendanceMethodType.MANUAL,
        )
        await self._repository.create_attendance_record(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def check_out(self, input_dto: CheckOutInputDTOV1) -> None:
        open_record = await self._repository.get_open_attendance(
            input_dto=GetOpenAttendanceQueryDTO(user_uuid=input_dto.user_uuid, method=AttendanceMethodType.MANUAL),
        )
        if not open_record:
            raise NoActiveCheckInError()

        await self._repository.check_out(
            input_dto=CheckOutCommandDTO(
                attendance_uuid=open_record.attendance_uuid,
                check_out_at=datetime.now(timezone.utc),
            ),
        )

    @async_postgres_sqlalchemy_atomic_decorator
    async def geo_check_in(self, input_dto: GeoCheckInInputDTOV1) -> None:
        within = await self._repository.is_within_geofence(latitude=input_dto.latitude, longitude=input_dto.longitude)
        if not within:
            raise OutsideGeofenceError()

        open_record = await self._repository.get_open_attendance(
            input_dto=GetOpenAttendanceQueryDTO(user_uuid=input_dto.user_uuid),
        )
        if open_record:
            raise AlreadyCheckedInError()

        command = CreateAttendanceRecordCommandDTO(
            user_uuid=input_dto.user_uuid,
            check_in_at=datetime.now(timezone.utc),
            method=AttendanceMethodType.GEO,
            location=Utils.make_point_wkt(input_dto.latitude, input_dto.longitude),
        )
        await self._repository.create_attendance_record(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def geo_check_out(self, input_dto: GeoCheckOutInputDTOV1) -> None:
        within = await self._repository.is_within_geofence(latitude=input_dto.latitude, longitude=input_dto.longitude)
        if within:
            raise InsideGeofenceError()

        open_record = await self._repository.get_open_attendance(
            input_dto=GetOpenAttendanceQueryDTO(user_uuid=input_dto.user_uuid, method=AttendanceMethodType.GEO),
        )
        if not open_record:
            raise NoActiveCheckInError()

        await self._repository.check_out(
            input_dto=CheckOutCommandDTO(
                attendance_uuid=open_record.attendance_uuid,
                check_out_at=datetime.now(timezone.utc),
            ),
        )

    @async_postgres_sqlalchemy_atomic_decorator
    async def geo_attendance(self, input_dto: GeoAttendanceInputDTOV1) -> None:
        within = await self._repository.is_within_geofence(latitude=input_dto.latitude, longitude=input_dto.longitude)

        if within:
            open_record = await self._repository.get_open_attendance(
                input_dto=GetOpenAttendanceQueryDTO(user_uuid=input_dto.user_uuid, method=AttendanceMethodType.GEO),
            )
            if open_record:
                raise AlreadyCheckedInError()
            await self._repository.create_attendance_record(
                input_dto=CreateAttendanceRecordCommandDTO(
                    user_uuid=input_dto.user_uuid,
                    check_in_at=datetime.now(timezone.utc),
                    method=AttendanceMethodType.GEO,
                    location=Utils.make_point_wkt(input_dto.latitude, input_dto.longitude),
                ),
            )
        else:
            open_record = await self._repository.get_open_attendance(
                input_dto=GetOpenAttendanceQueryDTO(user_uuid=input_dto.user_uuid, method=AttendanceMethodType.GEO),
            )
            if not open_record:
                raise NoActiveCheckInError()
            await self._repository.check_out(
                input_dto=CheckOutCommandDTO(
                    attendance_uuid=open_record.attendance_uuid,
                    check_out_at=datetime.now(timezone.utc),
                ),
            )

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_attendance_records(self, input_dto: SearchAttendanceInputDTOV1) -> SearchAttendanceOutputDTOV1:
        repository_dto = SearchAttendanceRecordQueryDTO.model_validate(input_dto)
        response = await self._repository.search_attendance_records(input_dto=repository_dto)
        return SearchAttendanceOutputDTOV1.model_validate(response)
