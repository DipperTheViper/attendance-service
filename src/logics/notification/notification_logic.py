from uuid import UUID

from src.logics.user.user_logic import UserLogic
from src.models.dtos.user.domain.v1.user_domain_interface_dtos import GetUserInputDTOV1
from src.tasks.sms_task import send_welcome_sms


class NotificationLogic:
    def __init__(self, user_logic: UserLogic) -> None:
        self._user_logic = user_logic

    async def send_welcome_sms(self, user_uuid: UUID) -> None:
        user = await self._user_logic.get_user(input_dto=GetUserInputDTOV1(user_uuid=user_uuid))
        send_welcome_sms.delay(phone_number=user.phone_number, first_name=user.first_name)
