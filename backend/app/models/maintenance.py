import enum
import uuid
from datetime import datetime, date

from sqlalchemy import String, Integer, Boolean, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class FrequencyType(str, enum.Enum):
    CALENDAR_DAYS = "calendar_days"     # e.g. every 90 days
    USAGE_CYCLES = "usage_cycles"       # e.g. every 500 operating cycles


class ScheduleStatus(str, enum.Enum):
    PENDING = "pending"
    OVERDUE = "overdue"
    COMPLETED = "completed"


class MaintenancePlan(Base):
    __tablename__ = "maintenance_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    frequency_type: Mapped[FrequencyType] = mapped_column(Enum(FrequencyType, name="frequency_type"))
    frequency_value: Mapped[int] = mapped_column(Integer)  # days, or cycles, depending on frequency_type
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    asset = relationship("Asset")
    schedules = relationship("MaintenanceSchedule", back_populates="plan", cascade="all, delete-orphan")


class MaintenanceSchedule(Base):
    __tablename__ = "maintenance_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("maintenance_plans.id", ondelete="CASCADE"), index=True
    )
    due_date: Mapped[date] = mapped_column(Date)
    status: Mapped[ScheduleStatus] = mapped_column(
        Enum(ScheduleStatus, name="schedule_status"), default=ScheduleStatus.PENDING
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    plan = relationship("MaintenancePlan", back_populates="schedules")