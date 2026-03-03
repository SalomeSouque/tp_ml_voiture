from contextlib import asynccontextmanager

from engine import engine
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from routes.predict_route import router
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Wait for the database to be available before creating tables
    try:
        from engine import wait_for_db

        wait_for_db(retries=20, delay=1)
    except Exception as e:
        raise RuntimeError(f"Database is not ready: {e}") from e

    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="API Prédiction Gravité Accident", lifespan=lifespan)
app.include_router(router)

# - instrument(app) =  observe toutes les requêtes HTTP automatiquement
# - expose(app) = crée l'endpoint GET /metrics que Prometheus va scraper
Instrumentator().instrument(app).expose(app)


# Endpoint
@app.get("/gravite")  # health
def gravite():
    return {"status": "API en ligne"}
