from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum


# 🔥 ENUM for appointment lifecycle
class AppointmentStatus(str, enum.Enum):
    BOOKED = "BOOKED"
    VISITED = "VISITED"
    NO_SHOW = "NO_SHOW"
    CANCELLED = "CANCELLED"


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("slots.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # 🔥 ensures 1 slot → 1 appointment
        index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus),
        default=AppointmentStatus.BOOKED,
        nullable=False
    )

    # 🔗 Relationships
    slot = relationship("Slot", back_populates="appointment")
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
