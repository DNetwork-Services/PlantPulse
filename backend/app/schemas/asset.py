import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.asset import AssetStatus


class AssetBase(BaseModel):
    asset_code: str
    name: str
    category: str
    area: str
    location_detail: str | None = None
    vendor: str | None = None
    is_critical: bool = False


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    area: str | None = None
    location_detail: str | None = None
    vendor: str | None = None
    status: AssetStatus | None = None
    is_critical: bool | None = None


class AssetResponse(AssetBase):
    id: uuid.UUID
    status: AssetStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)