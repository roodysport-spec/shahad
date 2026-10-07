from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

# ========== PLAYER ==========
class PlayerBase(BaseModel):
    name: str
    name_en: str
    age: int
    weight: float
    height: float
    position: str
    dominant_hand: str
    team: Optional[str] = None
    jersey_number: Optional[int] = None
    injury_history: Optional[List[Any]] = []

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# ========== TRAINING SESSION ==========
class TrainingSessionBase(BaseModel):
    player_id: int
    date: str
    training_type: str = 'technical'
    training_duration: int
    rpe: int
    srpe: Optional[float] = None
    jump_count: Optional[int] = 0
    spike_count: Optional[int] = 0
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    fatigue: Optional[int] = None
    muscle_soreness: Optional[int] = None
    stress_level: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    notes: Optional[str] = None
    coach_notes: Optional[str] = None

class TrainingSessionCreate(TrainingSessionBase):
    pass

class TrainingSession(TrainingSessionBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# ========== OLD FATIGUE ENTRY (backward compat) ==========
class FatigueEntryBase(BaseModel):
    player_id: int
    date: str
    training_duration: int
    training_intensity: int
    jump_count: Optional[int] = 0
    spike_count: Optional[int] = 0
    sleep_quality: Optional[int] = None
    stress_level: Optional[int] = None
    muscle_soreness: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    notes: Optional[str] = None

class FatigueEntryCreate(FatigueEntryBase):
    pass

class FatigueEntry(FatigueEntryBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# ========== INJURY RECORD ==========
class InjuryRecordBase(BaseModel):
    player_id: int
    date: str
    injury_type: str
    body_part: str
    severity: str
    absence_days: int
    return_to_training: Optional[str] = None
    return_to_competition: Optional[str] = None
    is_recurrent: bool = False
    previous_injury_count: int = 0
    description: Optional[str] = None

class InjuryRecordCreate(InjuryRecordBase):
    pass

class InjuryRecord(InjuryRecordBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# ========== SYSTEM SETTINGS ==========
class SystemSettingBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

class SystemSettingCreate(SystemSettingBase):
    pass

class SystemSetting(SystemSettingBase):
    id: int
    updated_at: datetime
    class Config:
        from_attributes = True
