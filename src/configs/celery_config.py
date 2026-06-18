from celery import Celery
from src.configs.runtime_config import RuntimeConfig

config = RuntimeConfig.global_config()

celery_app = Celery(
    "attendance",
    broker=f"redis://{config.REDIS.MASTER_HOST}:{config.REDIS.PORT}/0",
    backend=f"redis://{config.REDIS.MASTER_HOST}:{config.REDIS.PORT}/1",
    include=["src.tasks.sms_task"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tehran",
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
