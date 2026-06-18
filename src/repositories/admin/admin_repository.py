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
from src.repositories.admin.adapters.admin_postgres_adapter import AdminPostgresAdapter


class AdminRepository:
    def __init__(self, postgres_adapter: AdminPostgresAdapter):
        self._postgres_adapter: AdminPostgresAdapter = postgres_adapter

    async def create_app_config(self, input_dto: CreateAppConfigCommandDTO) -> CreateAppConfigResponseDTO:
        return await self._postgres_adapter.create_app_config(input_dto=input_dto)

    async def get_app_config(self, input_dto: GetAppConfigQueryDTO) -> GetAppConfigResponseDTO:
        return await self._postgres_adapter.get_app_config(input_dto=input_dto)

    async def search_app_configs(self, input_dto: SearchAppConfigQueryDTO) -> SearchAppConfigResponseDTO:
        return await self._postgres_adapter.search_app_configs(input_dto=input_dto)

    async def update_app_config(self, input_dto: UpdateAppConfigCommandDTO) -> None:
        await self._postgres_adapter.update_app_config(input_dto=input_dto)

    async def delete_app_config(self, input_dto: DeleteAppConfigCommandDTO) -> None:
        await self._postgres_adapter.delete_app_config(input_dto=input_dto)

    async def get_startup_config(
        self,
    ) -> GetStartupConfigResponseDTO:
        return await self._postgres_adapter.get_startup_config()
