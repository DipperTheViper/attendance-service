import logging
import uvicorn

from archipy.helpers.utils.app_utils import AppUtils

from src.configs.containers import ServiceContainer
from src.configs.dispatcher import set_dispatch_routes, set_admin_dispatch_routes
from src.configs.runtime_config import RuntimeConfig

logging.basicConfig(
    level=RuntimeConfig.global_config().ENVIRONMENT.log_level,
    handlers=[logging.StreamHandler()],
    format="{'time':'%(asctime)s', 'name': '%(name)s','level': '%(levelname)s', 'message': '%(message)s'}",
)

container: ServiceContainer = ServiceContainer()
container.wire(packages=["src.services"])

app = AppUtils.create_fastapi_app()
app.container = container
set_dispatch_routes(app)
set_admin_dispatch_routes(app)

if __name__ == "__main__":
    uvicorn.run(
        app="manage:app",
        host=RuntimeConfig.global_config().FASTAPI.SERVE_HOST,
        port=RuntimeConfig.global_config().FASTAPI.SERVE_PORT,
        reload=RuntimeConfig.global_config().FASTAPI.RELOAD,
        workers=RuntimeConfig.global_config().FASTAPI.WORKERS_COUNT,
    )
