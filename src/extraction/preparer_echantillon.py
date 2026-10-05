"""Construction d'un échantillon stratifié pour l'exploration.

Conserve l'intégralité des transactions frauduleuses et un échantillon
aléatoire des transactions normales, afin de permettre une exploration
interactive sans charger les 6,3 millions de lignes.

L'échantillon sert à l'analyse exploratoire uniquement ; les traitements
de production s'appuient sur le fichier complet.

Exécution :
    python -m src.extraction.preparer_echantillon
"""

import pandas as pd

from src.config import DATA_INTERIM, DATA_RAW, FICHIER_PAYSIM, creer_dossiers
from src.journal import obtenir_journal

journal = obtenir_journal("echantillon")

SOURCE = DATA_RAW / "paysim" / FICHIER_PAYSIM
CIBLE = DATA_INTERIM / "paysim_echantillon.parquet"

TAILLE_NORMAL = 300_000
GRAINE = 42  # fixée pour que l'échantillon soit reproductible


def preparer() -> None:
    creer_dossiers()
    journal.info("Lecture du fichier complet")
    donnees = pd.read_csv(SOURCE)

    fraudes = donnees[donnees["isFraud"] == 1]
    normales = donnees[donnees["isFraud"] == 0].sample(n=TAILLE_NORMAL, random_state=GRAINE)

    echantillon = (
        pd.concat([fraudes, normales])
        .sample(frac=1, random_state=GRAINE)  # mélange
        .reset_index(drop=True)
    )

    echantillon.to_parquet(CIBLE, index=False)

    journal.info(
        "Échantillon écrit : %d lignes (%d fraudes, %d normales)",
        len(echantillon),
        len(fraudes),
        len(normales),
    )
    journal.info("Taille sur disque : %.1f Mo", CIBLE.stat().st_size / 1024**2)


if __name__ == "__main__":
    preparer()
