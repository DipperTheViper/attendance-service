from archipy.configs.base_config import BaseConfig


class RuntimeConfig(BaseConfig):
    AUTH_GET_USER_CACHE_EXPIRATION_SECONDS: int = 11
    COMPANY_LATITUDE: float = 35.123444
    COMPANY_LONGITUDE: float = 51.123444
    COMPANY_GEOFENCE_RADIUS_METERS: float = 20.0
    SMS_MAX_RETRIES: int = 3
    SMS_RETRY_DELAY_SECONDS: int = 60


BaseConfig.set_global(RuntimeConfig())
