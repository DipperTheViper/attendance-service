import uuid

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, Synonym, mapped_column, relationship


class ReferralEntity(UpdatableDeletableEntity):
    __tablename__ = "referrals"

    referral_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("referral_uuid")

    # Foreign keys
    referee_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)
    referer_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_uuid"), nullable=False)

    # Relationships
    referee = relationship("UserEntity", foreign_keys=[referee_uuid], back_populates="referrals_received")
    referer = relationship("UserEntity", foreign_keys=[referer_uuid], back_populates="referrals_given")
