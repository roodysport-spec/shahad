from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..ml.predictor import predict_injury_risk

class PredictRequest(BaseModel):
    player_id: int
    body_part: str
    prev_injury: bool = False
    pain_level: int = 0
    field_tests: Optional[Dict[str, Any]] = None

from .fatigue import sessions_to_dicts, compute_acwr_from_sessions, get_chronic_weeks

router = APIRouter(prefix="/injury", tags=["injury"])

@router.post("/predict")
def predict_injury(req: PredictRequest, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == req.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    chronic_weeks = get_chronic_weeks(db)

    # Fetch sessions from both TrainingSession and FatigueEntry
    ts_sessions = db.query(models.TrainingSession).filter(
        models.TrainingSession.player_id == req.player_id
    ).order_by(models.TrainingSession.date).all()

    fe_sessions = db.query(models.FatigueEntry).filter(
        models.FatigueEntry.player_id == req.player_id
    ).order_by(models.FatigueEntry.date).all()

    all_sessions = sessions_to_dicts(ts_sessions) + sessions_to_dicts(fe_sessions)
    all_sessions.sort(key=lambda x: x['date'])

    acwr_data = compute_acwr_from_sessions(all_sessions, chronic_weeks)
    acwr_val = acwr_data.get('acwr') if acwr_data.get('acwr') is not None else 1.0

    recent_dicts = all_sessions[-14:] if all_sessions else []

    player_data = {
        'age': player.age,
        'weight': player.weight,
        'height': player.height,
        'position': player.position,
        'dominant_hand': player.dominant_hand,
        'acwr': acwr_val,
    }

    result = predict_injury_risk(
        player_data=player_data,
        recent_entries=recent_dicts,
        body_part=req.body_part,
        prev_injury=req.prev_injury,
        pain_level=req.pain_level,
        field_tests=req.field_tests or {}
    )

    # Provide both keys for compatibility
    result['factors'] = result.get('risk_factors', [])
    result['acwr'] = acwr_val
    result['acwr_classification'] = acwr_data.get('classification')
    return result


@router.post("/records", response_model=schemas.InjuryRecord)
def create_injury_record(record: schemas.InjuryRecordCreate, db: Session = Depends(get_db)):
    db_record = models.InjuryRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.get("/records/{player_id}", response_model=List[schemas.InjuryRecord])
def read_injury_records(player_id: int, db: Session = Depends(get_db)):
    return db.query(models.InjuryRecord).filter(
        models.InjuryRecord.player_id == player_id
    ).order_by(models.InjuryRecord.date.desc()).all()


@router.get("/records", response_model=List[schemas.InjuryRecord])
def read_all_injury_records(db: Session = Depends(get_db)):
    return db.query(models.InjuryRecord).order_by(models.InjuryRecord.date.desc()).all()


@router.delete("/records/{record_id}")
def delete_injury_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.InjuryRecord).filter(models.InjuryRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return {"message": "Deleted"}
