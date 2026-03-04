import pytest
from pydantic import ValidationError

from backend.models.accident import Accident


def test_accident_schema_valide():
    """
    STRICT MINIMUM : vérifier que le schéma Pydantic accepte
    des données correctes sans lever d'erreur.
    C'est le contrat entre le front et le back — si ce test casse,
    le front et le back ne se parlent plus.
    """
    accident = Accident(
        nb_usagers=2,
        age_moyen=30.0,
        age_min=18.0,
        age_max=45.0,
        presence_enfant=0,
        presence_senior=0,
        presence_pieton=0,
        presence_passager=1,
        nb_voiture=1,
        nuit=0,
        heure=14,
        lum=1,
        atm=1,
        catr=3,
        surf=1,
    )
    assert accident.nb_usagers == 2
    assert accident.age_moyen == 30.0


def test_accident_schema_type_incorrect():
    """
    STRICT MINIMUM : vérifier que Pydantic rejette un mauvais type.
    Exemple : envoyer "bonjour" pour nb_usagers qui attend un int.
    """
    with pytest.raises(ValidationError):
        Accident(
            nb_usagers="bonjour",  # ← mauvais type
            age_moyen=30.0,
            age_min=18.0,
            age_max=45.0,
            presence_enfant=0,
            presence_senior=0,
            presence_pieton=0,
            presence_passager=1,
            nb_voiture=1,
            nuit=0,
            heure=14,
            lum=1,
            atm=1,
            catr=3,
            surf=1,
        )
