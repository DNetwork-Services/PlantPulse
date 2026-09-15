import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class WorkOrderType(str, enum.Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    BREAKDOWN = "breakdown"


class WorkOrderStatus(str, enum.Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class WorkOrderPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="RESTRICT"), index=True
    )
    type: Mapped[WorkOrderType] = mapped_column(Enum(WorkOrderType, name="work_order_type"))
    status: Mapped[WorkOrderStatus] = mapped_column(
        Enum(WorkOrderStatus, name="work_order_status"), default=WorkOrderStatus.OPEN
    )
    priority: Mapped[WorkOrderPriority] = mapped_column(
        Enum(WorkOrderPriority, name="work_order_priority"), default=WorkOrderPriority.MEDIUM
    )
    description: Mapped[str] = mapped_column(Text)

    # Plain string for now, not a FK to a users table — Users/RBAC
    # module doesn't exist yet (next in this phase). Deliberately
    # simple so work order logic can be built and tested before auth
    # exists; will become ForeignKey("users.id") once that table lands.
    assigned_technician: Mapped[str | None] = mapped_column(String(150), nullable=True)

    completion_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    asset = relationship("Asset")
    downtime_record = relationship(
        "DowntimeRecord", back_populates="work_order", uselist=False, cascade="all, delete-orphan"
    )


class DowntimeRecord(Base):
    __tablename__ = "downtime_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("work_orders.id", ondelete="CASCADE"), unique=True, index=True
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cause: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    work_order = relationship("WorkOrder", back_populates="downtime_record")
# Allowed status transitions. Enforced in the API layer (see api/work_orders.py) —
# kept here alongside the enum so the rule lives next to the states it governs.
ALLOWED_TRANSITIONS: dict[WorkOrderStatus, set[WorkOrderStatus]] = {
    WorkOrderStatus.OPEN: {WorkOrderStatus.ASSIGNED, WorkOrderStatus.CANCELLED},
    WorkOrderStatus.ASSIGNED: {WorkOrderStatus.IN_PROGRESS, WorkOrderStatus.CANCELLED},
    WorkOrderStatus.IN_PROGRESS: {WorkOrderStatus.COMPLETED, WorkOrderStatus.CANCELLED},
    WorkOrderStatus.COMPLETED: {WorkOrderStatus.CLOSED},
    WorkOrderStatus.CLOSED: set(),
    WorkOrderStatus.CANCELLED: set(),
}
