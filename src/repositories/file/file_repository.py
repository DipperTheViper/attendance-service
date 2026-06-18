from src.models.dtos.file.repository.file_repository_interface_dtos import (
    CreateFileCommandDTO,
    CreateFileResponseDTO,
    GetFileQueryDTO,
    GetFileResponseDTO,
    UpdateFileCommandDTO,
    DeleteFileCommandDTO,
    SearchFileQueryDTO,
    SearchFileResponseDTO,
)
from src.repositories.file.adapters.file_postgres_adapter import FilePostgresAdapter


class FileRepository:
    def __init__(self, postgres_adapter: FilePostgresAdapter):
        self._postgres_adapter: FilePostgresAdapter = postgres_adapter

    async def create_file(self, input_dto: CreateFileCommandDTO) -> CreateFileResponseDTO:
        return await self._postgres_adapter.create_file(input_dto=input_dto)

    async def get_file(self, input_dto: GetFileQueryDTO) -> GetFileResponseDTO:
        return await self._postgres_adapter.get_file(input_dto=input_dto)

    async def search_files(self, input_dto: SearchFileQueryDTO) -> SearchFileResponseDTO:
        return await self._postgres_adapter.search_files(input_dto=input_dto)

    async def update_file(self, input_dto: UpdateFileCommandDTO) -> None:
        await self._postgres_adapter.update_file(input_dto=input_dto)

    async def delete_file(self, input_dto: DeleteFileCommandDTO) -> None:
        await self._postgres_adapter.delete_file(input_dto=input_dto)
