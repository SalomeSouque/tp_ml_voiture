import os
import time

from sqlmodel import Session, create_engine

# Configuration via variables d'environnement
POSTGRES_USER = os.getenv("POSTGRES_USER", "dbeaver")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root")
POSTGRES_DB = os.getenv("POSTGRES_DB", "logging_accident")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")  # Nom du service Docker
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# En local :
# engine = create_engine(
# "postgresql+psycopg2://dbeaver:root@localhost:5432/logging_accident",
#  echo=True)

# Avec docker :
engine = create_engine(DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session


# En local :
# engine =  create_engine("
# postgresql+psycopg2://dbeaver:root@localhost:5432/logging_accident")
# Session = sessionmaker(bind=engine)


# Helper to wait for DB to be ready instead of connecting at import time
def wait_for_db(retries: int = 10, delay: float = 1.0):
    """Wait for the database to accept connections.

    Raises RuntimeError if the DB is not reachable after given retries.
    """
    for attempt in range(1, retries + 1):
        try:
            with engine.connect():
                return True
        except Exception as err:
            if attempt == retries:
                raise RuntimeError(
                    "Could not connect to the database after multiple attempts"
                ) from err
            time.sleep(delay)
