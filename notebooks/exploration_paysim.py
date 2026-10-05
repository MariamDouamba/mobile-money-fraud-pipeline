import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Exploration des transactions mobile money

    Analyse exploratoire du jeu PaySim, préalable à la conception du moteur
    de détection et du modèle dimensionnel.

    **Source** : API Kaggle (`ealaxi/paysim1`)
    **Périmètre** : échantillon stratifié — toutes les fraudes, 300 000 transactions normales
    **Finalité** : comprendre la structure de la donnée et fonder les règles de détection sur des faits mesurés

    Les figures produites ici alimentent la topographie des données (E2) et la
    justification des règles (E4).
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    # Chemins : le notebook vit dans notebooks/, la racine est un niveau au-dessus
    RACINE = Path(__file__).resolve().parent.parent
    ECHANTILLON = RACINE / "data" / "interim" / "paysim_echantillon.parquet"
    FIGURES = RACINE / "docs" / "figures"
    FIGURES.mkdir(parents=True, exist_ok=True)

    # Charte graphique commune à toutes les figures du projet
    INDIGO = "#534AB7"
    TEAL = "#0F6E56"
    AMBRE = "#C2660A"
    GRIS = "#6B7275"

    sns.set_theme(style="whitegrid", font_scale=0.95)
    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["savefig.dpi"] = 200
    plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["axes.edgecolor"] = "#C9C7BF"

    def enregistrer(figure, nom):
        """Enregistre une figure dans docs/figures pour réutilisation en rapport."""
        chemin = FIGURES / f"{nom}.png"
        figure.savefig(chemin, facecolor="white")
        return chemin

    return (
        AMBRE,
        ECHANTILLON,
        FIGURES,
        GRIS,
        INDIGO,
        TEAL,
        enregistrer,
        pd,
        plt,
        sns,
    )


@app.cell
def _(ECHANTILLON, pd):
    donnees = pd.read_parquet(ECHANTILLON)
    donnees.shape
    return (donnees,)


@app.cell
def _(mo):
    mo.md("""
    ## 1. Structure et aperçu du jeu de données
    """)
    return


@app.cell
def _(donnees):
    donnees.head(20)
    return


@app.cell
def _(donnees, pd):
    structure = pd.DataFrame(
        {
            "type": donnees.dtypes.astype(str),
            "manquantes": donnees.isna().sum(),
            "distinctes": donnees.nunique(),
        }
    )
    structure
    return


@app.cell
def _(mo):
    mo.md("""
    ### Signification des colonnes

    | Colonne | Signification |
    |---|---|
    | `step` | Pas de temps simulé — 1 pas équivaut à 1 heure |
    | `type` | Type d'opération : CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER |
    | `amount` | Montant de l'opération |
    | `nameOrig` | Identifiant du compte émetteur |
    | `oldbalanceOrg` / `newbalanceOrig` | Solde de l'émetteur avant et après l'opération |
    | `nameDest` | Identifiant du compte destinataire — un préfixe M désigne un marchand |
    | `oldbalanceDest` / `newbalanceDest` | Solde du destinataire avant et après |
    | `isFraud` | Vérité terrain : l'opération est frauduleuse |
    | `isFlaggedFraud` | Signalement produit par le dispositif existant |
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 2. Répartition des types d'opération
    """)
    return


@app.cell
def _(INDIGO, TEAL, donnees, enregistrer, plt):
    fig_types, axes_types = plt.subplots(1, 2, figsize=(11, 4))

    repartition = donnees["type"].value_counts()
    axes_types[0].barh(repartition.index, repartition.values, color=INDIGO)
    axes_types[0].set_title("Volume par type d'opération", loc="left", fontweight="bold")
    axes_types[0].set_xlabel("Nombre de transactions")

    taux = (
        donnees.groupby("type")["isFraud"].mean().sort_values(ascending=True) * 100
    )
    couleurs = [TEAL if valeur > 0 else "#D5D3CC" for valeur in taux.values]
    axes_types[1].barh(taux.index, taux.values, color=couleurs)
    axes_types[1].set_title(
        "Taux de fraude par type (%)", loc="left", fontweight="bold"
    )
    axes_types[1].set_xlabel("Part de transactions frauduleuses")

    fig_types.tight_layout()
    enregistrer(fig_types, "repartition_types_operation")
    fig_types
    return


