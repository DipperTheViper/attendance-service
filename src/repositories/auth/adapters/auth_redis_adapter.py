import json

from archipy.adapters.redis.adapters import AsyncRedisAdapter, AsyncRedisPort
from archipy.models.errors import InvalidArgumentError

from src.configs.runtime_config import RuntimeConfig
from src.models.dtos.auth.repository_interface.auth_repository_interface_dtos import (
    CreateTOTPCommandDTO,
    CreateTOTPResponseDTO,
    VerifyTOTPCommandDTO,
)
from src.models.vos.redis_vo import RedisVO


class AuthRedisAdapter(AsyncRedisAdapter):
    def __init__(self, adapter: AsyncRedisPort) -> None:
        super().__init__()
        self._adapter: AsyncRedisPort = adapter

    @classmethod
    def get_redis_key(cls, key_format: str, **args) -> str:
        return key_format.format(**args)

    async def create_totp(self, command: CreateTOTPCommandDTO) -> CreateTOTPResponseDTO:
        key: str = self.get_redis_key(
            key_format=RedisVO.totp_key,
            mobile_number=command.phone_number,
            nonce_code=command.nonce_code,
        )
        await self._adapter.set(
            name=key,
            value=command.model_dump_json(exclude_none=True, exclude_unset=True),
            ex=RuntimeConfig.global_config().AUTH.TOTP_EXPIRES_IN,
        )
        return CreateTOTPResponseDTO(nonce_code=command.nonce_code)

    async def verify_totp(self, command: VerifyTOTPCommandDTO) -> None:
        key: str = self.get_redis_key(
            key_format=RedisVO.totp_key,
            mobile_number=command.phone_number,
            nonce_code=command.nonce_code,
        )
        stored_totp: str = await self._adapter.get(key=key)
        if not stored_totp:
            raise InvalidArgumentError(argument_name="totp_code")

        totp: dict[str, any] = json.loads(stored_totp)
        await self._expire_totp(command=command)

        if not stored_totp or totp["totp_code"] != command.totp_code:
            raise InvalidArgumentError(argument_name="totp_code")

    async def _expire_totp(self, command: VerifyTOTPCommandDTO) -> None:
        key: str = self.get_redis_key(
            key_format=RedisVO.totp_key,
            mobile_number=command.phone_number,
            nonce_code=command.nonce_code,
        )
        await self._adapter.delete(key)
