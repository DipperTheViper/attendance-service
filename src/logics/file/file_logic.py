from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator

from src.models.dtos.file.domain.v1.file_domain_interface_dtos import (
    CreateFileInputDTOV1,
    CreateFileOutputDTOV1,
    GetFileInputDTOV1,
    GetFileOutputDTOV1,
    UpdateFileInputDTOV1,
    DeleteFileInputDTOV1,
    SearchFileInputDTOV1,
    SearchFileOutputDTOV1,
)
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
from src.repositories.file.file_repository import FileRepository


class FileLogic:
    def __init__(
        self,
        repository: FileRepository,
    ) -> None:
        self._repository: FileRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_file(self, input_dto: CreateFileInputDTOV1) -> CreateFileOutputDTOV1:
        command = CreateFileCommandDTO.model_validate(input_dto)
        response: CreateFileResponseDTO = await self._repository.create_file(input_dto=command)
        return CreateFileOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_file(self, input_dto: GetFileInputDTOV1) -> GetFileOutputDTOV1:
        query = GetFileQueryDTO.model_validate(obj=input_dto)
        response: GetFileResponseDTO = await self._repository.get_file(input_dto=query)
        return GetFileOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_files(self, input_dto: SearchFileInputDTOV1) -> SearchFileOutputDTOV1:
        repository_dto = SearchFileQueryDTO.model_validate(input_dto)
        response: SearchFileResponseDTO = await self._repository.search_files(input_dto=repository_dto)
        return SearchFileOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_file(self, input_dto: UpdateFileInputDTOV1) -> None:
        command = UpdateFileCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_file(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_file(self, input_dto: DeleteFileInputDTOV1) -> None:
        command = DeleteFileCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_file(input_dto=command)
