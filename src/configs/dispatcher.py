from archipy.helpers.utils.base_utils import BaseUtils
from archipy.models.errors import UnauthenticatedError, UnknownError, UnavailableError, InvalidArgumentError
from fastapi import Depends, FastAPI

from src.configs.containers import ServiceContainer
from src.logics.auth.admin_authenticator_logic import AdminAuthenticator
from src.logics.auth.authenticator_logic import Authenticator
from src.services.admin.v1 import admin_service
from src.services.auth.v1 import auth_service
from src.services.file.v1 import file_service
from src.services.referral.v1 import referral_service
from src.services.user.v1 import user_service


def set_dispatch_routes(app: FastAPI) -> None:
    authenticator = Authenticator(user_logic=ServiceContainer.user_logic())

    common_private_response = BaseUtils.get_fastapi_exception_responses(
        [UnauthenticatedError, UnknownError, UnavailableError, InvalidArgumentError],
    )
    app.include_router(router=auth_service.routerV1, prefix="/api/v1/auth", responses=common_private_response)

    dependencies = [
        Depends(authenticator),
    ]

    app.include_router(
        router=admin_service.routerV1,
        prefix="/api/v1/configs",
        responses=common_private_response,
    )
    app.include_router(
        router=user_service.routerV1,
        prefix="/api/v1/users",
        dependencies=dependencies,
        responses=common_private_response,
    )

    app.include_router(
        router=referral_service.routerV1,
        prefix="/api/v1/users",
        dependencies=dependencies,
        responses=common_private_response,
    )

    app.include_router(
        router=file_service.routerV1,
        prefix="/api/v1/users",
        dependencies=dependencies,
        responses=common_private_response,
    )


def set_admin_dispatch_routes(app: FastAPI) -> None:
    admin_authenticator = AdminAuthenticator(user_logic=ServiceContainer.user_logic())
    common_private_response = BaseUtils.get_fastapi_exception_responses(
        [UnauthenticatedError, UnknownError, UnavailableError, InvalidArgumentError],
    )

    app.include_router(
        router=auth_service.AdminRouterV1,
        prefix="/api/v1/auth/admin",
        responses=common_private_response,
    )

    admin_dependencies = [
        Depends(admin_authenticator),
    ]

    app.include_router(
        router=admin_service.AdminRouterV1,
        prefix="/api/v1/admin",
        dependencies=admin_dependencies,
        responses=common_private_response,
    )
