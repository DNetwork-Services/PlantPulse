import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class AssetStatus(str, enum.Enum):
    PLANNED = "planned"
    PROCURED = "procured"
    RECEIVED = "received"
    INSTALLED = "installed"
    COMMISSIONED = "commissioned"
    OPERATIONAL = "operational"
    UNDER_MAINTENANCE = "under_maintenance"
    RETIRED = "retired"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100), index=True)
    area: Mapped[str] = mapped_column(String(100), index=True)
    location_detail: Mapped[str | None] = mapped_column(String(200), nullable=True)
    vendor: Mapped[str | None] = mapped_column(String(150), nullable=True)
    status: Mapped[AssetStatus] = mapped_column(
        Enum(AssetStatus, name="asset_status"), default=AssetStatus.PLANNED
    )
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )