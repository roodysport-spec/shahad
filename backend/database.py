from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./volleyball.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def run_migrations():
    """
    Run safe incremental migrations using ALTER TABLE.
    SQLite supports ADD COLUMN only (no DROP/RENAME), so we just add missing columns.
    """
    migrations = [
        # Players table: add new columns
        ("players", "team", "ALTER TABLE players ADD COLUMN team TEXT"),
        ("players", "jersey_number", "ALTER TABLE players ADD COLUMN jersey_number INTEGER"),

        # FatigueEntry table: add new wellness columns
        ("fatigue_entries", "fatigue", "ALTER TABLE fatigue_entries ADD COLUMN fatigue INTEGER"),
        ("fatigue_entries", "sleep_hours", "ALTER TABLE fatigue_entries ADD COLUMN sleep_hours REAL"),
        ("fatigue_entries", "training_type", "ALTER TABLE fatigue_entries ADD COLUMN training_type TEXT"),
        ("fatigue_entries", "coach_notes", "ALTER TABLE fatigue_entries ADD COLUMN coach_notes TEXT"),
        ("fatigue_entries", "resting_heart_rate", "ALTER TABLE fatigue_entries ADD COLUMN resting_heart_rate INTEGER"),
        ("fatigue_entries", "respiratory_rate", "ALTER TABLE fatigue_entries ADD COLUMN respiratory_rate INTEGER"),

        # TrainingSession table: add physiological and biomechanical columns
        ("training_sessions", "resting_heart_rate", "ALTER TABLE training_sessions ADD COLUMN resting_heart_rate INTEGER"),
        ("training_sessions", "respiratory_rate", "ALTER TABLE training_sessions ADD COLUMN respiratory_rate INTEGER"),
        ("training_sessions", "jump_count", "ALTER TABLE training_sessions ADD COLUMN jump_count INTEGER DEFAULT 0"),
        ("training_sessions", "spike_count", "ALTER TABLE training_sessions ADD COLUMN spike_count INTEGER DEFAULT 0"),

        # InjuryRecord table: add new detailed columns
        ("injury_records", "injury_type", "ALTER TABLE injury_records ADD COLUMN injury_type TEXT"),
        ("injury_records", "body_part", "ALTER TABLE injury_records ADD COLUMN body_part TEXT"),
        ("injury_records", "severity", "ALTER TABLE injury_records ADD COLUMN severity TEXT DEFAULT 'mild'"),
        ("injury_records", "absence_days", "ALTER TABLE injury_records ADD COLUMN absence_days INTEGER DEFAULT 0"),
        ("injury_records", "return_to_training", "ALTER TABLE injury_records ADD COLUMN return_to_training TEXT"),
        ("injury_records", "return_to_competition", "ALTER TABLE injury_records ADD COLUMN return_to_competition TEXT"),
        ("injury_records", "is_recurrent", "ALTER TABLE injury_records ADD COLUMN is_recurrent BOOLEAN DEFAULT 0"),
        ("injury_records", "previous_injury_count", "ALTER TABLE injury_records ADD COLUMN previous_injury_count INTEGER DEFAULT 0"),
        ("injury_records", "description", "ALTER TABLE injury_records ADD COLUMN description TEXT"),
    ]

    with engine.connect() as conn:
        for table, col, sql in migrations:
            try:
                # Check if column already exists
                result = conn.execute(text(f"PRAGMA table_info({table})"))
                existing_cols = [row[1] for row in result.fetchall()]

                if col not in existing_cols:
                    conn.execute(text(sql))
                    conn.commit()
                    logger.info(f"Migration: added {table}.{col}")
                else:
                    pass  # Column already exists, skip
            except Exception as e:
                # Log but don't fail startup
                logger.debug(f"Migration skipped {table}.{col}: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
