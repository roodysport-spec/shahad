from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .fatigue import sessions_to_dicts, compute_acwr_from_sessions, compute_readiness_score, get_chronic_weeks

router = APIRouter(prefix="/team", tags=["team"])


@router.get("/dashboard")
def get_team_dashboard(db: Session = Depends(get_db)):
    """Team overview with all players' ACWR, Readiness, and wellness metrics."""
    players = db.query(models.Player).all()
    chronic_weeks = get_chronic_weeks(db)
    result = []

    for player in players:
        ts_sessions = db.query(models.TrainingSession).filter(
            models.TrainingSession.player_id == player.id
        ).order_by(models.TrainingSession.date).all()

        fe_sessions = db.query(models.FatigueEntry).filter(
            models.FatigueEntry.player_id == player.id
        ).order_by(models.FatigueEntry.date).all()

        all_sessions = sessions_to_dicts(ts_sessions) + sessions_to_dicts(fe_sessions)
        all_sessions.sort(key=lambda x: x['date'])

        acwr_data = compute_acwr_from_sessions(all_sessions, chronic_weeks)
        readiness = compute_readiness_score(all_sessions, acwr_data.get('acwr'))

        latest = all_sessions[-1] if all_sessions else {}

        result.append({
            'player': {
                'id': player.id,
                'name': player.name,
                'name_en': player.name_en,
                'position': player.position,
                'team': player.team,
                'age': player.age,
                'jersey_number': player.jersey_number,
            },
            'acwr': acwr_data.get('acwr'),
            'acute_load': acwr_data.get('acute_load'),
            'chronic_load': acwr_data.get('chronic_load'),
            'weekly_load': acwr_data.get('weekly_load'),
            'acwr_classification': acwr_data.get('classification'),
            'readiness': readiness.get('score'),
            'readiness_level': readiness.get('level'),
            'readiness_label_ar': readiness.get('label_ar'),
            'readiness_label_en': readiness.get('label_en'),
            'sleep_quality': latest.get('sleep_quality'),
            'fatigue': latest.get('fatigue'),
            'muscle_soreness': latest.get('muscle_soreness'),
            'rpe': latest.get('rpe'),
            'resting_heart_rate': latest.get('resting_heart_rate'),
            'respiratory_rate': latest.get('respiratory_rate'),
            'session_count': len(all_sessions),
        })

    return {'players': result, 'total': len(result)}
