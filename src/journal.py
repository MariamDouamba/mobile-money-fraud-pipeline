"""Journalisation commune à tous les scripts du projet.

Écrit simultanément dans la console et dans un fichier horodaté,
afin de conserver une trace des exécutions (exigence de traçabilité).
"""

import logging
from datetime import datetime

from src.config import LOGS


def obtenir_journal(nom: str) -> logging.Logger:
    """Retourne un journal configuré pour le script appelant.

    Args:
        nom: nom du script, qui servira de préfixe au fichier de log.
    """
    LOGS.mkdir(parents=True, exist_ok=True)

    journal = logging.getLogger(nom)
    journal.setLevel(logging.INFO)

    # Évite d'ajouter plusieurs fois les mêmes gestionnaires
    if journal.handlers:
        return journal

    format_message = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Sortie console
    console = logging.StreamHandler()
    console.setFormatter(format_message)
    journal.addHandler(console)

    # Sortie fichier, un fichier par jour et par script
    horodatage = datetime.now().strftime("%Y%m%d")
    fichier = logging.FileHandler(LOGS / f"{nom}_{horodatage}.log", encoding="utf-8")
    fichier.setFormatter(format_message)
    journal.addHandler(fichier)

    return journal
