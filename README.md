# 🚗 Prédiction de la Gravité des Accidents de la Route

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitored-orange.svg)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboards-yellow.svg)](https://grafana.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black.svg)](https://github.com/features/actions)
[![Locust](https://img.shields.io/badge/Load%20Testing-Locust-green.svg)](https://locust.io/)

---

## 📋 Description

Projet **Data Science & MLOps** de bout en bout visant à prédire la gravité d'un accident de la route — blessure légère ou accident grave — à partir de ses caractéristiques : conditions météo, type de route, profil des usagers, heure, luminosité etc.

> 🎓 Réalisé dans le cadre d'une en développement en intelligence artificielle.
> L'accent a été mis sur la **mise en production complète** : API, monitoring, tests de charge et CI/CD.

---

## 🎯 Ce que ce projet démontre

Ce projet ne se limite pas à entraîner un modèle — il couvre **l'intégralité du cycle de vie d'une application ML en production** :

| Compétence | Technologie | Détail |
|-----------|-------------|--------|
| **Machine Learning** | Random Forest | Nettoyage, entraînement, optimisation, déploiement du modèle |
| **API Production** | FastAPI | Endpoints REST documentés, validation Pydantic |
| **Conteneurisation** | Docker Compose | Stack 8 services orchestrés |
| **Monitoring** | Prometheus + Grafana | Métriques custom, dashboards temps réel |
| **Observabilité** | node-exporter + cAdvisor | Métriques système et containers |
| **Tests de charge** | Locust | 3 paliers : 20 / 100 / 200 utilisateurs simultanés |
| **CI/CD** | GitHub Actions | Pipeline automatisé sur push |
| **Base de données** | PostgreSQL | Logging de chaque prédiction |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                           │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  FastAPI     │    │  Streamlit   │    │  PostgreSQL  │  │
│  │  :8000       │    │  :8501       │    │  :5432       │  │
│  │  /predict    │    │  Interface   │    │  Logging     │  │
│  │  /metrics ───┼────┼──────────────┼──▶ │  prédictions │  │
│  └──────┬───────┘    └──────────────┘    └──────────────┘  │
│         │ expose métriques                                   │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Prometheus  │◀───│node-exporter │    │   cAdvisor   │  │
│  │  :9090       │◀───│  :9100       │    │   :8080      │  │
│  │  scrape 15s  │    │  CPU/RAM/    │    │  métriques   │  │
│  └──────┬───────┘    │  Disque/Réseau│   │  containers  │  │
│         │            └──────────────┘    └──────────────┘  │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐                       │
│  │   Grafana    │    │    Locust    │                       │
│  │   :3000      │    │   :8089      │                       │
│  │  Dashboards  │    │  Stress test │                       │
│  └──────────────┘    └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 Data Science Pipeline

### 📦 Source des données

- **Base BAAC** (Accidents Corporels de la Circulation) — [data.gouv.fr](https://www.data.gouv.fr/...)
- **Période** : 2021 à 2024
- **3 tables fusionnées** : `caracteristiques`, `lieux`, `usagers`
- **Chargement automatisé** : boucle sur les répertoires par année, concaténation et normalisation des colonnes

---

### 🧹 Nettoyage des données

| Étape | Action | Détail |
|-------|--------|--------|
| **Sélection des colonnes** | Réduction du périmètre | 8 colonnes retenues par table (sur ~30) |
| **Suppression des doublons** | `drop_duplicates()` | Sur les 3 tables |
| **Types de colonnes** | Conversion `int`/`float` | Colonne `hrmn` objet → int, séparation heure/minute |
| **Coordonnées GPS** | Recadrage France métropolitaine | `lat` ∈ [41, 52] · `long` ∈ [-6, 10] |
| **Valeurs `-1`** | Remplacement par `NaN` | Signifient "non renseigné" dans la BAAC |
| **Valeurs manquantes** | Suppression si < 5% | Remplissage par moyenne pour `circ` |
| **Outliers âge** | Clipping percentile 5–95 | Suppression des âges aberrants > 100 ans |

---

### ⚙️ Feature Engineering

> L'idée clé : **agréger par accident** pour avoir 1 ligne = 1 accident.
```python
df_accident_final = df.groupby(['num_acc', 'year']).agg(
    gravite_accident  = ('grav', 'max'),
    nb_usagers        = ('grav', 'count'),
    age_moyen         = ('age', 'mean'),
    presence_enfant   = ('age', lambda x: int((x < 18).any())),
    presence_senior   = ('age', lambda x: int((x >= 75).any())),
    presence_pieton   = ('catu', lambda x: int((x == 3).any())),
    nuit              = ('nuit', 'max'),
    ...
)
```

**Observations clés de l'EDA :**
- 🌙 La nuit → proportion d'accidents graves significativement plus élevée
- 🛣️ Routes départementales → zone la plus accidentogène pour les accidents mortels
- 👴 Accidents mortels → âge médian ~45 ans, large dispersion toutes tranches d'âge
- 🗺️ Zones à risque : A7, A6, A61, A62 + littoral méditerranéen (toute saison)

---

### 🎯 Choix de la cible — Classification binaire
```python
# 0 = blessure légère  |  1 = accident grave (hospitalisé ou mortel)
df_ml['target'] = df_ml['gravite_accident'].apply(lambda x: 1 if x >= 2 else 0)
```

> La classe "mortel" était trop sous-représentée pour du multi-classe. La fusion en binaire améliore l'équilibre et la pertinence métier.

---

### 🤖 Comparaison des modèles — Split 80/20 stratifié

| Modèle | Accuracy | Precision (grave) | Recall (grave) | Décision |
|--------|----------|-------------------|----------------|----------|
| Régression Logistique | 0.65 | 0.50 | 0.64 | ❌ Baseline insuffisant |
| **Random Forest** | **0.67** | **0.52** | **0.64** | ✅ **Retenu** |
| CatBoost (v1) | 0.46 | — | **0.94** | ❌ Trop de faux positifs |

**Top features (Random Forest) :** `nb_usagers` · `age_moyen` · `heure` · `nb_voiture` · `catr` · `lum` · `presence_passager` · `atm`

---

## 📊 Monitoring & Observabilité

L'un des points forts de ce projet est sa **stack de monitoring complète**, identique à ce qu'on trouve en production professionnelle.

### Métriques custom instrumentées dans le code

```python
# Compteurs métier
predictions_total         # nombre total de prédictions
predictions_success_total # prédictions réussies
predictions_error_total   # prédictions en échec

# Histograms
prediction_duration_seconds   # latence du modèle CatBoost
prediction_proba_histogram    # distribution des probabilités prédites
```

### Dashboards Grafana

**Dashboard "HTTP Overview"** (6 panels) :
- Requêtes/seconde — Latence P95 — Taux d'erreur coloré
- Requêtes en cours — CPU % — RAM disponible

**Dashboard "Accident Prediction Overview"** (9 panels) :
- Total prédictions — Taux d'erreur — Latence P95
- Prédictions/seconde — Comportement du modèle ML — Durée moyenne
- CPU % machine — RAM disponible — RAM par container (cAdvisor)

### Requêtes PromQL clés

```promql
# Taux d'erreur en temps réel
rate(predictions_error_total[5m]) / rate(predictions_total[5m]) * 100

# Latence P95 du modèle
histogram_quantile(0.95, rate(prediction_duration_seconds_bucket[5m]))

# Comportement du modèle : probabilité médiane de gravité
histogram_quantile(0.50, rate(prediction_proba_histogram_bucket[5m]))

# CPU % de la machine hôte
100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

---

## ⚡ Tests de charge — Locust

3 paliers de charge testés avec **2 profils utilisateur** :

| Profil | Comportement | Part du trafic |
|--------|-------------|----------------|
| `PredictUser` | Envoie des prédictions variées (conditions aléatoires) | 75% |
| `HealthCheckUser` | Vérifie la disponibilité `/gravite` | 25% |

| Palier | Utilisateurs | Spawn rate | Objectif |
|--------|-------------|------------|---------|
| 🟢 Léger | 20 | 2/s | Baseline |
| 🟠 Moyen | 100 | 10/s | Comportement normal |
| 🔴 Élevé | 200 | 20/s | Point de rupture |

> Les résultats sont observés **en temps réel dans Grafana** pendant les tests.

---

## 🐳 Images Docker

Les images sont disponibles sur DockerHub et se téléchargent automatiquement au `docker-compose up` :

| Image | Lien |
|-------|------|
| **API FastAPI** | [`salomesouque/tp-ml-voiture-api`](https://hub.docker.com/r/salomesouque/tp-ml-voiture-api) |
| **Frontend Streamlit** | [`salomesouque/tp-ml-voiture-front`](https://hub.docker.com/r/salomesouque/tp-ml-voiture-front) |
```bash
docker pull salomesouque/tp-ml-voiture-api:latest
docker pull salomesouque/tp-ml-voiture-front:latest
```

| Tag | Description |
|-----|-------------|
| `latest` | Dernière version stable — mise à jour automatiquement à chaque push sur `main` |
| `1.0.0` | Version initiale |

> Les images `postgres:16`, `prom/prometheus`, `grafana/grafana` et les autres services
> sont des images officielles téléchargées directement depuis DockerHub.

---

## 🚀 Démarrage Rapide

### Prérequis

- [Docker](https://docs.docker.com/get-docker/) >= 20.x
- [Docker Compose](https://docs.docker.com/compose/install/) >= 1.29
- Fichier `.env` configuré (voir `.env.example`)

### Installation
```bash
# 1. Cloner le repo
git clone https://github.com/SalomeSouque/tp_ml_voiture.git
cd tp_ml_voiture

# 2. Configurer les variables d'environnement
cp .env.example .env

# 3. Lancer la stack complète (les images se téléchargent automatiquement)
docker-compose up -d

# 4. Vérifier que tous les services sont UP
docker-compose ps
```

> **Note** : le premier lancement peut prendre 1 à 2 minutes le temps de télécharger les images.
> Les lancements suivants sont quasi instantanés.

### Accès aux services

| Service | URL | Credentials |
|---------|-----|-------------|
| 🌐 API + Swagger | http://localhost:8000/docs | — |
| 🖥️ Frontend | http://localhost:8501 | — |
| 📊 Prometheus | http://localhost:9090 | — |
| 📈 Grafana | http://localhost:3000 | `admin` / `changeme` |
| ⚡ Locust | http://localhost:8089 | — |
| 🐳 cAdvisor | http://localhost:8080 | — |
| 🗄️ PostgreSQL | `localhost:5000` | voir `.env` |

### Exemple de prédiction

Via l'interface Streamlit sur http://localhost:8501 ou en ligne de commande :
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "nb_usagers": 3,
    "age_moyen": 25.0,
    "age_min": 18.0,
    "age_max": 45.0,
    "presence_enfant": false,
    "presence_senior": false,
    "presence_pieton": true,
    "presence_passager": true,
    "nb_voiture": 2,
    "nuit": true,
    "heure": 22,
    "lum": 3,
    "atm": 2,
    "catr": 3,
    "surf": 1
  }'
```

Réponse attendue :
```json
{
  "prediction": 1,
  "probability": {
    "blessure_legere": 0.32,
    "accident_grave": 0.68
  }
}
```

---

## 🔄 CI/CD — GitHub Actions

Le pipeline s'exécute automatiquement à chaque push sur `main` ou `develop` :
```
push sur main/develop
        ↓
┌─────────────────────┐     ┌─────────────────────┐
│  build-backend      │ ──▶ │  build-frontend      │
│  (ubuntu-latest)    │     │  (ubuntu-latest)     │
│                     │     │  needs: backend ✅   │
└─────────────────────┘     └─────────────────────┘
        ↓                           ↓
  ghcr.io/salomesouque/       ghcr.io/salomesouque/
  tp_ml_voiture-backend       tp_ml_voiture-frontend
```

### Images publiées automatiquement

Les images sont publiées sur **GitHub Container Registry (GHCR)** :

| Image | Registre |
|-------|---------|
| Backend (FastAPI) | `ghcr.io/salomesouque/tp_ml_voiture-backend` |
| Frontend (Streamlit) | `ghcr.io/salomesouque/tp_ml_voiture-frontend` |
```bash
docker pull ghcr.io/salomesouque/tp_ml_voiture-backend:develop
docker pull ghcr.io/salomesouque/tp_ml_voiture-frontend:develop
```

### Tags disponibles

| Tag | Description |
|-----|-------------|
| `develop` | Dernière version de la branche develop |
| `sha-xxxxxxx` | Build lié à un commit spécifique |

### Déclencheurs

| Événement | Effet |
|-----------|-------|
| Push sur `main` ou `develop` | Build + push des 2 images |
| Pull Request vers `main` | Build de vérification |
---

## 🧪 Qualité du Code

La qualité du code est assurée à **deux niveaux** : en local via pre-commit, et automatiquement via GitHub Actions à chaque push.

### Tests — pytest
```bash
pytest tests/ -v                              # tous les tests avec détail
pytest tests/ -v --cov=backend --cov-report=term-missing  # avec couverture
```

**6 tests couvrant les cas critiques :**

| Test | Fichier | Ce qu'il vérifie |
|------|---------|-----------------|
| `test_health_check` | `test_routes.py` | L'API démarre et répond |
| `test_predict_retourne_200` | `test_routes.py` | `/predict` fonctionne sans DB ni modèle réel |
| `test_predict_structure_reponse` | `test_routes.py` | Le contrat JSON est respecté |
| `test_predict_donnees_manquantes` | `test_routes.py` | Validation Pydantic → rejet 422 |
| `test_accident_schema_valide` | `test_models.py` | Le schéma accepte des données correctes |
| `test_accident_schema_type_incorrect` | `test_models.py` | Le schéma rejette les mauvais types |

> Les tests utilisent des **mocks** pour simuler la base de données et le modèle ML —
> aucune infrastructure externe nécessaire pour les faire tourner.

**Couverture actuelle : 61%** sur le backend

---

### Hooks pre-commit

Vérifications automatiques à chaque `git commit` :

| Outil | Rôle |
|-------|------|
| `ruff` | Linting et formatage Python |
| `mypy` | Vérification des types statiques |
| `bandit` | Détection de failles de sécurité |
| `safety` | Audit des dépendances vulnérables |
| `detect-secrets` | Empêche de committer des mots de passe |
```bash
# Installer les hooks
pre-commit install

# Lancer manuellement sur tout le projet
pre-commit run --all-files
```

---

## 📁 Structure du Projet

```
tp_ml_voiture/
├── .github/workflows/       # CI/CD GitHub Actions
├── backend/
│   ├── main.py              # FastAPI + Prometheus Instrumentator
│   ├── routes/
│   │   └── predict_route.py # Endpoint /predict + métriques custom
│   ├── services/
│   │   └── prediction_service.py
│   ├── models/
│   │   └── accident.py      # Schéma Pydantic
│   └── model_prediction/    # Modèle CatBoost sérialisé
├── frontend/                # Interface Streamlit
├── notebook/                # EDA + entraînement
├── tests/                   # Tests unitaires & intégration
├── locustfile.py            # Scénarios de charge
├── prometheus.yml           # Config scraping (4 jobs)
├── docker-compose.yml       # Stack 8 services
└── requirements.txt
```

---

## 🛠️ Stack Technique

**Machine Learning** : Python 3.11 · Random Forest · Pandas · Scikit-learn

**Backend** : FastAPI · SQLModel · PostgreSQL · Pydantic · prometheus-client

**Frontend** : Streamlit · Plotly

**Monitoring** : Prometheus · Grafana · node-exporter · cAdvisor · prometheus-fastapi-instrumentator

**DevOps** : Docker · Docker Compose · GitHub Actions · pre-commit · Locust

---

## 👤 Auteure

**Salomé Souque** — [@SalomeSouque](https://github.com/SalomeSouque)

> 📧 Pour toute question, ouvrir une issue sur GitHub.

---

*Projet réalisé dans un cadre pédagogique — les prédictions ne doivent pas être utilisées pour des décisions critiques sans validation appropriée.*