@app.cell
def _(mo):
    mo.md("""
    **Lecture** : la fraude est strictement absente de CASH_IN, DEBIT et PAYMENT.
    Elle se concentre sur TRANSFER et CASH_OUT, ce qui correspond au schéma de
    détournement : transférer les fonds vers un compte contrôlé, puis les retirer
    en espèces.

    **Conséquence pour le projet** : le périmètre de surveillance se limite à ces
    deux types d'opération, et cette restriction est justifiée par la donnée.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 3. La règle décisive — montant égal au solde initial
    """)
    return


@app.cell
def _(donnees):
    perimetre = donnees[donnees["type"].isin(["TRANSFER", "CASH_OUT"])].copy()
    perimetre["montant_egal_solde"] = (
        (perimetre["amount"] - perimetre["oldbalanceOrg"]).abs() < 0.01
    )
    perimetre["compte_vide"] = (
        (perimetre["newbalanceOrig"] == 0) & (perimetre["oldbalanceOrg"] > 0)
    )
    perimetre["dest_solde_nul"] = (
        (perimetre["oldbalanceDest"] == 0) & (perimetre["newbalanceDest"] == 0)
    )
    perimetre["heure"] = perimetre["step"] % 24
    perimetre["nocturne"] = perimetre["heure"].between(1, 8)
    len(perimetre)
    return (perimetre,)


@app.cell
def _(AMBRE, GRIS, enregistrer, perimetre, plt):
    criteres = [
        ("montant_egal_solde", "Montant égal\nau solde initial"),
        ("compte_vide", "Compte émetteur\nvidé"),
        ("dest_solde_nul", "Destinataire\nà solde nul"),
        ("nocturne", "Opération\nnocturne (1h-8h)"),
    ]

    fraude = perimetre[perimetre["isFraud"] == 1]
    normal = perimetre[perimetre["isFraud"] == 0]

    valeurs_fraude = [fraude[colonne].mean() * 100 for colonne, _ in criteres]
    valeurs_normal = [normal[colonne].mean() * 100 for colonne, _ in criteres]
    etiquettes = [libelle for _, libelle in criteres]

    fig_regles, axe_regles = plt.subplots(figsize=(9, 4.5))
    positions = range(len(criteres))
    largeur = 0.38

    axe_regles.bar(
        [p - largeur / 2 for p in positions], valeurs_fraude,
        largeur, label="Transactions frauduleuses", color=AMBRE,
    )
    axe_regles.bar(
        [p + largeur / 2 for p in positions], valeurs_normal,
        largeur, label="Transactions normales", color=GRIS, alpha=0.6,
    )

    for position, (val_f, val_n) in enumerate(zip(valeurs_fraude, valeurs_normal)):
        axe_regles.text(position - largeur / 2, val_f + 2, f"{val_f:.1f}",
                        ha="center", fontsize=9, fontweight="bold", color=AMBRE)
        axe_regles.text(position + largeur / 2, val_n + 2, f"{val_n:.1f}",
                        ha="center", fontsize=9, color=GRIS)

    axe_regles.set_xticks(list(positions))
    axe_regles.set_xticklabels(etiquettes)
    axe_regles.set_ylabel("Part des transactions (%)")
    axe_regles.set_title(
        "Pouvoir discriminant des critères de détection",
        loc="left", fontweight="bold",
    )
    axe_regles.legend(frameon=False)
    axe_regles.set_ylim(0, 110)

    fig_regles.tight_layout()
    enregistrer(fig_regles, "pouvoir_discriminant_regles")
    fig_regles
    return fraude, normal


