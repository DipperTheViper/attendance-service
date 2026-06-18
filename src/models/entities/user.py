import uuid
from datetime import date
from typing import Optional

from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, Date, Integer
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship, Synonym


class UserEntity(UpdatableDeletableEntity):
    __tablename__ = "users"

    user_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("user_uuid")

    # Basic Information
    first_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(15), nullable=False, unique=True)

    # Profile Information
    username: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    profile_picture_path: Mapped[Optional[str]] = mapped_column(VARCHAR(500), nullable=True)
    # Enums
    user_type: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="USER")
    user_status: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, default="ACTIVE")
    gender_type: Mapped[Optional[str]] = mapped_column(VARCHAR(30), nullable=True)

    created_files = relationship("FileEntity", foreign_keys="[FileEntity.created_by]")
    updated_files = relationship("FileEntity", foreign_keys="[FileEntity.updated_by]")
