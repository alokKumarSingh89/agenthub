from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from packages.database.base import Base
from packages.database.types import TimestampMixin

if TYPE_CHECKING:
    from .credential import Credential
    from .organization import Organization
    from .role import Role


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    organization: Mapped[Organization] = relationship(
        back_populates="users",
    )

    roles: Mapped[list[Role]] = relationship(
        secondary="user_roles",
        back_populates="users",
    )

    credential: Mapped[Credential] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
