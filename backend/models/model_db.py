from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class AccidentPrediction(SQLModel, table=True):
        __tablename__ = "prediction_requete"
    #Bloc identification
        id: int | None = Field(default=None, primary_key=True)
        created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    #Bloc input user
        nb_usagers: int
        age_moyen: float
        age_min: int
        age_max: int
        presence_enfant: bool
        presence_senior: bool
        presence_pieton: bool
        presence_passager: bool
        nb_voiture: int
        nuit: bool
        heure: int
        lum: int
        atm: int
        catr: int
        surf: int

    #Bloc prédiction
        prediction: int | None = None
        proba_blessure_legere: float | None = None
        proba_blessure_grave: float | None = None

    #Bloc métadonnées
        success: bool
        error_message: str | None = None
        execution_time: float




