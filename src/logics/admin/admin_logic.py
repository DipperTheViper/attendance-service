from archipy.helpers.decorators.sqlalchemy_atomic import async_postgres_sqlalchemy_atomic_decorator
from uuid import UUID

from src.models.dtos.admin.domain.v1.admin_domain_interface_dtos import (
    CreateAppConfigInputDTOV1,
    CreateAppConfigOutputDTOV1,
    GetAppConfigInputDTOV1,
    GetAppConfigOutputDTOV1,
    UpdateAppConfigInputDTOV1,
    DeleteAppConfigInputDTOV1,
    SearchAppConfigInputDTOV1,
    SearchAppConfigOutputDTOV1,
    GetStartupConfigOutputDTOV1,
)
from src.models.dtos.admin.repository.admin_repository_interface_dtos import (
    CreateAppConfigCommandDTO,
    CreateAppConfigResponseDTO,
    GetAppConfigQueryDTO,
    GetAppConfigResponseDTO,
    UpdateAppConfigCommandDTO,
    DeleteAppConfigCommandDTO,
    SearchAppConfigQueryDTO,
    SearchAppConfigResponseDTO,
    GetStartupConfigResponseDTO,
)
from src.repositories.admin.admin_repository import AdminRepository
from src.utils.utils import Utils


class AdminLogic:
    def __init__(
        self,
        repository: AdminRepository,
    ) -> None:
        self._repository: AdminRepository = repository

    @async_postgres_sqlalchemy_atomic_decorator
    async def create_app_config(self, input_dto: CreateAppConfigInputDTOV1) -> CreateAppConfigOutputDTOV1:
        command = CreateAppConfigCommandDTO.model_validate(input_dto)
        response: CreateAppConfigResponseDTO = await self._repository.create_app_config(input_dto=command)
        return CreateAppConfigOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_app_config(self, input_dto: GetAppConfigInputDTOV1) -> GetAppConfigOutputDTOV1:
        query = GetAppConfigQueryDTO.model_validate(obj=input_dto)
        response: GetAppConfigResponseDTO = await self._repository.get_app_config(input_dto=query)
        return GetAppConfigOutputDTOV1.model_validate(obj=response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def search_app_configs(self, input_dto: SearchAppConfigInputDTOV1) -> SearchAppConfigOutputDTOV1:
        repository_dto = SearchAppConfigQueryDTO.model_validate(input_dto)
        response: SearchAppConfigResponseDTO = await self._repository.search_app_configs(input_dto=repository_dto)
        return SearchAppConfigOutputDTOV1.model_validate(response)

    @async_postgres_sqlalchemy_atomic_decorator
    async def update_app_config(self, input_dto: UpdateAppConfigInputDTOV1) -> None:
        command = UpdateAppConfigCommandDTO.model_validate(obj=input_dto)
        await self._repository.update_app_config(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def delete_app_config(self, input_dto: DeleteAppConfigInputDTOV1) -> None:
        command = DeleteAppConfigCommandDTO.model_validate(obj=input_dto)
        await self._repository.delete_app_config(input_dto=command)

    @async_postgres_sqlalchemy_atomic_decorator
    async def get_startup_config(self, version: str) -> GetStartupConfigOutputDTOV1:
        response: GetStartupConfigResponseDTO = await self._repository.get_startup_config()
        update_status = Utils.get_update_status(
            client_version=version,
            force_update_version=response.force_update_version,
            optional_update_version=response.optional_update_version,
        )
        return GetStartupConfigOutputDTOV1(**response.model_dump(), update_status=update_status)
