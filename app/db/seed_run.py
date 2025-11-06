from app.db.session import SessionLocal, engine
from app.db.init_database import init_database
from app.db.seed import run_seed


def main():
    init_database(engine)

    with SessionLocal() as session:
        run_seed(session)

if __name__ == "__main__":
    main()
