from archipy.models.dtos.base_dtos import BaseDTO
from pydantic import StrictStr
from uuid import UUID


class CreateSessionCommandDTO(BaseDTO):
    user_uuid: UUID
    access_token: StrictStr


class DeleteSessionCommandDTO(BaseDTO):
    access_token: StrictStr


class GetSessionQueryDTO(BaseDTO):
    access_token: StrictStr


class GetSessionResponseDTO(BaseDTO):
    user_uuid: UUID
