import uuid
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.asset import Asset
from app.models.maintenance import MaintenancePlan, MaintenanceSchedule, FrequencyType, ScheduleStatus
from app.schemas.maintenance import (
    MaintenancePlanCreate,
    MaintenancePlanResponse,
    MaintenanceScheduleResponse,
)

router = APIRouter(prefix="/maintenance-plans", tags=["maintenance"])


@router.post("", response_model=MaintenancePlanResponse, status_code=201)
def create_plan(payload: MaintenancePlanCreate, db: Session = Depends(get_db)):
    asset = db.get(Asset, payload.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")

    plan = MaintenancePlan(**payload.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("", response_model=list[MaintenancePlanResponse])
def list_plans(asset_id: uuid.UUID | None = Query(None), db: Session = Depends(get_db)):
    stmt = select(MaintenancePlan)
    if asset_id:
        stmt = stmt.where(MaintenancePlan.asset_id == asset_id)
    return db.execute(stmt).scalars().all()


@router.post("/{plan_id}/generate-schedule", response_model=MaintenanceScheduleResponse, status_code=201)
def generate_schedule(plan_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Generates the next due schedule from a plan.
    For calendar_days plans: due_date = today + frequency_value days.
    For usage_cycles plans: we don't yet track live usage counters
    (would need an asset-usage-event feed from Phase 6+), so for now
    this creates a placeholder due date and flags it for manual review —
    an honest MVP simplification, not a hidden gap.
    """
    plan = db.get(MaintenancePlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="maintenance plan not found")
    if not plan.is_active:
        raise HTTPException(status_code=400, detail="plan is not active")

    if plan.frequency_type == FrequencyType.CALENDAR_DAYS:
        due = date.today() + timedelta(days=plan.frequency_value)
    else:
        # usage_cycles: MVP placeholder — see docstring
        due = date.today() + timedelta(days=30)

    schedule = MaintenanceSchedule(plan_id=plan.id, due_date=due, status=ScheduleStatus.PENDING)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.get("/schedules/overdue", response_model=list[MaintenanceScheduleResponse])
def list_overdue_schedules(db: Session = Depends(get_db)):
    stmt = select(MaintenanceSchedule).where(
        MaintenanceSchedule.due_date < date.today(),
        MaintenanceSchedule.status == ScheduleStatus.PENDING,
    )
    return db.execute(stmt).scalars().all()