from src.models.dtos.attendance.repository.attendance_repository_interface_dtos import (
    CheckOutCommandDTO,
    CreateAttendanceRecordCommandDTO,
    CreateAttendanceRecordResponseDTO,
    GetOpenAttendanceQueryDTO,
    GetOpenAttendanceResponseDTO,
    SearchAttendanceRecordQueryDTO,
    SearchAttendanceRecordResponseDTO,
    DeleteAttendanceRecordCommandDTO,
)
from src.repositories.attendance.adapters.attendance_postgres_adapter import AttendancePostgresAdapter


class AttendanceRepository:
    def __init__(self, postgres_adapter: AttendancePostgresAdapter):
        self._postgres_adapter: AttendancePostgresAdapter = postgres_adapter

    async def create_attendance_record(
        self,
        input_dto: CreateAttendanceRecordCommandDTO,
    ) -> CreateAttendanceRecordResponseDTO:
        return await self._postgres_adapter.create_attendance_record(input_dto=input_dto)

    async def get_open_attendance(self, input_dto: GetOpenAttendanceQueryDTO) -> GetOpenAttendanceResponseDTO | None:
        return await self._postgres_adapter.get_open_attendance(input_dto=input_dto)

    async def check_out(self, input_dto: CheckOutCommandDTO) -> None:
        await self._postgres_adapter.check_out(input_dto=input_dto)

    async def is_within_geofence(self, latitude: float, longitude: float) -> bool:
        return await self._postgres_adapter.is_within_geofence(latitude=latitude, longitude=longitude)

    async def search_attendance_records(
        self,
        input_dto: SearchAttendanceRecordQueryDTO,
    ) -> SearchAttendanceRecordResponseDTO:
        return await self._postgres_adapter.search_attendance_records(input_dto=input_dto)

    async def delete_attendance_record(self, input_dto: DeleteAttendanceRecordCommandDTO) -> None:
        await self._postgres_adapter.delete_attendance_record(input_dto=input_dto)
