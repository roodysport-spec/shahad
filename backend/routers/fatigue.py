from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
import datetime
from collections import defaultdict

router = APIRouter(prefix="/fatigue", tags=["fatigue"])


def get_chronic_weeks(db: Session) -> int:
    """Get the number of chronic weeks from settings (default 4)"""
    setting = db.query(models.SystemSettings).filter(
        models.SystemSettings.key == 'chronic_weeks'
    ).first()
    if setting:
        try:
            return max(1, int(setting.value))
        except Exception:
            pass
    return 4


def compute_srpe(duration: int, rpe: int) -> float:
    """sRPE = duration (minutes) × RPE"""
    return float(duration * rpe)


def classify_acwr(acwr: float) -> dict:
    """
    Classify ACWR according to the 6-level system.

    IMPORTANT: ACWR is a workload monitoring ratio, NOT an injury prediction tool.
    Example: ACWR = 0.57 => 'منخفض / أقل من المعتاد' (NOT high risk)

    Classification:
    < 0.50     => Very Low      (Monitor)
    0.50-0.79  => Below Normal  (Follow-up)
    0.80-1.30  => Reference Zone (Normal)  <-- optimal
    1.31-1.49  => Slightly Elevated (Attention)
    1.50-1.99  => High (Training Intervention)
    >= 2.00    => Extreme (Alert)
    """
    if acwr < 0.50:
        return {
            'level': 'very_low',
            'label_ar': 'منخفض جداً',
            'label_en': 'Very Low',
            'status_ar': 'مراقبة',
            'status_en': 'Monitor',
            'color': 'blue'
        }
    elif acwr <= 0.79:
        return {
            'level': 'low',
            'label_ar': 'منخفض / أقل من المعتاد',
            'label_en': 'Below Normal',
            'status_ar': 'متابعة',
            'status_en': 'Follow-up',
            'color': 'cyan'
        }
    elif acwr <= 1.30:
        return {
            'level': 'normal',
            'label_ar': 'ضمن النطاق المرجعي',
            'label_en': 'Reference Zone',
            'status_ar': 'طبيعي',
            'status_en': 'Normal',
            'color': 'green'
        }
    elif acwr <= 1.49:
        return {
            'level': 'slightly_high',
            'label_ar': 'مرتفع نسبياً',
            'label_en': 'Slightly Elevated',
            'status_ar': 'انتباه',
            'status_en': 'Attention',
            'color': 'yellow'
        }
    elif acwr <= 1.99:
        return {
            'level': 'high',
            'label_ar': 'ارتفاع كبير',
            'label_en': 'High',
            'status_ar': 'تدخل تدريبي',
            'status_en': 'Training Intervention',
            'color': 'orange'
        }
    else:
        return {
            'level': 'extreme',
            'label_ar': 'ارتفاع حاد جداً',
            'label_en': 'Extreme',
            'status_ar': 'إنذار',
            'status_en': 'Alert',
            'color': 'red'
        }


