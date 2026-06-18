import uuid

from typing import Optional
from archipy.models.entities import UpdatableDeletableEntity
from sqlalchemy import Column, ForeignKey, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, Synonym, mapped_column, relationship


class AppConfigEntity(UpdatableDeletableEntity):
    __tablename__ = "app_configs"

    app_config_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pk_uuid = Synonym("app_config_uuid")

    # Fields
    force_update_version: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    force_update_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    optional_update_version: Mapped[Optional[str]] = mapped_column(String, nullable=False)
    optional_update_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    update_link: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
