from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from .fatigue import compute_srpe

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/", response_model=schemas.TrainingSession)
def create_session(session: schemas.TrainingSessionCreate, db: Session = Depends(get_db)):
    """Create a new training session. sRPE is auto-calculated if not provided."""
    data = session.model_dump()
    if not data.get('srpe'):
        data['srpe'] = compute_srpe(data['training_duration'], data['rpe'])
    db_session = models.TrainingSession(**data)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.get("/{player_id}", response_model=List[schemas.TrainingSession])
def get_sessions(player_id: int, limit: int = 60, db: Session = Depends(get_db)):
    return db.query(models.TrainingSession).filter(
        models.TrainingSession.player_id == player_id
    ).order_by(models.TrainingSession.date.desc()).limit(limit).all()


@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    s = db.query(models.TrainingSession).filter(models.TrainingSession.id == session_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(s)
    db.commit()
    return {"message": "Deleted"}
