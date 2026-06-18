from src.models.dtos.attendance.repository.attendance_repository_interface_dtos import (
    CreateAttendanceRecordCommandDTO,
    CreateAttendanceRecordResponseDTO,
    GetAttendanceRecordQueryDTO,
    GetAttendanceRecordResponseDTO,
    UpdateAttendanceRecordCommandDTO,
    DeleteAttendanceRecordCommandDTO,
    SearchAttendanceRecordQueryDTO,
    SearchAttendanceRecordResponseDTO,
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

    async def get_attendance_record(self, input_dto: GetAttendanceRecordQueryDTO) -> GetAttendanceRecordResponseDTO:
        return await self._postgres_adapter.get_attendance_record(input_dto=input_dto)

    async def search_attendance_records(
        self,
        input_dto: SearchAttendanceRecordQueryDTO,
    ) -> SearchAttendanceRecordResponseDTO:
        return await self._postgres_adapter.search_attendance_records(input_dto=input_dto)

    async def update_attendance_record(self, input_dto: UpdateAttendanceRecordCommandDTO) -> None:
        await self._postgres_adapter.update_attendance_record(input_dto=input_dto)

    async def delete_attendance_record(self, input_dto: DeleteAttendanceRecordCommandDTO) -> None:
        await self._postgres_adapter.delete_attendance_record(input_dto=input_dto)
