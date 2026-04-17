from datetime import date

from sqlalchemy import ForeignKey, Date, Time, Enum, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    mobile_number: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        index=True,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="user"
    )

    created_at: Mapped[date] = mapped_column(Date, nullable=False)

    patients = relationship("Patient", back_populates="user")