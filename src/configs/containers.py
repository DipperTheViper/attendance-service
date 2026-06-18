from archipy.adapters.postgres.sqlalchemy.adapters import AsyncPostgresSQLAlchemyAdapter
from archipy.adapters.redis.adapters import AsyncRedisAdapter
from dependency_injector import containers, providers

from src.configs.runtime_config import RuntimeConfig
from src.logics.attendance.attendance_logic import AttendanceLogic
from src.logics.auth.auth_logic import AuthLogic
from src.logics.notification.notification_logic import NotificationLogic
from src.logics.user.user_logic import UserLogic
from src.repositories.attendance.adapters.attendance_postgres_adapter import AttendancePostgresAdapter
from src.repositories.attendance.attendance_repository import AttendanceRepository
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
    user_logic = providers.ThreadSafeSingleton(
        UserLogic,
        repository=_user_repository,
    )
    # endregion

    # region notification
    notification_logic = providers.ThreadSafeSingleton(
        NotificationLogic,
        user_logic=user_logic,
    )
    # endregion

    # region attendance
    _attendance_postgres_adapter = providers.ThreadSafeSingleton(
        AttendancePostgresAdapter,
        adapter=_postgres_adapter,
    )
    _attendance_repository = providers.ThreadSafeSingleton(
        AttendanceRepository,
        postgres_adapter=_attendance_postgres_adapter,
    )
    attendance_logic = providers.ThreadSafeSingleton(
        AttendanceLogic,
        repository=_attendance_repository,
        notification_logic=notification_logic,
    )
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
