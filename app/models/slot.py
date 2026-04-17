from sqlalchemy import ForeignKey, Date, Time, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum
from datetime import date, time


# 🔥 ENUM for slot state
class SlotStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    BOOKED = "BOOKED"
    INACTIVE = "INACTIVE"


class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    slot_date: Mapped[date] = mapped_column(Date, nullable=False)

    start_time: Mapped[time] = mapped_column(Time, nullable=False)

    status: Mapped[SlotStatus] = mapped_column(
        Enum(SlotStatus),
        default=SlotStatus.AVAILABLE,
        nullable=False
    )

    # 🔗 Relationship
    doctor = relationship("Doctor", back_populates="slots")
    appointment = relationship("Appointment", back_populates="slot", uselist=False)
