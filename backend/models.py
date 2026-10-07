from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Boolean, Text
import datetime
from .database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)         # Arabic name
    name_en = Column(String)                  # English name
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    position = Column(String)                 # goalkeeper, left_back, right_back, center_back, left_wing, right_wing, pivot
    dominant_hand = Column(String)            # right / left
    team = Column(String, nullable=True)      # team name
    jersey_number = Column(Integer, nullable=True)
    injury_history = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TrainingSession(Base):
    __tablename__ = "training_sessions"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, index=True)
    date = Column(String, index=True)         # YYYY-MM-DD
    training_type = Column(String)            # e.g. 'technical', 'physical', 'match', 'recovery'
    training_duration = Column(Integer)       # minutes
    rpe = Column(Integer)                     # Rate of Perceived Exertion 1-10
    srpe = Column(Float)                      # sRPE = duration * rpe (calculated automatically)
    jump_count = Column(Integer, nullable=True, default=0)   # عدد القفزات
    spike_count = Column(Integer, nullable=True, default=0)  # عدد الضربات الساحقة
    sleep_hours = Column(Float, nullable=True)
    sleep_quality = Column(Integer, nullable=True)   # 1-10
    fatigue = Column(Integer, nullable=True)         # 1-10 (higher = more fatigued)
    muscle_soreness = Column(Integer, nullable=True) # 1-10
    stress_level = Column(Integer, nullable=True)    # 1-10 (psychological stress)
    resting_heart_rate = Column(Integer, nullable=True) # bpm (نبض الراحة)
    respiratory_rate = Column(Integer, nullable=True)   # breaths/min (معدل التنفس في الراحة)
    notes = Column(Text, nullable=True)
    coach_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class InjuryRecord(Base):
    __tablename__ = "injury_records"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, index=True)
    date = Column(String)                     # YYYY-MM-DD
    injury_type = Column(String)              # e.g. 'sprain', 'strain', 'fracture', 'contusion'
    body_part = Column(String)                # body location
    severity = Column(String)                 # 'mild', 'moderate', 'severe'
    absence_days = Column(Integer)            # days out
    return_to_training = Column(String, nullable=True)      # YYYY-MM-DD
    return_to_competition = Column(String, nullable=True)   # YYYY-MM-DD
    is_recurrent = Column(Boolean, default=False)
    previous_injury_count = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SystemSettings(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)
    description = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Keep old FatigueEntry for backward compatibility with existing data
class FatigueEntry(Base):
    __tablename__ = "fatigue_entries"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, index=True)
    date = Column(String)
    training_duration = Column(Integer)
    training_intensity = Column(Integer)
    jump_count = Column(Integer, nullable=True)
    spike_count = Column(Integer, nullable=True)
    sleep_quality = Column(Integer, nullable=True)
    stress_level = Column(Integer, nullable=True)
    muscle_soreness = Column(Integer, nullable=True)
    resting_heart_rate = Column(Integer, nullable=True)
    respiratory_rate = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
