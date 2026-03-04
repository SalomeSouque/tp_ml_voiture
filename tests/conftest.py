import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pytest

# On mocke les 3 choses qui nécessitent Docker :
# 1. joblib.load      → pas besoin du vrai fichier .pkl
# 2. wait_for_db      → pas besoin de la vraie DB
# 3. create_all       → pas besoin de créer les tables

with (
    patch("joblib.load", return_value=MagicMock()),
    patch("engine.wait_for_db", return_value=True),
    patch("sqlmodel.SQLModel.metadata.create_all", return_value=None),
):
    from backend.main import app

from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Client de test FastAPI — remplace un vrai navigateur."""
    with (
        patch("engine.wait_for_db", return_value=True),
        patch("sqlmodel.SQLModel.metadata.create_all", return_value=None),
    ):
        with TestClient(app) as c:
            yield c


@pytest.fixture
def accident_valide():
    """Données d'accident valides réutilisables dans tous les tests."""
    return {
        "nb_usagers": 2,
        "age_moyen": 30.0,
        "age_min": 18.0,
        "age_max": 45.0,
        "presence_enfant": 0,
        "presence_senior": 0,
        "presence_pieton": 0,
        "presence_passager": 1,
        "nb_voiture": 1,
        "nuit": 0,
        "heure": 14,
        "lum": 1,
        "atm": 1,
        "catr": 3,
        "surf": 1,
    }
