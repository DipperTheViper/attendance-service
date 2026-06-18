import logging
from celery import Task
from src.configs.celery_config import celery_app
from src.configs.runtime_config import RuntimeConfig

logger = logging.getLogger(__name__)


class SmsTask(Task):
    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"SMS task {task_id} failed: {exc}")


config = RuntimeConfig.global_config()


@celery_app.task(
    bind=True,
    base=SmsTask,
    max_retries=config.SMS_MAX_RETRIES,
    default_retry_delay=config.SMS_RETRY_DELAY_SECONDS,
    name="tasks.send_welcome_sms",
)
def send_welcome_sms(self, phone_number: str, first_name: str | None) -> None:
    try:
        name = first_name or "کاربر"
        message = f"خوش آمدید {name}! ورود شما با موفقیت ثبت شد."

        # Pseudocode
        # sms_provider.send(to=phone_number, message=message)
        logger.info(f"SMS sent to {phone_number}: {message}")

    except Exception as exc:
        raise self.retry(exc=exc, countdown=2**self.request.retries * 60)