def compute_acwr_from_sessions(sessions: list, chronic_weeks: int = 4) -> dict:
    """
    Compute ACWR from a list of session dicts with 'date' and 'srpe'.

    Formula:
    - Acute Load = SUM of sRPE for last 7 days
    - Chronic Load = AVERAGE of weekly sums over 'chronic_weeks' weeks (before the acute window)
    - ACWR = Acute / Chronic

    Test: Acute=5625, Chronic=9843.75 => ACWR=0.57 => 'منخفض / أقل من المعتاد'
    """
    if not sessions:
        return {
            'acute_load': 0, 'chronic_load': 0, 'acwr': None,
            'classification': {'level': 'no_data', 'label_ar': 'لا توجد بيانات', 'label_en': 'No Data',
                               'status_ar': 'غير محدد', 'status_en': 'Undefined', 'color': 'gray'},
            'weekly_load': 0, 'monotony': None, 'strain': None, 'load_change_pct': None
        }

    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    # Group sessions by date
    load_by_date: dict = defaultdict(float)
    for s in sessions:
        load_by_date[s['date']] += s['srpe']

    # Acute Load = sum of sRPE over last 7 days (strictly last 7 days)
    acute_load = sum(
        v for k, v in load_by_date.items()
        if datetime.date.fromisoformat(k) > seven_days_ago
    )

    # Chronic Load = average of weekly sums for chronic_weeks weeks
    # Week 1: days -7 to -14 before today, Week 2: -14 to -21, etc.
    weekly_sums = []
    for w in range(chronic_weeks):
        week_end = today - datetime.timedelta(days=7 * (w + 1))
        week_start = today - datetime.timedelta(days=7 * (w + 2))
        week_sum = sum(
            v for k, v in load_by_date.items()
            if week_start < datetime.date.fromisoformat(k) <= week_end
        )
        weekly_sums.append(week_sum)

    chronic_load = sum(weekly_sums) / len(weekly_sums) if weekly_sums else 0

    if chronic_load == 0:
        acwr_value = None
        classification = {
            'level': 'no_chronic', 'label_ar': 'لا توجد بيانات مزمنة كافية',
            'label_en': 'Insufficient chronic data', 'status_ar': 'غير محدد', 'status_en': 'Undefined', 'color': 'gray'
        }
    else:
        acwr_value = round(acute_load / chronic_load, 2)
        classification = classify_acwr(acwr_value)

    # Weekly load (this week)
    weekly_load = acute_load

    # Monotony = mean_daily_load / std_daily_load (for last 7 days)
    last_7_loads = [
        load_by_date.get((today - datetime.timedelta(days=i)).isoformat(), 0)
        for i in range(7)
    ]
    mean_load = sum(last_7_loads) / 7
    variance = sum((x - mean_load) ** 2 for x in last_7_loads) / 7
    std_load = variance ** 0.5
    monotony = round(mean_load / std_load, 2) if std_load > 0 else None
    strain = round(weekly_load * monotony, 2) if monotony is not None else None

    # Load change % vs previous week
    prev_week_load = weekly_sums[0] if weekly_sums else 0
    if prev_week_load > 0:
        load_change_pct = round(((weekly_load - prev_week_load) / prev_week_load) * 100, 1)
    else:
        load_change_pct = None

    return {
        'acute_load': round(acute_load, 2),
        'chronic_load': round(chronic_load, 2),
        'acwr': acwr_value,
        'classification': classification,
        'weekly_load': round(weekly_load, 2),
        'monotony': monotony,
        'strain': strain,
        'load_change_pct': load_change_pct,
        'weekly_sums': weekly_sums,
    }


def compute_readiness_score(sessions: list, acwr: Optional[float]) -> dict:
    """
    Athlete Readiness Score (0-100).
    Weights: sleep 20%, fatigue 20%, muscle_soreness 15%, stress 10%, rpe 15%, acwr 20%

    NOTE: Operational indicator only, not a medical diagnosis tool.
    """
    if not sessions:
        return {
            'score': None, 'level': 'no_data',
            'label_ar': 'لا توجد بيانات', 'label_en': 'No Data',
            'color': 'gray', 'components': {}
        }

    # Use the most recent session for wellness indicators
    recent = sessions[-1] if sessions else None
    if not recent:
        return {
            'score': None, 'level': 'no_data',
            'label_ar': 'لا توجد بيانات', 'label_en': 'No Data',
            'color': 'gray', 'components': {}
        }

    sleep_q = recent.get('sleep_quality') or 7    # 1-10, higher is better
    fatigue = recent.get('fatigue') or 5           # 1-10, higher = more fatigued (inverted)
    soreness = recent.get('muscle_soreness') or 5  # 1-10, higher = more sore (inverted)
    stress = recent.get('stress_level') or 5       # 1-10, higher = more stress (inverted)
    rpe_val = recent.get('rpe') or 5              # 1-10, higher = more effort (inverted)

    # Convert to 0-100 scale (higher score = BETTER readiness)
    sleep_score = (sleep_q / 10) * 100
    fatigue_score = ((10 - fatigue) / 9) * 100
    soreness_score = ((10 - soreness) / 9) * 100
    stress_score = ((10 - stress) / 9) * 100
    rpe_score = ((10 - rpe_val) / 9) * 100

    # ACWR contribution to readiness
    if acwr is None:
        acwr_score = 50.0
    elif 0.80 <= acwr <= 1.30:
        acwr_score = 100.0
    elif 0.50 <= acwr < 0.80 or 1.30 < acwr <= 1.49:
        acwr_score = 65.0
    elif acwr < 0.50 or 1.50 <= acwr <= 1.99:
        acwr_score = 30.0
    else:  # >= 2.00
        acwr_score = 0.0

    # Weighted readiness score
    score = (
        sleep_score * 0.20 +
        fatigue_score * 0.20 +
        soreness_score * 0.15 +
        stress_score * 0.10 +
        rpe_score * 0.15 +
        acwr_score * 0.20
    )
    score = round(min(100, max(0, score)), 1)

    if score >= 85:
        level, label_ar, label_en, color = 'good', 'جاهزية جيدة', 'Good Readiness', 'green'
    elif score >= 70:
        level, label_ar, label_en, color = 'moderate', 'جاهزية متوسطة', 'Moderate Readiness', 'yellow'
    elif score >= 50:
        level, label_ar, label_en, color = 'low', 'تحتاج مراقبة', 'Needs Monitoring', 'orange'
    else:
        level, label_ar, label_en, color = 'poor', 'تحتاج تقييم', 'Needs Assessment', 'red'

    return {
        'score': score,
        'level': level,
        'label_ar': label_ar,
        'label_en': label_en,
        'color': color,
        'components': {
            'sleep': round(sleep_score, 1),
            'fatigue': round(fatigue_score, 1),
            'soreness': round(soreness_score, 1),
            'stress': round(stress_score, 1),
            'rpe': round(rpe_score, 1),
            'acwr': round(acwr_score, 1),
        }
    }


