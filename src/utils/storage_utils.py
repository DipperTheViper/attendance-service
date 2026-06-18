from pathlib import Path

from archipy.helpers.utils.base_utils import BaseUtils

from src.configs.runtime_config import RuntimeConfig


class StorageUtils(BaseUtils):
    @staticmethod
    def get_dir_path(path: str | None = None, is_secure: bool | None = True, config: RuntimeConfig = None) -> Path:
        if not path:
            if is_secure:
                return Path(config.SECURE_BASE_DIR)
            else:
                return Path(config.PUBLIC_BASE_DIR)

        if path[0] == "/":
            return (
                Path(config.SECURE_BASE_DIR).joinpath(path[1:])
                if is_secure
                else Path(config.PUBLIC_BASE_DIR).joinpath(path[1:])
            )
        if is_secure:
            return Path(config.SECURE_BASE_DIR).joinpath(path)
        else:
            return Path(config.PUBLIC_BASE_DIR).joinpath(path)

    @staticmethod
    def get_file_path(path: str, name: str, is_secure: bool | None = True, config: RuntimeConfig = None) -> Path:
        if config is None:
            raise ValueError("config is required")
        dir_path = StorageUtils.get_dir_path(path, is_secure=is_secure, config=config)
        return dir_path.joinpath(name)

    @staticmethod
    def get_storage_path(path: str, name: str, is_secure: bool | None = True) -> Path:
        if is_secure:
            concatenated_path = f"/media{path}/{name}"
        else:
            concatenated_path = f"/media/static{path}/{name}"
        output_path = Path(concatenated_path)
        return output_path
