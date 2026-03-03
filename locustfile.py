# locustfile.py
import random

from locust import HttpUser, between, task


class PredictUser(HttpUser):
    """
    Profil 1 — Utilisateur qui fait des prédictions
    Simule un vrai usage de l'API avec des données variées
    wait_time = attend entre 1 et 3 secondes entre chaque requête
    """

    wait_time = between(1, 3)
    weight = 3  # 3x plus fréquent que HealthCheckUser

    @task
    def predict_accident(self):
        """Envoie une prédiction avec des paramètres aléatoires"""
        payload = {
            "nb_usagers": random.randint(1, 8),
            "age_moyen": round(random.uniform(18, 80), 1),
            "age_min": round(random.uniform(10, 40), 1),
            "age_max": round(random.uniform(40, 90), 1),
            "presence_enfant": random.choice([True, False]),
            "presence_senior": random.choice([True, False]),
            "presence_pieton": random.choice([True, False]),
            "presence_passager": random.choice([True, False]),
            "nb_voiture": random.randint(1, 10),
            "nuit": random.choice([True, False]),
            "heure": random.randint(0, 23),
            "lum": random.randint(1, 5),
            "atm": random.randint(1, 8),
            "catr": random.randint(1, 7),
            "surf": random.randint(1, 9),
        }
        self.client.post(
            "/predict",
            json=payload,
            name="/predict",  # nom affiché dans l'interface Locust
        )

    @task(2)  # effectué 2x plus souvent que predict_accident
    def predict_accident_grave(self):
        """Scénario typique d'accident grave — conditions difficiles"""
        payload = {
            "nb_usagers": random.randint(3, 8),
            "age_moyen": round(random.uniform(18, 80), 1),
            "age_min": round(random.uniform(10, 25), 1),
            "age_max": round(random.uniform(60, 90), 1),
            "presence_enfant": True,
            "presence_senior": True,
            "presence_pieton": True,
            "presence_passager": True,
            "nb_voiture": random.randint(3, 10),
            "nuit": True,
            "heure": random.randint(20, 23),
            "lum": random.randint(3, 5),
            "atm": random.randint(3, 8),
            "catr": random.randint(3, 7),
            "surf": random.randint(3, 9),
        }
        self.client.post("/predict", json=payload, name="/predict (grave)")


class HealthCheckUser(HttpUser):
    """
    Profil 2 — Utilisateur léger (lecture seule)
    Simule un monitoring ou un load balancer qui vérifie
    que l'API est en vie
    wait_time = attend entre 2 et 5 secondes
    """

    wait_time = between(2, 5)
    weight = 1  # moins fréquent que PredictUser

    @task
    def health_check(self):
        """Vérifie juste que l'API répond"""
        self.client.get("/gravite", name="/gravite (health)")
