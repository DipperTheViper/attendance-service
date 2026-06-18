from uuid import UUID

from archipy.adapters.redis.adapters import AsyncRedisAdapter, AsyncRedisPort
from archipy.models.errors import UnauthenticatedError

from src.configs.runtime_config import RuntimeConfig
from src.models.dtos.auth.repository_interface.auth_repository_interface_dtos import (
    CreateSessionCommandDTO,
    DeleteSessionCommandDTO,
    GetSessionQueryDTO,
    GetSessionResponseDTO,
)


class AuthRedisAdapter(AsyncRedisAdapter):
    def __init__(self, adapter: AsyncRedisPort) -> None:
        super().__init__()
        self._adapter: AsyncRedisPort = adapter

    async def create_session(self, command: CreateSessionCommandDTO) -> None:
        await self._adapter.set(
            name=command.access_token,
            value=str(command.user_uuid),
            ex=RuntimeConfig.global_config().AUTH.ACCESS_TOKEN_EXPIRES_IN,
        )

    async def get_session(self, query: GetSessionQueryDTO) -> GetSessionResponseDTO:
        user_uuid: str = await self._adapter.get(key=query.access_token)
        if not user_uuid:
            raise UnauthenticatedError()
        return GetSessionResponseDTO(user_uuid=UUID(user_uuid))

    async def delete_session(self, command: DeleteSessionCommandDTO) -> None:
        await self._adapter.delete(command.access_token)
