from archipy.configs.base_config import BaseConfig


class RuntimeConfig(BaseConfig):
    AUTH_GET_USER_CACHE_EXPIRATION_SECONDS: int = 11


BaseConfig.set_global(RuntimeConfig())
