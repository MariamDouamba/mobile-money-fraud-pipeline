"""Charge le fichier PaySim brut dans la couche bronze du lakehouse.

Principe : lecture par morceaux (le CSV pèse 470 Mo, on ne le charge jamais
entièrement en mémoire), ajout de métadonnées techniques de traçabilité,
écriture en Parquet compressé, partitionné par date d'ingestion.
"""

from __future__ import annotations

import time
from datetime import UTC, datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from src.config import CHEMIN_PAYSIM
from src.journal import obtenir_journal
from src.stockage import systeme_fichiers, uri

journal = obtenir_journal("charger_bronze")

TAILLE_MORCEAU = 1_000_000
SOURCE = "paysim"


def charger() -> None:
    fichier = CHEMIN_PAYSIM
    if not fichier.exists():
        raise FileNotFoundError(
            f"Fichier source absent : {fichier}. "
            "Lance d'abord python -m src.extraction.extraire_paysim"
        )

    fs = systeme_fichiers()

    maintenant = datetime.now(UTC)
    lot = maintenant.strftime("%Y%m%dT%H%M%SZ")
    jour = maintenant.strftime("%Y-%m-%d")
    prefixe = uri("bronze", SOURCE, f"dt={jour}").removeprefix("s3://")

    if fs.exists(prefixe) and fs.ls(prefixe):
        journal.info("Partition %s deja presente, rien a faire (idempotence)", prefixe)
        return

    journal.info("Chargement de %s vers s3://%s", fichier.name, prefixe)
    debut = time.perf_counter()
    lignes = 0
    octets = 0

    lecteur = pd.read_csv(fichier, chunksize=TAILLE_MORCEAU)
    for numero, morceau in enumerate(lecteur, start=1):
        morceau["_source"] = SOURCE
        morceau["_lot"] = lot
        morceau["_ingere_le"] = maintenant

        table = pa.Table.from_pandas(morceau, preserve_index=False)
        cible = f"{prefixe}/partie-{numero:04d}.parquet"
        with fs.open(cible, "wb") as flux:
            pq.write_table(table, flux, compression="snappy")

        taille = fs.info(cible)["size"]
        lignes += len(morceau)
        octets += taille
        journal.info(
            "Morceau %d : %s lignes, %.1f Mo ecrits",
            numero,
            f"{len(morceau):,}".replace(",", " "),
            taille / 1024**2,
        )

    duree = time.perf_counter() - debut
    source_mo = fichier.stat().st_size / 1024**2
    cible_mo = octets / 1024**2
    journal.info(
        "Termine : %s lignes en %.1f s | CSV %.1f Mo -> Parquet %.1f Mo (%.0f %% de gain)",
        f"{lignes:,}".replace(",", " "),
        duree,
        source_mo,
        cible_mo,
        (1 - cible_mo / source_mo) * 100,
    )


if __name__ == "__main__":
    charger()
