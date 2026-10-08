"""Configuration centrale du projet.

Charge les variables d'environnement et définit les chemins de travail.
Importé par tous les scripts, afin qu'un chemin ne soit jamais écrit en dur.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Racine du projet : deux niveaux au-dessus de ce fichier (src/config.py)
RACINE = Path(__file__).resolve().parent.parent

# Charge le fichier .env situé à la racine
load_dotenv(RACINE / ".env")

# Emplacements des données
DATA = RACINE / "data"
DATA_RAW = DATA / "raw"
DATA_INTERIM = DATA / "interim"
DATA_EXTERNAL = DATA / "external"

# Journaux d'exécution
LOGS = RACINE / "logs"

# Identifiant du jeu de données sur Kaggle
KAGGLE_DATASET = "ealaxi/paysim1"
FICHIER_PAYSIM = "PS_20174392719_1491204439457_log.csv"

DOSSIER_PAYSIM = DATA_RAW / "paysim"
CHEMIN_PAYSIM = DOSSIER_PAYSIM / FICHIER_PAYSIM


def verifier_identifiants_kaggle() -> None:
    """Vérifie la présence des identifiants avant tout appel à l'API.

    Lève une exception explicite plutôt que de laisser la bibliothèque
    Kaggle échouer avec un message peu lisible.
    """
    manquants = [cle for cle in ("KAGGLE_USERNAME", "KAGGLE_KEY") if not os.getenv(cle)]
    if manquants:
        raise RuntimeError(
            f"Identifiants Kaggle absents du fichier .env : {', '.join(manquants)}. "
            "Créer un jeton sur kaggle.com (Settings > API > Create New Token)."
        )


def creer_dossiers() -> None:
    """Crée les dossiers de travail s'ils n'existent pas."""
    for dossier in (DATA_RAW, DATA_INTERIM, DATA_EXTERNAL, LOGS):
        dossier.mkdir(parents=True, exist_ok=True)


CLE_FACTICE = "AKIAIOSFODNN7EXAMPLE"
