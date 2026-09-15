import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.maintenance import FrequencyType, ScheduleStatus


class MaintenancePlanCreate(BaseModel):
    asset_id: uuid.UUID
    title: str
    frequency_type: FrequencyType
    frequency_value: int


class MaintenancePlanResponse(MaintenancePlanCreate):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MaintenanceScheduleResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    due_date: date
    status: ScheduleStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)