import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.asset import Asset
from app.models.work_order import (
    WorkOrder,
    DowntimeRecord,
    WorkOrderType,
    WorkOrderStatus,
    ALLOWED_TRANSITIONS,
)
from app.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderAssign,
    WorkOrderStatusChange,
    WorkOrderComplete,
    WorkOrderResponse,
)

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.post("", response_model=WorkOrderResponse, status_code=201)
def create_work_order(payload: WorkOrderCreate, db: Session = Depends(get_db)):
    asset = db.get(Asset, payload.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")

    wo = WorkOrder(**payload.model_dump())
    db.add(wo)
    db.commit()
    db.refresh(wo)
    return wo


@router.get("", response_model=list[WorkOrderResponse])
def list_work_orders(
    status: WorkOrderStatus | None = Query(None),
    asset_id: uuid.UUID | None = Query(None),
    assigned_technician: str | None = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(WorkOrder)
    if status:
        stmt = stmt.where(WorkOrder.status == status)
    if asset_id:
        stmt = stmt.where(WorkOrder.asset_id == asset_id)
    if assigned_technician:
        stmt = stmt.where(WorkOrder.assigned_technician == assigned_technician)
    return db.execute(stmt).scalars().all()


@router.get("/{wo_id}", response_model=WorkOrderResponse)
def get_work_order(wo_id: uuid.UUID, db: Session = Depends(get_db)):
    wo = db.get(WorkOrder, wo_id)
    if not wo:
        raise HTTPException(status_code=404, detail="work order not found")
    return wo


@router.post("/{wo_id}/assign", response_model=WorkOrderResponse)
def assign_work_order(wo_id: uuid.UUID, payload: WorkOrderAssign, db: Session = Depends(get_db)):
    wo = db.get(WorkOrder, wo_id)
    if not wo:
        raise HTTPException(status_code=404, detail="work order not found")
    if wo.status != WorkOrderStatus.OPEN:
        raise HTTPException(status_code=400, detail=f"cannot assign a work order in status '{wo.status}'")

    wo.assigned_technician = payload.assigned_technician
    wo.status = WorkOrderStatus.ASSIGNED
    db.commit()
    db.refresh(wo)
    return wo


@router.post("/{wo_id}/status", response_model=WorkOrderResponse)
def change_status(wo_id: uuid.UUID, payload: WorkOrderStatusChange, db: Session = Depends(get_db)):
    """
    Generic status transition — enforces ALLOWED_TRANSITIONS.
    Used for the simple moves (e.g. Assigned -> In Progress, or -> Cancelled).
    Completing a work order uses the dedicated /complete endpoint instead,
    since completion requires extra data (notes, downtime).
    """
    wo = db.get(WorkOrder, wo_id)
    if not wo:
        raise HTTPException(status_code=404, detail="work order not found")

    if payload.status == WorkOrderStatus.COMPLETED:
        raise HTTPException(
            status_code=400, detail="use POST /work-orders/{id}/complete to complete a work order"
        )

    allowed = ALLOWED_TRANSITIONS.get(wo.status, set())
    if payload.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"cannot transition from '{wo.status}' to '{payload.status}'",
        )

    wo.status = payload.status
    db.commit()
    db.refresh(wo)
    return wo


@router.post("/{wo_id}/complete", response_model=WorkOrderResponse)
def complete_work_order(wo_id: uuid.UUID, payload: WorkOrderComplete, db: Session = Depends(get_db)):
    wo = db.get(WorkOrder, wo_id)
    if not wo:
        raise HTTPException(status_code=404, detail="work order not found")

    allowed = ALLOWED_TRANSITIONS.get(wo.status, set())
    if WorkOrderStatus.COMPLETED not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"cannot complete a work order in status '{wo.status}'",
        )

    wo.status = WorkOrderStatus.COMPLETED
    wo.completion_notes = payload.completion_notes
    wo.completed_at = datetime.now(timezone.utc)

    # WO-06: breakdown-type work orders automatically get a downtime record
    if wo.type == WorkOrderType.BREAKDOWN:
        if not payload.downtime_started_at:
            raise HTTPException(
                status_code=400, detail="downtime_started_at is required when completing a breakdown work order"
            )
        downtime = DowntimeRecord(
            work_order_id=wo.id,
            started_at=payload.downtime_started_at,
            ended_at=payload.downtime_ended_at,
            cause=payload.downtime_cause,
        )
        db.add(downtime)

    db.commit()
    db.refresh(wo)
    return wo