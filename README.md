# 🚗 Prédiction de la Gravité des Accidents de la Route

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 📋 Description du Projet

Projet de Machine Learning visant à prédire la gravité d'un accident de la route (matériel, blessés légers, blessés graves, mortel) à partir des caractéristiques de l'accident : lieu, heure, conditions météorologiques, type de route et profil des usagers.

Ce projet a été réalisé dans le cadre d'un TP de Machine Learning sur une durée de 5 jours et propose un pipeline complet incluant :
- 📊 Nettoyage et préparation des données
- 🤖 Entraînement d'un modèle CatBoost
- 🚀 API FastAPI pour les prédictions
- 💻 Interface utilisateur Streamlit
- 🐳 Déploiement via Docker

## 🏗️ Architecture du Projet

```
tp_ml_voiture/
├── .github/workflows/      # CI/CD pipelines
├── backend/                # API FastAPI et logique métier
├── frontend/               # Interface Streamlit
├── notebook/               # Notebooks Jupyter (EDA, modélisation)
├── pdf/                    # Documentation PDF
├── tests/                  # Tests unitaires et d'intégration
├── veille_technologique/   # Documentation technique
├── docker-compose.yml      # Configuration Docker development
├── docker-compose.prod.yml # Configuration Docker production
├── pyproject.toml         # Configuration Poetry
└── requirements.txt       # Dépendances Python
```

## 🎯 Fonctionnalités

- ✅ Prédiction de la gravité des accidents en temps réel
- ✅ API REST documentée avec Swagger/OpenAPI
- ✅ Interface utilisateur intuitive
- ✅ Base de données PostgreSQL pour le logging
- ✅ Pipeline CI/CD automatisé
- ✅ Tests automatisés avec pre-commit hooks
- ✅ Détection de secrets avec detect-secrets

## 🚀 Démarrage Rapide

### Prérequis

- Docker >= 20.x
- Docker Compose >= 1.29 ou v2
- Python 3.10+ (pour développement local)

### Installation avec Docker

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/SalomeSouque/tp_ml_voiture.git
   cd tp_ml_voiture
   ```

2. **Lancer les services**
   ```bash
   docker-compose up --build -d
   ```

3. **Vérifier le statut des services**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

4. **Accéder aux services**
   - 🌐 API Backend : [http://localhost:8000](http://localhost:8000)
   - 📖 Documentation API : [http://localhost:8000/docs](http://localhost:8000/docs)
   - 🖥️ Interface Streamlit : [http://localhost:8501](http://localhost:8501)
   - 🗄️ PostgreSQL : `localhost:5000` (mappé depuis le port interne 5432)

### Installation Locale (Développement)

1. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env avec vos configurations
   ```

4. **Lancer l'API**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Lancer le frontend**
   ```bash
   cd frontend
   streamlit run app.py
   ```

## 📦 Services Docker

Le projet utilise Docker Compose pour orchestrer trois services principaux :

| Service | Port | Description |
|---------|------|-------------|
| `api` | 8000 | API FastAPI pour les prédictions |
| `my-postgres` | 5000:5432 | Base de données PostgreSQL |
| `predict_front` | 8501 | Interface utilisateur Streamlit |

### Variables d'environnement

Configuration PostgreSQL (à ajuster dans `docker-compose.yml`) :
- `POSTGRES_USER` : dbeaver
- `POSTGRES_PASSWORD` : dbeaver
- `POSTGRES_DB` : logging_accident

## 🧪 Tests et Qualité du Code

### Pre-commit Hooks

Le projet utilise pre-commit pour maintenir la qualité du code :

```bash
# Installer les hooks
pre-commit install

# Exécuter manuellement
pre-commit run --all-files
```

Hooks configurés :
- Détection de secrets (detect-secrets)
- Formatage du code
- Validation des fichiers YAML/JSON
- Trailing whitespace

### Tests

```bash
# Exécuter les tests
pytest tests/

# Avec couverture
pytest --cov=backend --cov=frontend tests/
```

## 🐳 Commandes Docker Utiles

```bash
# Construire et démarrer
docker-compose up --build -d

# Voir les logs
docker-compose logs -f api
docker-compose logs -f my-postgres
docker-compose logs -f predict_front

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Entrer dans un conteneur
docker exec -it model_call /bin/sh
docker exec -it my-postgres /bin/bash

# Vérifier la santé de PostgreSQL
docker exec -it my-postgres pg_isready -U dbeaver -d logging_accident

# Rebuild complet (sans cache)
docker-compose build --no-cache
docker-compose up -d
```

