"""Analyse ciblée des transactions frauduleuses.

Vérifie des hypothèses de détection sur le périmètre où la fraude existe
(TRANSFER et CASH_OUT), afin de fonder les règles sur des faits observés.

Exécution :
    python -m src.extraction.analyser_fraude
"""

import pandas as pd

from src.config import DATA_RAW, FICHIER_PAYSIM
from src.journal import obtenir_journal

journal = obtenir_journal("analyse_fraude")

SOURCE = DATA_RAW / "paysim" / FICHIER_PAYSIM
COLONNES = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "newbalanceOrig",
    "nameDest",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
]


def analyser() -> None:
    journal.info("Lecture du périmètre TRANSFER et CASH_OUT")
    donnees = pd.read_csv(SOURCE, usecols=COLONNES)
    perimetre = donnees[donnees["type"].isin(["TRANSFER", "CASH_OUT"])].copy()
    journal.info("Périmètre : %d transactions", len(perimetre))

    fraude = perimetre[perimetre["isFraud"] == 1]
    normal = perimetre[perimetre["isFraud"] == 0]

    print("\n=== Hypothèse 1 : le compte émetteur est vidé ===")
    for nom, jeu in (("Fraude", fraude), ("Normal", normal)):
        vide = ((jeu["newbalanceOrig"] == 0) & (jeu["oldbalanceOrg"] > 0)).mean()
        print(f"{nom:8} : {vide:.1%} des transactions vident le compte émetteur")

    print("\n=== Hypothèse 2 : le montant égale le solde initial ===")
    for nom, jeu in (("Fraude", fraude), ("Normal", normal)):
        egal = (abs(jeu["amount"] - jeu["oldbalanceOrg"]) < 0.01).mean()
        print(f"{nom:8} : {egal:.1%} des montants égalent le solde initial")

    print("\n=== Hypothèse 3 : le solde destinataire reste inchangé ===")
    for nom, jeu in (("Fraude", fraude), ("Normal", normal)):
        fige = ((jeu["oldbalanceDest"] == 0) & (jeu["newbalanceDest"] == 0)).mean()
        print(f"{nom:8} : {fige:.1%} ont un destinataire à solde nul avant et après")

    print("\n=== Montants ===")
    print(
        f"Fraude   : médiane {fraude['amount'].median():,.0f}, "
        f"max {fraude['amount'].max():,.0f}"
    )
    print(
        f"Normal   : médiane {normal['amount'].median():,.0f}, "
        f"max {normal['amount'].max():,.0f}"
    )

    print("\n=== Hypothèse 4 : un transfert suivi d'un retrait ===")
    transferts = set(perimetre.loc[perimetre["type"] == "TRANSFER", "nameDest"])
    retraits = set(perimetre.loc[perimetre["type"] == "CASH_OUT", "nameOrig"])
    chaines = transferts & retraits
    print(f"Comptes recevant un transfert puis effectuant un retrait : {len(chaines):,}")

    print("\n=== Répartition horaire ===")
    heures_fraude = (fraude["step"] % 24).value_counts(normalize=True).sort_index()
    heures_normal = (normal["step"] % 24).value_counts(normalize=True).sort_index()
    creuses = [h for h in range(1, 9)]
    print(f"Fraude   : {heures_fraude.reindex(creuses).sum():.1%} entre 1h et 8h")
    print(f"Normal   : {heures_normal.reindex(creuses).sum():.1%} entre 1h et 8h")

    journal.info("Analyse terminée")


if __name__ == "__main__":
    analyser()