def generate_alerts(sessions: list, acwr_data: dict, readiness: dict) -> list:
    """
    Generate monitoring alerts. Operational use only, not medical diagnoses.
    Uses descriptive language per scientific best practices.
    """
    alerts = []
    acwr = acwr_data.get('acwr')
    load_change = acwr_data.get('load_change_pct')

    if not sessions:
        return alerts

    recent = sessions[-1] if sessions else {}

    # ACWR alerts
    if acwr is not None:
        if acwr < 0.50:
            alerts.append({
                'type': 'load_low',
                'severity': 'info',
                'ar': 'الحمل الحاد أقل بشكل واضح من الحمل المزمن.',
                'en': 'Acute load is notably lower than chronic load.'
            })
        elif 1.31 <= acwr < 1.50:
            alerts.append({
                'type': 'load_elevated',
                'severity': 'warning',
                'ar': 'حدث ارتفاع ملحوظ في الحمل التدريبي مقارنة بالأسبوع السابق.',
                'en': 'Notable increase in training load compared to previous week.'
            })
        elif acwr >= 1.50:
            alerts.append({
                'type': 'load_high',
                'severity': 'danger',
                'ar': 'ارتفاع كبير في الحمل التدريبي. تحتاج حالة اللاعب إلى مراقبة إضافية.',
                'en': 'Significant training load increase. Player\'s condition needs additional monitoring.'
            })

    # Load change spike
    if load_change is not None and load_change > 30:
        alerts.append({
            'type': 'load_spike',
            'severity': 'warning',
            'ar': f'ارتفع الحمل التدريبي بنسبة {load_change}% مقارنة بالأسبوع السابق.',
            'en': f'Training load increased by {load_change}% compared to previous week.'
        })

    # Sleep alert
    sleep_q = recent.get('sleep_quality')
    if sleep_q and sleep_q <= 5:
        alerts.append({
            'type': 'sleep_low',
            'severity': 'warning',
            'ar': 'اللاعب سجّل انخفاضاً في جودة النوم.',
            'en': 'Player recorded low sleep quality.'
        })

    # Fatigue alert
    fatigue_val = recent.get('fatigue')
    if fatigue_val and fatigue_val >= 7:
        alerts.append({
            'type': 'fatigue_high',
            'severity': 'warning',
            'ar': 'مستوى تعب مرتفع مسجّل من اللاعب.',
            'en': 'High fatigue level reported by player.'
        })

    # Combined: high load + high soreness
    soreness = recent.get('muscle_soreness')
    if acwr and acwr >= 1.31 and soreness and soreness >= 7:
        alerts.append({
            'type': 'combined',
            'severity': 'danger',
            'ar': 'هناك ارتفاع في الحمل مع وجود ألم عضلي مرتفع. تحتاج حالة اللاعب إلى مراقبة إضافية.',
            'en': 'High load combined with elevated muscle soreness. Player\'s condition needs additional monitoring.'
        })

    # Readiness drop
    readiness_score = readiness.get('score')
    if readiness_score is not None and readiness_score < 50:
        alerts.append({
            'type': 'readiness_low',
            'severity': 'danger',
            'ar': 'مؤشر الجاهزية انخفض. تحتاج حالة اللاعب إلى مراقبة إضافية.',
            'en': 'Readiness indicator is low. Player\'s condition needs additional monitoring.'
        })

    return alerts


