from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
import datetime

router = APIRouter(prefix="/settings", tags=["settings"])

DEFAULT_SETTINGS = [
    {'key': 'chronic_weeks', 'value': '4', 'description': 'Number of weeks for chronic load calculation (default 4)'},
    {'key': 'acwr_very_low_threshold', 'value': '0.50', 'description': 'ACWR threshold: below this = Very Low'},
    {'key': 'acwr_low_threshold', 'value': '0.80', 'description': 'ACWR threshold: below this = Below Normal (Low)'},
    {'key': 'acwr_normal_max', 'value': '1.30', 'description': 'ACWR Reference Zone upper limit'},
    {'key': 'acwr_slightly_high', 'value': '1.50', 'description': 'ACWR threshold: below this = Slightly Elevated'},
    {'key': 'acwr_high', 'value': '2.00', 'description': 'ACWR Extreme threshold: >= this = Extreme Alert'},
    {'key': 'readiness_good', 'value': '85', 'description': 'Readiness score threshold for Good (>=)'},
    {'key': 'readiness_moderate', 'value': '70', 'description': 'Readiness score threshold for Moderate (>=)'},
    {'key': 'readiness_needs_monitoring', 'value': '50', 'description': 'Readiness score threshold for Needs Monitoring (>=)'},
    {'key': 'sport', 'value': 'volleyball', 'description': 'Sport type (volleyball)'},
    {'key': 'team_name', 'value': 'SHM LOAD', 'description': 'Platform name'},
]


def ensure_defaults(db: Session):
    for s in DEFAULT_SETTINGS:
        existing = db.query(models.SystemSettings).filter(models.SystemSettings.key == s['key']).first()
        if not existing:
            db.add(models.SystemSettings(**s))
    db.commit()


@router.get("/", response_model=List[schemas.SystemSetting])
def get_settings(db: Session = Depends(get_db)):
    ensure_defaults(db)
    return db.query(models.SystemSettings).all()


@router.put("/{key}")
def update_setting(key: str, value: str, db: Session = Depends(get_db)):
    setting = db.query(models.SystemSettings).filter(models.SystemSettings.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting.value = value
    setting.updated_at = datetime.datetime.utcnow()
    db.commit()
    return {"key": key, "value": value, "message": "Updated"}


@router.post("/reset")
def reset_settings(db: Session = Depends(get_db)):
    db.query(models.SystemSettings).delete()
    db.commit()
    ensure_defaults(db)
    return {"message": "Settings reset to defaults"}
