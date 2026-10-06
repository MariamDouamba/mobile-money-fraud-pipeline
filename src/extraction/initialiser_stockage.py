"""Initialisation du lakehouse dans le stockage objet.

Crée le compartiment et les trois couches de l'architecture médaillon.
Le script est idempotent : il peut être relancé sans effet de bord.

Exécution :
    python -m src.extraction.initialiser_stockage
"""

import sys

from botocore.exceptions import ClientError

from src.journal import obtenir_journal
from src.stockage import BUCKET, COUCHES, client, compartiment_existe

journal = obtenir_journal("initialisation_stockage")


def initialiser() -> None:
    s3 = client()

    if compartiment_existe():
        journal.info("Compartiment '%s' déjà présent", BUCKET)
    else:
        s3.create_bucket(Bucket=BUCKET)
        journal.info("Compartiment '%s' créé", BUCKET)

    # Le stockage objet n'a pas de dossiers : on matérialise chaque couche
    # par un objet marqueur, ce qui la rend visible dans l'interface.
    for couche in COUCHES:
        cle = f"{couche}/.couche"
        try:
            s3.head_object(Bucket=BUCKET, Key=cle)
            journal.info("Couche '%s' déjà initialisée", couche)
        except ClientError:
            s3.put_object(
                Bucket=BUCKET,
                Key=cle,
                Body=f"Couche {couche} du lakehouse\n".encode(),
            )
            journal.info("Couche '%s' initialisée", couche)

    contenu = s3.list_objects_v2(Bucket=BUCKET)
    journal.info("Compartiment '%s' : %d objet(s)", BUCKET, contenu.get("KeyCount", 0))


if __name__ == "__main__":
    try:
        initialiser()
    except Exception as erreur:  # noqa: BLE001
        journal.error("Initialisation en échec : %s", erreur)
        sys.exit(1)
