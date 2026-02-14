from contextlib import asynccontextmanager

from engine import engine
from fastapi import FastAPI
from routes.predict_route import router
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Wait for the database to be available before creating tables
    try:
        from engine import wait_for_db
        wait_for_db(retries=20, delay=1)
    except Exception as e:
        raise RuntimeError(f"Database is not ready: {e}")from e

    SQLModel.metadata.create_all(engine)
    yield



app = FastAPI(title="API Prédiction Gravité Accident", lifespan=lifespan)
app.include_router(router)

# Endpoint
@app.get("/gravite")  #health
def gravite():
    return {"status": "API en ligne"}