## 🔍 API Endpoints

### Endpoints principaux

```bash
# Health check
curl http://localhost:8000/gravite

# Prédiction
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "lieu": "urbain",
       "heure": "18:30",
       "meteo": "pluie",
       "type_route": "départementale"
     }'
```

Documentation complète disponible sur : [http://localhost:8000/docs](http://localhost:8000/docs)

## 📊 Données

### Source des données

Les données proviennent de la **Base de données des Accidents Corporels de la Circulation** (BAAC) :
- 🔗 Source : [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024/)
- 📅 Période : 2005-2024
- 📈 Mise à jour : Annuelle

### Structure des données

Les données comprennent les caractéristiques suivantes :
- Localisation (département, commune, coordonnées GPS)
- Temporalité (date, heure, jour de la semaine)
- Conditions (météo, luminosité, type de route)
- Usagers (âge, sexe, catégorie d'usager)
- Véhicules impliqués
- Gravité de l'accident (variable cible)

## 🤖 Modèle de Machine Learning

### Algorithme utilisé

- **CatBoost** : Gradient boosting optimisé pour les variables catégorielles
- Gestion native des variables catégorielles
- Robuste au surapprentissage
- Performances élevées sur données tabulaires

### Pipeline de modélisation

1. **Prétraitement** (`notebook/`)
   - Nettoyage des données
   - Gestion des valeurs manquantes
   - Encodage des variables catégorielles
   - Feature engineering

2. **Entraînement** (`notebook/`)
   - Séparation train/test
   - Validation croisée
   - Optimisation des hyperparamètres
   - Évaluation des performances

3. **Déploiement** (`backend/`)
   - Sauvegarde du modèle
   - Intégration dans l'API
   - Monitoring des prédictions

## 📚 Documentation Complémentaire

- 📓 **Notebooks** : Analyses exploratoires et modélisation dans `notebook/`
- 📄 **PDF** : Documentation détaillée dans `pdf/`
- 🔧 **Veille technique** : Ressources et recherches dans `veille_technologique/`

## 🛠️ Technologies Utilisées

### Backend
- **FastAPI** : Framework web moderne et performant
- **CatBoost** : Algorithme de machine learning
- **PostgreSQL** : Base de données relationnelle
- **Pydantic** : Validation des données
- **SQLAlchemy** : ORM pour PostgreSQL

### Frontend
- **Streamlit** : Interface utilisateur interactive
- **Pandas** : Manipulation de données
- **Plotly** : Visualisations interactives

### DevOps
- **Docker** : Conteneurisation
- **Docker Compose** : Orchestration multi-conteneurs
- **GitHub Actions** : CI/CD
- **pre-commit** : Hooks de qualité de code

### Qualité & Tests
- **pytest** : Framework de tests
- **detect-secrets** : Détection de secrets
- **black** : Formatage du code
- **flake8** : Linting

## 🚢 Déploiement en Production

### Configuration Production

Utiliser le fichier `docker-compose.prod.yml` pour le déploiement en production :

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Recommandations de sécurité

- [ ] Modifier les mots de passe par défaut
- [ ] Utiliser des variables d'environnement sécurisées
- [ ] Configurer un reverse proxy (Nginx/Traefik)
- [ ] Activer HTTPS avec Let's Encrypt
- [ ] Mettre en place des backups automatiques de la base de données
- [ ] Configurer les limites de ressources Docker
- [ ] Activer les logs et monitoring

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Guidelines

- Respecter le style de code existant
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation si nécessaire
- Vérifier que les pre-commit hooks passent

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **Salomé Souque** - [@SalomeSouque](https://github.com/SalomeSouque)

## 🙏 Remerciements

- Data.gouv.fr pour la mise à disposition des données BAAC
- La communauté open-source pour les outils utilisés
- Les contributeurs du projet

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à :
- Ouvrir une issue sur GitHub
- Contacter via GitHub

---

**Note** : Ce projet a été réalisé dans un cadre pédagogique. Les prédictions ne doivent pas être utilisées pour des décisions critiques sans validation appropriée.
