from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, run_migrations
from .routers import players, fatigue, injury, sessions, settings, team

# Run migrations first (adds new columns to existing DB without data loss)
run_migrations()
# Then create any new tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SHM LOAD API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:3000", "http://127.0.0.1:3000", "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)
app.include_router(fatigue.router)
app.include_router(injury.router)
app.include_router(sessions.router)
app.include_router(settings.router)
app.include_router(team.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to SHM LOAD API v2.0",
        "sport": "volleyball",
        "version": "2.0.0",
        "endpoints": ["/players", "/fatigue", "/sessions", "/injury", "/settings", "/team"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
