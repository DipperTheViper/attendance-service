from archipy.models.errors import AlreadyExistsError

from src.configs.runtime_config import RuntimeConfig
from src.models.dtos.storage.repository.storage_repository_interface_dtos import (
    CreateFileCommandDTO,
    CreateFileResponseDTO,
)
from src.models.types.file_types import WriteModeType
from src.utils.storage_utils import StorageUtils


class SystemStorageAdapter:
    def __init__(self, config: RuntimeConfig):
        self.config: RuntimeConfig = config

    async def create_file(self, input_dto: CreateFileCommandDTO) -> CreateFileResponseDTO:
        file_path = self._create_path(input_dto)

        with open(file_path, "wb") as file:
            file.write(await input_dto.file.read())

        output_path = StorageUtils.get_storage_path(
            path=input_dto.path,
            name=input_dto.file_name,
            is_secure=input_dto.is_secured,
        )
        return CreateFileResponseDTO(path=output_path.__str__())

    def _create_path(self, input_dto):
        dir_path = StorageUtils.get_dir_path(input_dto.path, input_dto.is_secured, config=self.config)
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = StorageUtils.get_file_path(
            path=input_dto.path,
            name=input_dto.file_name,
            is_secure=input_dto.is_secured,
            config=self.config,
        )
        if file_path.exists() and input_dto.write_mode == WriteModeType.WRITE:
            raise AlreadyExistsError(resource_type="FileEntity")
        return file_path
