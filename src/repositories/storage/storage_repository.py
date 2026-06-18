from src.models.dtos.storage.repository.storage_repository_interface_dtos import (
    CreateFileCommandDTO,
    CreateFileResponseDTO,
)
from src.repositories.storage.adapters.system_storage_adapter import SystemStorageAdapter


class StorageRepository:
    def __init__(self, system_adapter: SystemStorageAdapter):
        self._system_adapter: SystemStorageAdapter = system_adapter

    async def create_file(self, input_dto: CreateFileCommandDTO) -> CreateFileResponseDTO:
        return await self._system_adapter.create_file(input_dto)
