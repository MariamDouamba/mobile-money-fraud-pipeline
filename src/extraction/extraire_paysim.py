"""Extraction du jeu de données PaySim depuis l'API Kaggle.

Source      : service web (API REST Kaggle)
Destination : data/raw/paysim/
Fréquence   : chargement initial, puis à la demande

Exécution :
    python -m src.extraction.extraire_paysim
"""

import hashlib
import sys
import time
from pathlib import Path

from src.config import (
    DATA_RAW,
    FICHIER_PAYSIM,
    KAGGLE_DATASET,
    creer_dossiers,
    verifier_identifiants_kaggle,
)
from src.journal import obtenir_journal

journal = obtenir_journal("extraction_paysim")

DESTINATION = DATA_RAW / "paysim"
TENTATIVES_MAX = 3
ATTENTE_ENTRE_TENTATIVES = 5  # secondes


def empreinte_fichier(chemin: Path) -> str:
    """Calcule l'empreinte SHA-256 d'un fichier, par blocs.

    La lecture par blocs évite de charger en mémoire un fichier
    de plusieurs centaines de mégaoctets.
    """
    empreinte = hashlib.sha256()
    with chemin.open("rb") as flux:
        for bloc in iter(lambda: flux.read(1024 * 1024), b""):
            empreinte.update(bloc)
    return empreinte.hexdigest()


def telecharger(destination: Path) -> None:
    """Télécharge et décompresse le jeu de données depuis Kaggle.

    L'import de la bibliothèque Kaggle est volontairement local :
    elle tente de s'authentifier dès son chargement, et nous voulons
    avoir vérifié les identifiants avant.
    """
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    journal.info("Authentification auprès de l'API Kaggle réussie")

    journal.info("Téléchargement du jeu de données %s en cours", KAGGLE_DATASET)
    api.dataset_download_files(
        KAGGLE_DATASET,
        path=str(destination),
        unzip=True,
        quiet=False,
    )


def extraire() -> Path:
    """Point d'entrée de l'extraction.

    Returns:
        Le chemin du fichier extrait.

    Raises:
        RuntimeError: si l'extraction échoue après plusieurs tentatives,
            ou si le fichier attendu est absent à l'issue du téléchargement.
    """
    debut = time.time()
    journal.info("--- Début de l'extraction PaySim ---")

    verifier_identifiants_kaggle()
    creer_dossiers()
    DESTINATION.mkdir(parents=True, exist_ok=True)

    cible = DESTINATION / FICHIER_PAYSIM

    # Idempotence : ne pas retélécharger un fichier déjà présent
    if cible.exists():
        journal.info(
            "Fichier déjà présent (%.1f Mo), téléchargement ignoré",
            cible.stat().st_size / 1024**2,
        )
        return cible

    derniere_erreur: Exception | None = None
    for tentative in range(1, TENTATIVES_MAX + 1):
        try:
            telecharger(DESTINATION)
            break
        except Exception as erreur:  # noqa: BLE001 — on veut toute défaillance réseau
            derniere_erreur = erreur
            journal.warning(
                "Tentative %d sur %d échouée : %s",
                tentative,
                TENTATIVES_MAX,
                erreur,
            )
            if tentative < TENTATIVES_MAX:
                time.sleep(ATTENTE_ENTRE_TENTATIVES)
    else:
        journal.error("Extraction abandonnée après %d tentatives", TENTATIVES_MAX)
        raise RuntimeError(f"Échec du téléchargement depuis Kaggle : {derniere_erreur}")

    if not cible.exists():
        trouves = [f.name for f in DESTINATION.iterdir()]
        raise RuntimeError(
            f"Fichier attendu absent : {FICHIER_PAYSIM}. " f"Fichiers présents : {trouves}"
        )

    taille_mo = cible.stat().st_size / 1024**2
    journal.info("Fichier extrait : %s (%.1f Mo)", cible.name, taille_mo)

    journal.info("Calcul de l'empreinte d'intégrité en cours")
    empreinte = empreinte_fichier(cible)
    journal.info("Empreinte SHA-256 : %s", empreinte)

    # Sauvegarde du résultat : trace de l'extraction à côté du fichier
    (DESTINATION / "EMPREINTE.txt").write_text(f"{empreinte}  {cible.name}\n", encoding="utf-8")

    duree = time.time() - debut
    journal.info("--- Extraction terminée en %.1f s ---", duree)
    return cible


if __name__ == "__main__":
    try:
        extraire()
    except Exception as erreur:  # noqa: BLE001
        journal.error("Extraction en échec : %s", erreur)
        sys.exit(1)
