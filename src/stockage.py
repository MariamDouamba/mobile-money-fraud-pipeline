"""Accès au stockage objet via le protocole S3.

Le client est construit à partir des variables d'environnement, de sorte que
le même code fonctionne contre un stockage local ou un service managé :
seule l'adresse du point d'accès change.
"""

import os
from functools import lru_cache

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from src.config import RACINE  # noqa: F401 — déclenche le chargement du .env

BUCKET = os.getenv("S3_BUCKET", "lakehouse")

COUCHES = ("bronze", "silver", "gold")


@lru_cache(maxsize=1)
def client():
    """Retourne un client S3 configuré, mis en cache.

    Le cache évite de reconstruire le client à chaque appel : la connexion
    est établie une fois pour la durée du processus.
    """
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
        config=Config(
            signature_version="s3v4",
            # Indispensable hors AWS : sans cela, boto3 préfixerait l'adresse
            # par le nom du compartiment, ce que le serveur local ne gère pas.
            s3={"addressing_style": "path"},
            retries={"max_attempts": 3, "mode": "standard"},
        ),
        region_name="us-east-1",  # valeur de forme, exigée par le protocole
    )


def compartiment_existe(nom: str = BUCKET) -> bool:
    """Indique si le compartiment est présent et accessible."""
    try:
        client().head_bucket(Bucket=nom)
        return True
    except ClientError:
        return False


def chemin(couche: str, *segments: str) -> str:
    """Construit une clé d'objet dans la couche indiquée.

    Exemple : chemin("bronze", "paysim", "fichier.parquet")
              -> "bronze/paysim/fichier.parquet"
    """
    if couche not in COUCHES:
        raise ValueError(f"Couche inconnue : {couche}. Attendu : {COUCHES}")
    return "/".join((couche, *segments))


def uri(couche: str, *segments: str) -> str:
    """Construit une adresse S3 complète, telle que l'attendent Spark et Delta."""
    return f"s3://{BUCKET}/{chemin(couche, *segments)}"
