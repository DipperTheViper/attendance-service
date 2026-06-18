from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.adapters.redis.adapters import AsyncRedisAdapter
from dependency_injector import containers, providers

from src.configs.runtime_config import RuntimeConfig
from src.logics.admin.admin_logic import AdminLogic
from src.logics.auth.auth_logic import AuthLogic
from src.logics.user.user_logic import UserLogic
from src.repositories.admin.adapters.admin_postgres_adapter import AdminPostgresAdapter
from src.repositories.admin.admin_repository import AdminRepository
from src.repositories.auth.adapters.auth_redis_adapter import AuthRedisAdapter
from src.repositories.auth.auth_repository import AuthRepository
from src.repositories.user.adapters.user_postgres_adapter import UserPostgresAdapter
from src.repositories.user.user_repository import UserRepository


class ServiceContainer(containers.DeclarativeContainer):
    # region base adapters
    _config: RuntimeConfig = RuntimeConfig.global_config()
    _postgres_adapter: AsyncPostgresSQLAlchemyAdapter = providers.ThreadSafeSingleton(AsyncPostgresSQLAlchemyAdapter)
    _redis_adapter: AsyncRedisAdapter = providers.ThreadSafeSingleton(AsyncRedisAdapter)
    # endregion

    # region user
    _user_postgres_adapter = providers.ThreadSafeSingleton(
        UserPostgresAdapter,
        adapter=_postgres_adapter,
    )
    _user_repository = providers.ThreadSafeSingleton(
        UserRepository,
        postgres_adapter=_user_postgres_adapter,
    )
    user_logic = providers.ThreadSafeSingleton(UserLogic, repository=_user_repository)
    # endregion

    # region auth
    _auth_redis_adapter = providers.ThreadSafeSingleton(
        AuthRedisAdapter,
        adapter=_redis_adapter,
    )
    _auth_repository = providers.ThreadSafeSingleton(
        AuthRepository,
        redis_adapter=_auth_redis_adapter,
    )
    auth_logic = providers.ThreadSafeSingleton(
        AuthLogic,
        repository=_auth_repository,
        user_logic=user_logic,
    )
    # endregion

    # region admin
    _admin_postgres_adapter = providers.ThreadSafeSingleton(
        AdminPostgresAdapter,
        adapter=_postgres_adapter,
    )
    _admin_repository = providers.ThreadSafeSingleton(
        AdminRepository,
        postgres_adapter=_admin_postgres_adapter,
    )
    admin_logic = providers.ThreadSafeSingleton(
        AdminLogic,
        repository=_admin_repository,
    )
    # endregion
