from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.db.session import engine
from app.db.init_database import init_database
from app.api.routers import units, sensors, readings
from psycopg.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

app = FastAPI(title="FastAPI internet of things")
init_database(engine)

# Routers
app.include_router(units.router)
app.include_router(sensors.router)
app.include_router(readings.router)

# Serve static files (CSS, JS, images...)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root -> load index.html
@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/health")
def health():
    return {"status": "health check successfully done"}

@app.exception_handler(IntegrityError)
async def db_integrity_handler(request, exc):
    if isinstance(exc.orig, ForeignKeyViolation):
        raise HTTPException(
            status_code=400,
            detail="Invalid foreign key: referenced resource does not exist."
        )
    raise HTTPException(status_code=400, detail="Database integrity error")
