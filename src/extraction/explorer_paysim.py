"""Exploration initiale du jeu de données PaySim.

Produit un profil du fichier brut : volumétrie, types, valeurs manquantes,
distribution des opérations et des cas de fraude.

Le résultat alimente le dictionnaire de données et la topographie du projet.

Exécution :
    python -m src.extraction.explorer_paysim
"""

import pandas as pd

from src.config import DATA_RAW, FICHIER_PAYSIM, RACINE
from src.journal import obtenir_journal

journal = obtenir_journal("exploration_paysim")

SOURCE = DATA_RAW / "paysim" / FICHIER_PAYSIM
RAPPORT = RACINE / "docs" / "profil_paysim.md"


def explorer() -> None:
    journal.info("Lecture du fichier source")
    donnees = pd.read_csv(SOURCE)

    lignes, colonnes = donnees.shape
    journal.info("%s lignes, %s colonnes", f"{lignes:,}".replace(",", " "), colonnes)

    sections: list[str] = ["# Profil du jeu de données PaySim\n"]
    sections.append(
        f"Source : API Kaggle (`ealaxi/paysim1`)  \n"
        f"Fichier : `{FICHIER_PAYSIM}`  \n"
        f"Volumétrie : {lignes:,} lignes, {colonnes} colonnes\n".replace(",", " ")
    )

    # Structure des colonnes
    sections.append("\n## Colonnes\n")
    sections.append("| Colonne | Type | Valeurs manquantes | Valeurs distinctes |")
    sections.append("|---|---|---|---|")
    for colonne in donnees.columns:
        sections.append(
            f"| `{colonne}` | {donnees[colonne].dtype} | "
            f"{donnees[colonne].isna().sum()} | "
            f"{donnees[colonne].nunique():,} |".replace(",", " ")
        )

    # Répartition par type d'opération
    sections.append("\n## Types d'opération\n")
    sections.append("| Type | Nombre | Part |")
    sections.append("|---|---|---|")
    for operation, nombre in donnees["type"].value_counts().items():
        part = nombre / lignes * 100
        sections.append(f"| {operation} | {nombre:,} | {part:.1f} % |".replace(",", " "))

    # Fraude
    fraudes = int(donnees["isFraud"].sum())
    taux = fraudes / lignes * 100
    sections.append("\n## Fraude\n")
    sections.append(
        f"- Transactions frauduleuses : **{fraudes:,}** sur {lignes:,} "
        f"(**{taux:.3f} %**)".replace(",", " ")
    )
    signalees = (
        int(donnees["isFlaggedFlagged"].sum())
        if "isFlaggedFlagged" in donnees
        else int(donnees["isFlaggedFraud"].sum())
    )
    sections.append(f"- Transactions signalées par le système existant : {signalees}")

    sections.append("\n### Fraude par type d'opération\n")
    sections.append("| Type | Transactions | Fraudes | Taux |")
    sections.append("|---|---|---|---|")
    par_type = donnees.groupby("type")["isFraud"].agg(["count", "sum"])
    for operation, ligne in par_type.iterrows():
        taux_type = ligne["sum"] / ligne["count"] * 100
        sections.append(
            f"| {operation} | {int(ligne['count']):,} | {int(ligne['sum']):,} | "
            f"{taux_type:.3f} % |".replace(",", " ")
        )

    # Montants
    sections.append("\n## Montants\n")
    montants = donnees["amount"].describe()
    sections.append("| Statistique | Valeur |")
    sections.append("|---|---|")
    for cle in ("min", "25%", "50%", "75%", "max", "mean"):
        sections.append(f"| {cle} | {montants[cle]:,.2f} |".replace(",", " "))

    # Dimension temporelle
    sections.append("\n## Dimension temporelle\n")
    pas = donnees["step"]
    sections.append(
        f"- Pas de temps : de {pas.min()} à {pas.max()} "
        f"(1 pas = 1 heure, soit {pas.max() / 24:.0f} jours simulés)"
    )

    # Parties impliquées
    sections.append("\n## Parties impliquées\n")
    marchands = donnees["nameDest"].str.startswith("M").sum()
    sections.append(f"- Émetteurs distincts : {donnees['nameOrig'].nunique():,}".replace(",", " "))
    sections.append(
        f"- Destinataires distincts : {donnees['nameDest'].nunique():,}".replace(",", " ")
    )
    sections.append(
        f"- Opérations vers un marchand (préfixe M) : {marchands:,} "
        f"({marchands / lignes * 100:.1f} %)".replace(",", " ")
    )

    RAPPORT.write_text("\n".join(sections) + "\n", encoding="utf-8")
    journal.info("Profil écrit dans %s", RAPPORT.relative_to(RACINE))


if __name__ == "__main__":
    explorer()
