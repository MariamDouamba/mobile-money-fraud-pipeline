"""Genere le dictionnaire de donnees d'une source depuis le contenu reel de la couche bronze.

Les descriptions metier viennent d'un fichier YAML maintenu a la main.
Les caracteristiques techniques sont mesurees sur les donnees elles-memes,
ce qui interdit au dictionnaire de diverger de la realite.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import yaml
from pyarrow.fs import FSSpecHandler, PyFileSystem

from src.config import RACINE
from src.journal import obtenir_journal
from src.stockage import systeme_fichiers, uri

journal = obtenir_journal("dictionnaire")

DOSSIER = RACINE / "docs" / "dictionnaire"
SEUIL_ENUMERATION = 50

RGPD = {
    "non": "Non personnelle",
    "indirect": "Identifiant indirect",
    "financier": "Donnee financiere rattachable",
}


def espacer(nombre: int) -> str:
    return f"{nombre:,}".replace(",", " ")


def profiler(colonne) -> dict:
    """Mesure une colonne sans la materialiser en objets Python."""
    total = len(colonne)
    nuls = colonne.null_count
    profil = {
        "nuls": nuls,
        "taux_nuls": (nuls / total) if total else 0.0,
        "distincts": pc.count_distinct(colonne).as_py(),
        "etendue": "",
        "valeurs": "",
        "zeros": None,
        "taux_zeros": 0.0,
    }

    if pa.types.is_integer(colonne.type) or pa.types.is_floating(colonne.type):
        zeros = pc.sum(pc.cast(pc.equal(colonne, 0), "int64")).as_py() or 0
        profil["zeros"] = zeros
        profil["taux_zeros"] = (zeros / total) if total else 0.0

    try:
        bornes = pc.min_max(colonne).as_py()
        if bornes["min"] is not None:
            profil["etendue"] = f"{bornes['min']} a {bornes['max']}"
    except Exception:
        pass

    if profil["distincts"] <= SEUIL_ENUMERATION:
        comptes = pc.value_counts(colonne).to_pylist()
        comptes.sort(key=lambda e: e["counts"], reverse=True)
        profil["valeurs"] = ", ".join(
            f"{e['values']} ({espacer(e['counts'])})" for e in comptes[:6]
        )

    return profil


def generer(source: str = "paysim") -> Path:
    descriptif = yaml.safe_load((DOSSIER / f"{source}.yml").read_text(encoding="utf-8"))
    metier = descriptif.get("colonnes", {})

    fs = systeme_fichiers()
    racine_source = uri("bronze", source).removeprefix("s3://")
    partitions = sorted(p for p in fs.ls(racine_source) if "dt=" in p)
    if not partitions:
        raise FileNotFoundError(f"Aucune partition sous s3://{racine_source}")
    chemin = partitions[-1]

    journal.info("Lecture de s3://%s", chemin)
    jeu = ds.dataset(chemin, filesystem=PyFileSystem(FSSpecHandler(fs)), format="parquet")
    total = jeu.count_rows()
    journal.info("%s enregistrements, %d colonnes", espacer(total), len(jeu.schema))

    profils = {}
    for champ in jeu.schema:
        table = jeu.to_table(columns=[champ.name])
        profils[champ.name] = profiler(table.column(0))
        journal.info(
            "  %-16s %-22s %s distincts",
            champ.name,
            str(champ.type),
            espacer(profils[champ.name]["distincts"]),
        )

    horodatage = datetime.now(UTC).strftime("%d/%m/%Y a %H:%M UTC")
    m = [
        f"# Dictionnaire de donnees — {descriptif['libelle']}",
        "",
        "> **Document genere automatiquement — ne pas modifier a la main.**",
        f"> Le sens metier provient de `docs/dictionnaire/{source}.yml`.",
        "> Les caracteristiques techniques sont mesurees sur la couche bronze.",
        "",
        "| | |",
        "|---|---|",
        f"| Origine | {descriptif['origine']} |",
        f"| Granularite | {descriptif['granularite']} |",
        f"| Responsable | {descriptif['responsable']} |",
        f"| Partition analysee | `{chemin}` |",
        f"| Enregistrements | {espacer(total)} |",
        f"| Colonnes | {len(jeu.schema)} |",
        f"| Genere le | {horodatage} |",
        "",
        "## Synthese",
        "",
        "| Colonne | Type | Libelle | Nulles | A zero | Distinctes | RGPD |",
        "|---|---|---|---|---|---|---|",
    ]

    for champ in jeu.schema:
        p = profils[champ.name]
        d = metier.get(champ.name, {})
        zeros = "—" if p["zeros"] is None else f"{espacer(p['zeros'])} ({p['taux_zeros']:.2%})"
        m.append(
            f"| `{champ.name}` | {champ.type} | {d.get('libelle', '—')} | "
            f"{espacer(p['nuls'])} ({p['taux_nuls']:.2%}) | {zeros} | "
            f"{espacer(p['distincts'])} | {RGPD.get(d.get('rgpd', 'non'), '—')} |"
        )

    m += ["", "## Detail par colonne", ""]
    for champ in jeu.schema:
        p = profils[champ.name]
        d = metier.get(champ.name, {})
        m.append(f"### `{champ.name}` — {d.get('libelle', 'Non documentee')}")
        m.append("")
        if d.get("description"):
            m.append(d["description"].strip())
            m.append("")
        m.append(f"- **Type mesure** : `{champ.type}`")
        m.append(
            f"- **Valeurs nulles** : {espacer(p['nuls'])} sur {espacer(total)} ({p['taux_nuls']:.2%})"
        )
        m.append(f"- **Valeurs distinctes** : {espacer(p['distincts'])}")
        if p["zeros"] is not None:
            m.append(f"- **Valeurs a zero** : {espacer(p['zeros'])} ({p['taux_zeros']:.2%})")
        if p["etendue"]:
            m.append(f"- **Etendue** : {p['etendue']}")
        if p["valeurs"]:
            m.append(f"- **Valeurs observees** : {p['valeurs']}")
        if d.get("regle"):
            m.append(f"- **Regle de gestion** : {d['regle'].strip()}")
        m.append(f"- **Classification RGPD** : {RGPD.get(d.get('rgpd', 'non'), '—')}")
        m.append("")

    if descriptif.get("constats"):
        m += ["## Constats de qualite", ""]
        m += [f"- {c.strip()}" for c in descriptif["constats"]]
        m.append("")

    non_documentees = [c.name for c in jeu.schema if c.name not in metier]
    if non_documentees:
        m += ["## Colonnes non documentees", ""]
        m += [f"- `{c}`" for c in non_documentees]
        m.append("")

    destination = DOSSIER / f"{source}.md"
    destination.write_text("\n".join(m), encoding="utf-8")
    journal.info("Dictionnaire ecrit : %s", destination)
    return destination


if __name__ == "__main__":
    generer()
