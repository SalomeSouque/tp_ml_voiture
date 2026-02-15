# Prédiction de la Gravité des Accidents de la Route

**Projet Machine Learning • Durée : 1 semaine (5 jours)**

## Description du projet
Ce projet vise à prédire la gravité d'un accident (ex. : matériel, blessés légers, blessés graves, mortel) à partir des caractéristiques de l'accident (lieu, heure, conditions météo, type de route, profil des usagers). Le pipeline inclut le nettoyage des données, l'entraînement d'un modèle (CatBoost), une API FastAPI pour servir les prédictions et une interface Streamlit pour l'interaction utilisateur.

---

## Prérequis
- Docker (>=20.x)
- Docker Compose (>=1.29 ou v2)
- Python 3.10+ (pour exécution locale sans Docker)
- (Optionnel) conda / virtualenv pour travail local

---

## Installation & déploiement (Docker)
1. Cloner le dépôt :
   ```bash
   git clone <votre-repo.git>
   cd tp_ml_voiture
   ```
2. Construire et lancer les services (API, Postgres, Frontend) :
   ```bash
   docker-compose up --build -d
   ```
3. Vérifier les logs :
   ```bash
   docker-compose logs -f api
   docker-compose logs -f my-postgres
   docker-compose logs -f predict_front
   ```
4. Accès :
   - API : http://localhost:8000
   - Frontend Streamlit : http://localhost:8501

> Remarque : le `docker-compose.yml` expose la base de données sur le port 5000 localement (`5000:5432`).

---

## Lien vers l'image DockerHub
- Image (exemple) : `dockerhub_username/tp_ml_voiture:latest`

Remplacez par le lien réel de votre image DockerHub si vous publiez une image : `docker pull dockerhub_username/tp_ml_voiture:TAG`.

---

## Commandes utiles
- Lancer en local (avec Docker Compose) :
  ```bash
  docker-compose up --build -d
  ```
- Arrêter et supprimer les conteneurs :
  ```bash
  docker-compose down
  ```
- Voir les logs en continu :
  ```bash
  docker-compose logs -f api
  ```
- Entrer dans le conteneur API :
  ```bash
  docker exec -it model_call /bin/sh
  ```
- Rebuild (forcer la reconstruction) :
  ```bash
  docker-compose build --no-cache
  docker-compose up -d
  ```
- Vérifier la santé de Postgres (depuis l'hôte) :
  ```bash
  docker exec -it my-postgres pg_isready -U dbeaver -d logging_accident
  ```
- Tester l'endpoint santé :
  ```bash
  curl http://localhost:8000/gravite
  ```

---

## Structure recommandée du dépôt
- `data/` : données brutes et jeu nettoyé
- `notebooks/` : notebooks Jupyter (collecte, nettoyage, EDA, modélisation)
- `backend/` : API, services, modèles de données
- `frontend/` : interface Streamlit
- `models/` : modèles sauvegardés

---

## Notes
- Documentez la version exacte de l'image DockerHub quand vous la publiez.
- Ajustez les variables d'environnement dans `docker-compose.yml` si nécessaire (utilisateur, mot de passe, DB).

---

## Sources :
- BAAC / data.gouv.fr : https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024/

---
