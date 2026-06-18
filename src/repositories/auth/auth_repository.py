from src.models.dtos.auth.repository_interface.auth_repository_interface_dtos import (
    CreateTOTPCommandDTO,
    CreateTOTPResponseDTO,
    VerifyTOTPCommandDTO,
)
from src.repositories.auth.adapters.auth_redis_adapter import AuthRedisAdapter


class AuthRepository:
    def __init__(self, redis_adapter: AuthRedisAdapter):
        self._redis_adapter = redis_adapter

    async def create_totp(self, command: CreateTOTPCommandDTO) -> CreateTOTPResponseDTO:
        return await self._redis_adapter.create_totp(command=command)

    async def verify_totp(self, command: VerifyTOTPCommandDTO) -> None:
        await self._redis_adapter.verify_totp(command=command)
