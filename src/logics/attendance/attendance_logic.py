from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from uuid import UUID

from src.models.dtos.attendance.domain.v1.attendance_domain_interface_dtos import (
    CreateAttendanceRecordInputDTOV1,
    CreateAttendanceRecordOutputDTOV1,
    GetAttendanceRecordInputDTOV1,
    GetAttendanceRecordOutputDTOV1,
    UpdateAttendanceRecordInputDTOV1,
    DeleteAttendanceRecordInputDTOV1,
    SearchAttendanceRecordInputDTOV1,
    SearchAttendanceRecordOutputDTOV1,
)
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
from src.repositories.attendance.attendance_repository import AttendanceRepository


class AttendanceLogic:
    def __init__(
        self,
        repository: AttendanceRepository,
    ) -> None:
        self._repository: AttendanceRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_attendance_record(
        self,
        input_dto: CreateAttendanceRecordInputDTOV1,
    ) -> CreateAttendanceRecordOutputDTOV1:
        command = CreateAttendanceRecordCommandDTO.model_validate(input_dto)
        response: CreateAttendanceRecordResponseDTO = await self._repository.create_attendance_record(input_dto=command)
        return CreateAttendanceRecordOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_attendance_record(self, input_dto: GetAttendanceRecordInputDTOV1) -> GetAttendanceRecordOutputDTOV1:
        query = GetAttendanceRecordQueryDTO.model_validate(obj=input_dto)
        response: GetAttendanceRecordResponseDTO = await self._repository.get_attendance_record(input_dto=query)
        return GetAttendanceRecordOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_attendance_records(
        self,
        input_dto: SearchAttendanceRecordInputDTOV1,
    ) -> SearchAttendanceRecordOutputDTOV1:
        repository_dto = SearchAttendanceRecordQueryDTO.model_validate(input_dto)
        response: SearchAttendanceRecordResponseDTO = await self._repository.search_attendance_records(
            input_dto=repository_dto,
        )
        return SearchAttendanceRecordOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_attendance_record(self, input_dto: UpdateAttendanceRecordInputDTOV1) -> None:
        command = UpdateAttendanceRecordCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_attendance_record(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_attendance_record(self, input_dto: DeleteAttendanceRecordInputDTOV1) -> None:
        command = DeleteAttendanceRecordCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_attendance_record(input_dto=command)
