import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.work_order import WorkOrderType, WorkOrderStatus, WorkOrderPriority


class WorkOrderCreate(BaseModel):
    asset_id: uuid.UUID
    type: WorkOrderType
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
    description: str


class WorkOrderAssign(BaseModel):
    assigned_technician: str


class WorkOrderStatusChange(BaseModel):
    status: WorkOrderStatus


class WorkOrderComplete(BaseModel):
    completion_notes: str
    downtime_started_at: datetime | None = None
    downtime_ended_at: datetime | None = None
    downtime_cause: str | None = None


class WorkOrderResponse(BaseModel):
    id: uuid.UUID
    asset_id: uuid.UUID
    type: WorkOrderType
    status: WorkOrderStatus
    priority: WorkOrderPriority
    description: str
    assigned_technician: str | None
    completion_notes: str | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)