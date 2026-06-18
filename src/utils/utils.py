from archipy.configs.config_template import FileConfig
from archipy.helpers.utils.base_utils import BaseUtils

from src.configs.runtime_config import RuntimeConfig
from src.models.types.enums import UpdateStatusType


class Utils(BaseUtils):
    @classmethod
    def create_secure_link(
        cls,
        path: str,
        minutes: int | None = None,
        file_config: FileConfig | None = None,
    ) -> str:
        secured_path = BaseUtils.create_secure_link(
            path=path,
            minutes=minutes,
            file_config=file_config,
        )

        return RuntimeConfig.global_config().SECURE_BASE_URL + secured_path

    @classmethod
    def generate_referral_code(cls, length=7):
        import time
        import random

        if length <= 0:
            raise ValueError("Length must be positive")
        timestamp = int(time.time() * 1000000) % (10 ** (length - 2))
        random_component = random.randint(10, 99)
        unique_number = int(str(timestamp) + str(random_component))
        return str(unique_number).zfill(length)

    @classmethod
    def parse_version(cls, version: str) -> tuple[int, int, int]:
        """
        Parse semantic version string into tuple of integers (major, minor, patch).

        Args:
            version: Version string in format "major.minor.patch"

        Returns:
            Tuple of (major, minor, patch) as integers

        Raises:
            ValueError: If version format is invalid
        """
        try:
            parts = version.strip().split(".")
            if len(parts) != 3:
                raise ValueError(f"Invalid version format: {version}. Expected 'major.minor.patch'")

            major, minor, patch = map(int, parts)

            if major < 0 or minor < 0 or patch < 0:
                raise ValueError(f"Version numbers cannot be negative: {version}")

            return (major, minor, patch)

        except ValueError as e:
            if "invalid literal for int()" in str(e):
                raise ValueError(f"Invalid version format: {version}. All parts must be integers")
            raise

    @classmethod
    def get_update_status(
        cls,
        client_version: str,
        force_update_version: str,
        optional_update_version: str,
    ) -> UpdateStatusType:
        """
        Determine update status by comparing client version with latest available version.

        Update logic:
        - LATEST_UPDATE: Client version equals or is newer than latest version
        - OPTIONAL_UPDATE: Latest version has higher minor or patch version (same major)
        - FORCE_UPDATE: Latest version has higher major version

        Args:
            client_version: Current client version (e.g., "1.2.3")
            latest_version: Latest available version from database (e.g., "1.2.4")

        Returns:
            UpdateStatus enum indicating the required update action


        """
        client_tuple = cls.parse_version(client_version)
        force_tuple = cls.parse_version(force_update_version)
        optional_tuple = cls.parse_version(optional_update_version)

        # Client version is below force update threshold - must update
        if client_tuple < force_tuple:
            return UpdateStatusType.FORCE_UPDATE

        # Client version is below optional update threshold - should update
        if client_tuple < optional_tuple:
            return UpdateStatusType.OPTIONAL_UPDATE

        # Client version is up to date or newer than optional threshold
        return UpdateStatusType.LATEST_UPDATE

    @classmethod
    def hash_pin_code(cls, pin: str) -> str:
        import hashlib

        return hashlib.sha256(pin.encode()).hexdigest()