def sessions_to_dicts(sessions) -> list:
    """Convert ORM session objects to dicts for calculations."""
    result = []
    for s in sessions:
        if hasattr(s, 'rpe') and not hasattr(s, 'training_intensity'):
            # TrainingSession model
            srpe = s.srpe if s.srpe else compute_srpe(s.training_duration, s.rpe)
            result.append({
                'date': s.date,
                'srpe': srpe,
                'rpe': s.rpe,
                'training_duration': s.training_duration,
                'sleep_quality': s.sleep_quality,
                'fatigue': s.fatigue,
                'muscle_soreness': s.muscle_soreness,
                'stress_level': s.stress_level,
                'resting_heart_rate': s.resting_heart_rate,
                'respiratory_rate': getattr(s, 'respiratory_rate', None),
            })
        else:
            # FatigueEntry (legacy) - training_intensity is RPE
            rpe = s.training_intensity
            srpe = compute_srpe(s.training_duration, rpe)
            result.append({
                'date': s.date,
                'srpe': srpe,
                'rpe': rpe,
                'training_duration': s.training_duration,
                'sleep_quality': s.sleep_quality,
                'fatigue': None,
                'muscle_soreness': s.muscle_soreness,
                'stress_level': s.stress_level,
                'resting_heart_rate': s.resting_heart_rate,
                'respiratory_rate': getattr(s, 'respiratory_rate', None),
            })
    return result


# ==================== ROUTES ====================

@router.post("/", response_model=schemas.FatigueEntry)
def create_fatigue_entry(entry: schemas.FatigueEntryCreate, db: Session = Depends(get_db)):
    db_entry = models.FatigueEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/{player_id}", response_model=list)
def read_fatigue_entries(player_id: int, db: Session = Depends(get_db)):
    return db.query(models.FatigueEntry).filter(
        models.FatigueEntry.player_id == player_id
    ).order_by(models.FatigueEntry.date.desc()).all()


@router.get("/{player_id}/acwr")
def calculate_acwr(player_id: int, db: Session = Depends(get_db)):
    """
    Correct ACWR calculation:
    - sRPE = training_duration × RPE
    - Acute Load = SUM of sRPE for last 7 days
    - Chronic Load = AVERAGE of 4 weekly sums (weeks before the acute window)
    - ACWR = Acute / Chronic

    Test: Acute=5625, Chronic=9843.75 => ACWR=0.57 => 'منخفض / أقل من المعتاد'
    """
    chronic_weeks = get_chronic_weeks(db)

    ts_sessions = db.query(models.TrainingSession).filter(
        models.TrainingSession.player_id == player_id
    ).order_by(models.TrainingSession.date).all()

    fe_sessions = db.query(models.FatigueEntry).filter(
        models.FatigueEntry.player_id == player_id
    ).order_by(models.FatigueEntry.date).all()

    all_sessions = sessions_to_dicts(ts_sessions) + sessions_to_dicts(fe_sessions)

    if not all_sessions:
        return {
            'acwr': None, 'acute_load': 0, 'chronic_load': 0,
            'status': 'لا توجد بيانات', 'status_en': 'No data',
            'classification': classify_acwr(0),
            'weekly_load': 0, 'monotony': None, 'strain': None, 'load_change_pct': None
        }

    acwr_data = compute_acwr_from_sessions(all_sessions, chronic_weeks)

    return {
        'acwr': acwr_data['acwr'],
        'acute_load': acwr_data['acute_load'],
        'chronic_load': acwr_data['chronic_load'],
        'status': acwr_data['classification']['status_ar'],
        'status_en': acwr_data['classification']['status_en'],
        'classification': acwr_data['classification'],
        'weekly_load': acwr_data['weekly_load'],
        'monotony': acwr_data['monotony'],
        'strain': acwr_data['strain'],
        'load_change_pct': acwr_data['load_change_pct'],
        'weekly_sums': acwr_data.get('weekly_sums', []),
    }


