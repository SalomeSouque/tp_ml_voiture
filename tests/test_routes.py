from unittest.mock import MagicMock, patch


def test_health_check(client):
    """
    STRICT MINIMUM : vérifier que l'API est en vie.
    Si ce test échoue → l'API ne démarre même pas correctement.
    C'est le premier test que tout projet doit avoir.
    """
    response = client.get("/gravite")

    assert response.status_code == 200
    assert response.json() == {"status": "API en ligne"}


def test_predict_retourne_200(client, accident_valide):
    """
    STRICT MINIMUM : vérifier que l'endpoint /predict répond sans planter.
    On ne teste pas la qualité de la prédiction (c'est le rôle du ML),
    juste que l'API reçoit les données et renvoie quelque chose.
    """
    # On remplace le vrai modèle par un faux qui renvoie toujours 0
    mock_model = MagicMock()
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [[0.7, 0.3]]

    with patch("routes.predict_route.model", mock_model):
        with patch("routes.predict_route.save_prediction"):  # on ne touche pas à la DB
            response = client.post("/predict", json=accident_valide)

    assert response.status_code == 200


def test_predict_structure_reponse(client, accident_valide):
    """
    STRICT MINIMUM : vérifier que la réponse JSON contient bien
    les clés "prediction" et "probability".
    Si quelqu'un modifie le format de retour sans le dire,
    ce test cassera et alertera.
    """
    mock_model = MagicMock()
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [[0.7, 0.3]]

    with patch("routes.predict_route.model", mock_model):
        with patch("routes.predict_route.save_prediction"):
            response = client.post("/predict", json=accident_valide)

    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert "blessure_legere" in data["probability"]
    assert "accident_grave" in data["probability"]


def test_predict_donnees_manquantes(client):
    """
    STRICT MINIMUM : vérifier que l'API rejette des données incomplètes.
    Pydantic/FastAPI renvoie automatiquement 422 si un champ obligatoire
    manque — ce test vérifie que cette protection fonctionne bien.
    """
    données_incomplètes = {"nb_usagers": 2}  # il manque tous les autres champs

    response = client.post("/predict", json=données_incomplètes)

    assert response.status_code == 422  # Unprocessable Entity
