from archipy.configs.base_config import BaseConfig


class RuntimeConfig(BaseConfig):
    AUTH_GET_USER_CACHE_EXPIRATION_SECONDS: int = 11
    PUBLIC_BASE_DIR: str = "/app/media/static"
    SECURE_BASE_DIR: str = "/app/media"
    SECURE_BASE_URL: str = "https://api-yoop.fazelidev.ir"
    AUTH_CREATE_TOTP_CALLS_COUNT_LIMIT: int = 10
    AUTH_CREATE_TOTP_MINUTES_LIMIT: int = 1
    AUTH_VERIFY_TOTP_CALLS_COUNT_LIMIT: int = 10
    AUTH_VERIFY_TOTP_MINUTES_LIMIT: int = 1
    ADMIN_AUTH_LOGIN_CALLS_COUNT_LIMIT: int = 10
    ADMIN_AUTH_LOGIN_MINUTES_LIMIT: int = 1


BaseConfig.set_global(RuntimeConfig())
