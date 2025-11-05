from sqlalchemy import Engine
from app.db.schema import metadata


def init_database(engine: Engine):
    metadata.create_all(bind=engine)
