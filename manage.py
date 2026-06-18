import logging
import time
import uvicorn

from archipy.helpers.utils.app_utils import AppUtils
from fastapi import FastAPI, APIRouter
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.configs.containers import ServiceContainer
from src.configs.dispatcher import set_dispatch_routes, set_admin_dispatch_routes
from src.configs.runtime_config import RuntimeConfig

logging.basicConfig(
    level=RuntimeConfig.global_config().ENVIRONMENT.log_level,
    handlers=[logging.FileHandler("../siteLogs.log"), logging.StreamHandler()],
    format="{'time':'%(asctime)s', 'name': '%(name)s','level': '%(levelname)s', 'message': '%(message)s'}",
)


container: ServiceContainer = ServiceContainer()
container.wire(packages=["src.services"])

app: FastAPI = AppUtils.create_fastapi_app()
app.container = container
set_dispatch_routes(app)
set_admin_dispatch_routes(app)


if __name__ == "__main__":
    uvicorn.run(
        app="manage:app",
        access_log=RuntimeConfig.global_config().FASTAPI.ACCESS_LOG,
        backlog=RuntimeConfig.global_config().FASTAPI.BACKLOG,
        date_header=RuntimeConfig.global_config().FASTAPI.DATE_HEADER,
        forwarded_allow_ips=RuntimeConfig.global_config().FASTAPI.FORWARDED_ALLOW_IPS,
        host=RuntimeConfig.global_config().FASTAPI.SERVE_HOST,
        limit_concurrency=RuntimeConfig.global_config().FASTAPI.LIMIT_CONCURRENCY,
        limit_max_requests=RuntimeConfig.global_config().FASTAPI.LIMIT_MAX_REQUESTS,
        port=RuntimeConfig.global_config().FASTAPI.SERVE_PORT,
        proxy_headers=RuntimeConfig.global_config().FASTAPI.PROXY_HEADERS,
        reload=RuntimeConfig.global_config().FASTAPI.RELOAD,
        server_header=RuntimeConfig.global_config().FASTAPI.SERVER_HEADER,
        timeout_graceful_shutdown=RuntimeConfig.global_config().FASTAPI.TIMEOUT_GRACEFUL_SHUTDOWN,
        timeout_keep_alive=RuntimeConfig.global_config().FASTAPI.TIMEOUT_KEEP_ALIVE,
        workers=RuntimeConfig.global_config().FASTAPI.WORKERS_COUNT,
        ws_max_size=RuntimeConfig.global_config().FASTAPI.WS_MAX_SIZE,
        ws_per_message_deflate=RuntimeConfig.global_config().FASTAPI.WS_PER_MESSAGE_DEFLATE,
        ws_ping_interval=RuntimeConfig.global_config().FASTAPI.WS_PING_INTERVAL,
        ws_ping_timeout=RuntimeConfig.global_config().FASTAPI.WS_PING_TIMEOUT,
    )
