import os

import requests
import streamlit as st

# api docker :
API_URL = os.getenv("API_URL", "http://api:8000")

# api local :
# API_URL = "http://127.0.0.1:8000"

st.title("Prédiction de la gravité d'un accident")

st.sidebar.header("Caractéristiques de l'accident")

# Formulaire utilisateur
accident = {
    "nb_usagers": int(st.sidebar.number_input("Nombre d'usagers", 1, 10, 2)),
    "age_moyen": float(st.sidebar.number_input("Âge moyen", 0, 100, 30)),
    "age_min": float(st.sidebar.number_input("Âge minimum", 0, 100, 18)),
    "age_max": float(st.sidebar.number_input("Âge maximum", 0, 100, 50)),
    "presence_enfant": int(st.sidebar.checkbox("Présence enfant")),
    "presence_senior": int(st.sidebar.checkbox("Présence senior")),
    "presence_pieton": int(st.sidebar.checkbox("Présence piéton")),
    "presence_passager": int(st.sidebar.checkbox("Présence passager")),
    "nb_voiture": int(st.sidebar.number_input("Nombre de voitures", 1, 10, 1)),
    "nuit": int(st.sidebar.checkbox("Accident de nuit")),
    "heure": int(st.sidebar.number_input("Heure (0-23)", 0, 23, 14)),
    # Pour les variables catégorielles :
    "lum": int(
        st.sidebar.selectbox(
            "Luminosité",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: {
                1: "Plein jour",
                2: "Crépuscule ou aube",
                3: "Nuit sans éclairage public",
                4: "Nuit avec éclairage public non allumé",
                5: "Nuit avec éclairage public allumé",
            }[x],
        )
    ),
    "atm": int(
        st.sidebar.selectbox(
            "Conditions atmosphériques",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            format_func=lambda x: {
                1: "Normale",
                2: "Pluie légère",
                3: "Pluie forte",
                4: "Neige - grêle",
                5: "Brouillard - fumée",
                6: "Vent fort - tempête",
                7: "Temps éblouissant",
                8: "Temps couvert",
                9: "Autre",
            }[x],
        )
    ),
    "catr": int(
        st.sidebar.selectbox(
            "Type de route",
            options=[1, 2, 3, 4, 5, 6, 7, 9],
            format_func=lambda x: {
                1: "Autoroute",
                2: "Route nationale",
                3: "Route Départementale",
                4: "Voie Communale",
                5: "Hors réseau public",
                6: "Parc de stationnement ouvert",
                7: "Routes métropole urbaine",
                9: "Autre",
            }[x],
        )
    ),
    "surf": int(
        st.sidebar.selectbox(
            "État de la surface",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            format_func=lambda x: {
                1: "Normale",
                2: "Mouillée",
                3: "Flaques",
                4: "Inondée",
                5: "Enneigée",
                6: "Boue",
                7: "Verglacée",
                8: "Corps gras – huile",
                9: "Autre",
            }[x],
        )
    ),
}

# Bouton prédiction
if st.button("Prédire la gravité"):
    # Utiliser un try pour catch les erreurs:
    try:
        response = requests.post(f"{API_URL}/predict", json=accident)
        response.raise_for_status()
        # Si code web est différent de 200 (donc ok) lève une erreur

        # Récupération du JSON
        result = response.json()  # Convertion au format json
        pred = result["prediction"]
        proba = result["probability"]

        if pred == 0:
            st.success(
                f"Prédiction : Blessure légère (probabilité {
                    proba['blessure_legere']:.2f})"
            )
        else:
            st.error(
                f"Prédiction : Accident grave (probabilité {
                    proba['accident_grave']:.2f})"
            )

    except requests.exceptions.HTTPError as err:
        # Le module request gère les erreur http
        # On affiche l'erreur
        st.error(f"Une erreur avec l'API est survenue : {err}")
        # On afficeh le contenu du JSON
        st.json(response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur connexion API: {e}")
