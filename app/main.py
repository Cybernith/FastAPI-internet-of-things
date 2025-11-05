from fastapi import FastAPI
from app.db.session import engine
from app.db.init_database import init_database
from app.api.routers import units, sensors, readings

app = FastAPI(title="FastAPI internet of things")
init_database(engine)

app.include_router(units.router)
app.include_router(sensors.router)
app.include_router(readings.router)


@app.get("/health")
def health():
    return {"status": "health check successfully done"}

