import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=list[AssetResponse])
def list_assets(
    category: str | None = Query(None),
    area: str | None = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(Asset)
    if category:
        stmt = stmt.where(Asset.category == category)
    if area:
        stmt = stmt.where(Asset.area == area)
    return db.execute(stmt).scalars().all()


@router.post("", response_model=AssetResponse, status_code=201)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    existing = db.execute(
        select(Asset).where(Asset.asset_code == payload.asset_code)
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="asset_code already exists")

    asset = Asset(**payload.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: uuid.UUID, db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")
    return asset


@router.patch("/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: uuid.UUID, payload: AssetUpdate, db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)
    return asset