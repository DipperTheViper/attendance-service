import hashlib
import hmac

from archipy.helpers.utils.base_utils import BaseUtils

from src.configs.runtime_config import RuntimeConfig


class Utils(BaseUtils):
    @classmethod
    def encrypt_username(cls, value: str) -> str:
        key = RuntimeConfig.global_config().AUTH.SECRET_KEY
        if hasattr(key, "get_secret_value"):
            key = key.get_secret_value()
        return hmac.new(key.encode(), value.encode(), hashlib.sha256).hexdigest()

    @classmethod
    def make_point_wkt(cls, latitude: float, longitude: float) -> str:
        return f"SRID=4326;POINT({longitude} {latitude})"