@app.cell
def _(mo):
    mo.md("""
    **Lecture** : le critère « montant égal au solde initial » sépare presque
    parfaitement les deux populations. Le critère « compte vidé », pourtant
    proche en apparence, concerne aussi 42,7 % des transactions normales : utilisé
    seul, il produirait un volume considérable de faux positifs.

    **Conséquence pour le projet** : la règle principale du moteur repose sur le
    premier critère ; les trois autres interviennent comme critères de
    renforcement du score, non comme déclencheurs autonomes.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 4. Distribution des montants
    """)
    return


@app.cell
def _(AMBRE, GRIS, enregistrer, fraude, normal, plt):
    import numpy as np

    fig_montants, axes_montants = plt.subplots(1, 2, figsize=(11, 4))

    # Échelle logarithmique : les montants s'étendent sur plusieurs ordres de grandeur
    axes_montants[0].hist(
        np.log10(normal["amount"].clip(lower=1)), bins=60,
        color=GRIS, alpha=0.6, label="Normales", density=True,
    )
    axes_montants[0].hist(
        np.log10(fraude["amount"].clip(lower=1)), bins=60,
        color=AMBRE, alpha=0.7, label="Frauduleuses", density=True,
    )
    axes_montants[0].set_xlabel("Montant (log10)")
    axes_montants[0].set_ylabel("Densité")
    axes_montants[0].set_title(
        "Distribution des montants", loc="left", fontweight="bold"
    )
    axes_montants[0].legend(frameon=False)

    donnees_boite = [normal["amount"], fraude["amount"]]
    boites = axes_montants[1].boxplot(
        donnees_boite, tick_labels=["Normales", "Frauduleuses"],
        patch_artist=True, showfliers=False,
    )
    for boite, couleur in zip(boites["boxes"], [GRIS, AMBRE]):
        boite.set_facecolor(couleur)
        boite.set_alpha(0.7)
    axes_montants[1].set_ylabel("Montant")
    axes_montants[1].set_title(
        "Dispersion des montants", loc="left", fontweight="bold"
    )

    fig_montants.tight_layout()
    enregistrer(fig_montants, "distribution_montants")
    fig_montants
    return


@app.cell
def _(mo):
    mo.md("""
    ## 5. Profil horaire
    """)
    return


@app.cell
def _(AMBRE, GRIS, enregistrer, fraude, normal, plt):
    fig_heures, axe_heures = plt.subplots(figsize=(10, 4))

    part_fraude = (
        fraude["heure"].value_counts(normalize=True).sort_index() * 100
    )
    part_normal = (
        normal["heure"].value_counts(normalize=True).sort_index() * 100
    )

    axe_heures.plot(
        part_normal.index, part_normal.values,
        marker="o", markersize=4, color=GRIS, label="Normales",
    )
    axe_heures.plot(
        part_fraude.index, part_fraude.values,
        marker="o", markersize=4, color=AMBRE, label="Frauduleuses", linewidth=2,
    )
    axe_heures.axvspan(1, 8, color=AMBRE, alpha=0.08)
    axe_heures.text(4.5, axe_heures.get_ylim()[1] * 0.92, "Heures creuses",
                    ha="center", fontsize=9, color=AMBRE, style="italic")
    axe_heures.set_xlabel("Heure de la journée")
    axe_heures.set_ylabel("Part des transactions (%)")
    axe_heures.set_title(
        "Répartition horaire des transactions", loc="left", fontweight="bold"
    )
    axe_heures.set_xticks(range(0, 24, 2))
    axe_heures.legend(frameon=False)

    fig_heures.tight_layout()
    enregistrer(fig_heures, "profil_horaire")
    fig_heures
    return


@app.cell
def _(mo):
    mo.md("""
    **Lecture** : l'activité normale s'effondre entre 1h et 8h, alors que la fraude
    s'y maintient. Ce contraste fait de l'heure un critère de renforcement utile,
    même s'il ne suffit pas à lui seul.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 6. Comptes destinataires
    """)
    return


