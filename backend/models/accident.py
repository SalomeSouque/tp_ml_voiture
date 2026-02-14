from sqlmodel import SQLModel


# Utilisation de pydantic et des class comme vu en alternance :
# Je crée une class avec basemodel en paramètre, qui me permet
# de créer un modèle ou un schéma à suivre de mes données avec leur attirbut
# Gestion des erreurs facilité grace a pydantic entre autre avantage
class Accident(SQLModel):
    nb_usagers: int
    age_moyen: float
    age_min: float
    age_max: float
    presence_enfant: int
    presence_senior: int
    presence_pieton: int
    presence_passager: int
    nb_voiture: int
    nuit: int
    heure: int
    lum: int
    atm: int
    catr: int
    surf: int
