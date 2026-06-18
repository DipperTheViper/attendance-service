import uuid

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym
from sqlalchemy import Enum as SAEnum
from src.models.types.enums import UserType


class UserEntity(UpdatableDeletableEntity):
    __tablename__ = "users"

    user_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("user_uuid")

    username: Mapped[str] = mapped_column(VARCHAR(500), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(VARCHAR(15), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    user_type: Mapped[str] = mapped_column(SAEnum(UserType), nullable=False, default=UserType.USER)

    attendance_records = relationship("AttendanceRecordEntity", back_populates="user")
