from src.models.dtos.storage.domain.v1.storage_domain_interface_dtos import CreateFileInputDTOV1, CreateFileOutputDTOV1
from src.models.dtos.storage.repository.storage_repository_interface_dtos import CreateFileCommandDTO
from src.repositories.storage.storage_repository import StorageRepository
from src.utils.storage_utils import StorageUtils


class StorageLogic:
    def __init__(self, repository: StorageRepository):
        self.repository: StorageRepository = repository

    async def create_file(self, input_dto: CreateFileInputDTOV1) -> CreateFileOutputDTOV1:
        try:
            command = CreateFileCommandDTO.model_validate(input_dto)
            response = await self.repository.create_file(command)
            return CreateFileOutputDTOV1.model_validate(response)
        except Exception as exception:
            StorageUtils.capture_exception(exception)
            raise exception
