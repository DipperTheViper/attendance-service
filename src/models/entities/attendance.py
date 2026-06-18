import uuid

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym
from sqlalchemy import Enum as SAEnum
from src.models.types.enums import AttendanceMethodType


class AttendanceRecordEntity(UpdatableDeletableEntity):
    __tablename__ = "attendance_records"

    attendance_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)
    pk_uuid = Synonym("attendance_uuid")
    check_in_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    check_out_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    method: Mapped[str] = mapped_column(SAEnum(AttendanceMethodType), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    user = relationship("UserEntity", back_populates="attendance_records")
