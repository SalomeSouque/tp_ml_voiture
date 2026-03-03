# Architecture du projet

Ce fichier décrit l'architecture générale du projet de prédiction d'accidents.

## Structure des dossiers principaux

- `backend/` : Contient l'application serveur Python pour les prédictions.
  - `engine.py` : Point d'entrée principal de l'application.
  - `main.py` : Lancement et configuration de l'API.
  - `routes/` : Définit les endpoints (ex : `predict_route.py`).
  - `services/` : Logique métier (ex : `prediction_service.py`).
  - `model_prediction/` : Modules liés aux modèles.
    - `models/` : Classes pour la gestion des modèles (`accident.py`, `model_db.py`).

- `frontend/` : Application front-end (probablement Flask) servant l'interface utilisateur.
  - `app.py` : Application principale.

- `data/` : Données CSV par année et fichiers consolidés.

- `notebook/` : Carnets Jupyter pour exploration et nettoyage (`data_clean.ipynb`).

- `locustfile.py` : Scénarios de charge destinés à l'outil Locust, avec deux profils (`PredictUser` et `HealthCheckUser`).

- `tests/` : Contient les tests unitaires (`test_placeholder.py`).

- `catboost_info/` : Informations et sorties d'entraînement du modèle CatBoost.

- `veille_technologique/` : Documentation de veille sur différents sujets.

## Fichiers de configuration

- `pyproject.toml` et `requirements.txt` : Dépendances du projet.
- `docker-compose.yml`/`docker-compose.prod.yml` : Déploiement en conteneur.

## Flux de données et fonctionnement

1. **Collecte et préparation** : Les données CSV (`data/`) sont nettoyées via le notebook.
2. **Modélisation** : Les modèles CatBoost sont entraînés et gérés dans `model_prediction/models`.
3. **API** : `backend` expose des endpoints pour demander des prédictions.
4. **Service** : `prediction_service` gère la logique de chargement du modèle et génération des prédictions.
5. **Frontend** : Une interface utilisateur en `frontend/app.py` pour interagir avec l'API.
6. **Performance** : `locustfile.py` simule des utilisateurs faisant des requêtes de prédiction et un monitoring périodique.

Ce schéma permet de séparer clairement la logique de modèle, l'API et l'interface utilisateur, facilitant les tests et le déploiement.