@router.get("/{player_id}/metrics")
def get_player_metrics(player_id: int, db: Session = Depends(get_db)):
    """Full player metrics: ACWR + Readiness + Alerts."""
    chronic_weeks = get_chronic_weeks(db)

    ts_sessions = db.query(models.TrainingSession).filter(
        models.TrainingSession.player_id == player_id
    ).order_by(models.TrainingSession.date).all()

    fe_sessions = db.query(models.FatigueEntry).filter(
        models.FatigueEntry.player_id == player_id
    ).order_by(models.FatigueEntry.date).all()

    all_sessions = sessions_to_dicts(ts_sessions) + sessions_to_dicts(fe_sessions)
    all_sessions.sort(key=lambda x: x['date'])

    acwr_data = compute_acwr_from_sessions(all_sessions, chronic_weeks)
    readiness = compute_readiness_score(all_sessions, acwr_data.get('acwr'))
    alerts = generate_alerts(all_sessions, acwr_data, readiness)

    latest = all_sessions[-1] if all_sessions else {}

    return {
        'acwr': acwr_data,
        'readiness': readiness,
        'alerts': alerts,
        'latest_wellness': {
            'sleep_quality': latest.get('sleep_quality'),
            'fatigue': latest.get('fatigue'),
            'muscle_soreness': latest.get('muscle_soreness'),
            'stress_level': latest.get('stress_level'),
            'rpe': latest.get('rpe'),
            'resting_heart_rate': latest.get('resting_heart_rate'),
            'respiratory_rate': latest.get('respiratory_rate'),
        },
        'session_count': len(all_sessions),
    }


@router.get("/{player_id}/chart-data")
def get_chart_data(player_id: int, weeks: int = 8, db: Session = Depends(get_db)):
    """Return daily data points for charting."""
    chronic_weeks = get_chronic_weeks(db)

    ts_sessions = db.query(models.TrainingSession).filter(
        models.TrainingSession.player_id == player_id
    ).order_by(models.TrainingSession.date).all()

    fe_sessions = db.query(models.FatigueEntry).filter(
        models.FatigueEntry.player_id == player_id
    ).order_by(models.FatigueEntry.date).all()

    all_sessions = sessions_to_dicts(ts_sessions) + sessions_to_dicts(fe_sessions)
    all_sessions.sort(key=lambda x: x['date'])

    daily_srpe: dict = defaultdict(float)
    daily_wellness: dict = {}

    for s in all_sessions:
        daily_srpe[s['date']] += s['srpe']
        daily_wellness[s['date']] = {
            'sleep_quality': s.get('sleep_quality'),
            'fatigue': s.get('fatigue'),
            'muscle_soreness': s.get('muscle_soreness'),
            'stress_level': s.get('stress_level'),
            'rpe': s.get('rpe'),
            'resting_heart_rate': s.get('resting_heart_rate'),
            'respiratory_rate': s.get('respiratory_rate'),
        }

    today = datetime.date.today()
    start = today - datetime.timedelta(days=weeks * 7)
    chart_points = []

    current = start
    while current <= today:
        date_str = current.isoformat()
        srpe = daily_srpe.get(date_str, 0)
        wellness = daily_wellness.get(date_str, {})

        # Compute rolling ACWR at this date point
        sessions_up_to = [s for s in all_sessions if s['date'] <= date_str]
        if len(sessions_up_to) >= 7:
            acwr_at_date = compute_acwr_from_sessions(sessions_up_to, chronic_weeks)
            acwr_val = acwr_at_date.get('acwr')
        else:
            acwr_val = None

        chart_points.append({
            'date': date_str,
            'srpe': srpe,
            'acwr': acwr_val,
            'sleep_quality': wellness.get('sleep_quality'),
            'fatigue': wellness.get('fatigue'),
            'muscle_soreness': wellness.get('muscle_soreness'),
            'stress_level': wellness.get('stress_level'),
            'rpe': wellness.get('rpe'),
        })
        current += datetime.timedelta(days=1)

    return {
        'daily': chart_points,
        'sessions': all_sessions,
    }


@router.get("/{player_id}/summary")
def get_summary(player_id: int, db: Session = Depends(get_db)):
    entries = db.query(models.FatigueEntry).filter(
        models.FatigueEntry.player_id == player_id
    ).order_by(models.FatigueEntry.date.desc()).limit(7).all()

    if not entries:
        return {'avg_sleep': 0, 'avg_stress': 0, 'avg_soreness': 0}

    avg_sleep = sum((e.sleep_quality or 0) for e in entries) / len(entries)
    avg_stress = sum((e.stress_level or 0) for e in entries) / len(entries)
    avg_soreness = sum((e.muscle_soreness or 0) for e in entries) / len(entries)

    return {
        'avg_sleep': round(avg_sleep, 2),
        'avg_stress': round(avg_stress, 2),
        'avg_soreness': round(avg_soreness, 2)
    }