@app.cell
def _(donnees, pd):
    # Les émetteurs n'apparaissent qu'une fois ; les destinataires sont réutilisés
    recurrence = pd.DataFrame(
        {
            "emetteurs_distincts": [donnees["nameOrig"].nunique()],
            "destinataires_distincts": [donnees["nameDest"].nunique()],
            "transactions": [len(donnees)],
        }
    )
    recurrence
    return


@app.cell
def _(fraude):
    # Comptes destinataires impliqués dans plusieurs fraudes : comptes collecteurs
    collecteurs = (
        fraude["nameDest"].value_counts().head(15).rename("fraudes_recues")
    )
    collecteurs.to_frame()
    return


@app.cell
def _(mo):
    mo.md("""
    **Lecture** : chaque émetteur n'apparaît pratiquement qu'une fois, ce qui rend
    inopérant tout profilage comportemental côté émetteur. Les destinataires, eux,
    sont réutilisés — l'analyse des comptes receveurs est donc la piste pertinente.

    **Conséquence pour le projet** : les agrégats de la couche gold portent sur les
    comptes destinataires, pas sur les émetteurs.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 7. Corrélations entre variables numériques
    """)
    return


@app.cell
def _(enregistrer, perimetre, plt, sns):
    colonnes_numeriques = [
        "amount", "oldbalanceOrg", "newbalanceOrig",
        "oldbalanceDest", "newbalanceDest", "isFraud",
    ]
    matrice = perimetre[colonnes_numeriques].corr()

    fig_corr, axe_corr = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(
        matrice, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
        vmin=-1, vmax=1, linewidths=0.5, ax=axe_corr,
        cbar_kws={"shrink": 0.8},
    )
    axe_corr.set_title(
        "Corrélations sur le périmètre TRANSFER et CASH_OUT",
        loc="left", fontweight="bold",
    )

    fig_corr.tight_layout()
    enregistrer(fig_corr, "matrice_correlations")
    fig_corr
    return


@app.cell
def _(mo):
    mo.md("""
    ## 8. Anomalies de qualité à traiter
    """)
    return


@app.cell
def _(donnees, pd):
    anomalies = pd.DataFrame(
        {
            "contrôle": [
                "Montant nul",
                "Solde émetteur négatif",
                "Solde destinataire négatif",
                "Destinataire marchand (préfixe M)",
                "Incohérence de solde émetteur",
            ],
            "occurrences": [
                int((donnees["amount"] == 0).sum()),
                int((donnees["oldbalanceOrg"] < 0).sum()),
                int((donnees["oldbalanceDest"] < 0).sum()),
                int(donnees["nameDest"].str.startswith("M").sum()),
                int(
                    (
                        (donnees["oldbalanceOrg"] - donnees["amount"]
                         - donnees["newbalanceOrig"]).abs() > 0.01
                    ).sum()
                ),
            ],
        }
    )
    anomalies["part"] = (anomalies["occurrences"] / len(donnees) * 100).round(2)
    anomalies
    return


@app.cell
def _(mo):
    mo.md("""
    **Conséquence pour le projet** : ces contrôles deviennent les règles de qualité
    appliquées à l'entrée de la couche normalisée. Les lignes en anomalie sont
    journalisées et orientées vers une file dédiée plutôt que rejetées silencieusement.
    """)
    return


@app.cell
def _(FIGURES, mo):
    mo.md(f"""
    ## Figures produites

    Les figures sont enregistrées dans `{FIGURES.name}/` et réutilisées
    dans les rapports de certification :

    - `repartition_types_operation.png` — topographie des données (E2)
    - `pouvoir_discriminant_regles.png` — justification des règles (E4)
    - `distribution_montants.png` — caractérisation des données (E2)
    - `profil_horaire.png` — critère de renforcement (E4)
    - `matrice_correlations.png` — analyse exploratoire (E4)
    """)
    return


if __name__ == "__main__":
    app.run()
