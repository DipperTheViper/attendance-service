from src.models.dtos.auth.repository_interface.auth_repository_interface_dtos import (
    CreateSessionCommandDTO,
    DeleteSessionCommandDTO,
    GetSessionQueryDTO,
    GetSessionResponseDTO,
)
from src.repositories.auth.adapters.auth_redis_adapter import AuthRedisAdapter


class AuthRepository:
    def __init__(self, redis_adapter: AuthRedisAdapter):
        self._redis_adapter = redis_adapter

    async def create_session(self, command: CreateSessionCommandDTO) -> None:
        await self._redis_adapter.create_session(command=command)

    async def get_session(self, query: GetSessionQueryDTO) -> GetSessionResponseDTO:
        return await self._redis_adapter.get_session(query=query)

    async def delete_session(self, command: DeleteSessionCommandDTO) -> None:
        await self._redis_adapter.delete_session(command=command)
