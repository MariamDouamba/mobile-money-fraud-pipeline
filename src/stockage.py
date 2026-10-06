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


@lru_cache(maxsize=2)
def client(role: str = "ingestion"):
    """Retourne un client S3 pour le rôle demandé.

    Deux rôles sont disponibles :
      - "ingestion" : lecture et écriture des données (usage courant)
      - "admin"     : administration, notamment la création du compartiment

    Le cloisonnement applique le principe du moindre privilège : les scripts
    de traitement n'utilisent jamais d'identité administrateur.
    """
    if role == "admin":
        cle = os.getenv("S3_ADMIN_ACCESS_KEY")
        secret = os.getenv("S3_ADMIN_SECRET_KEY")
    elif role == "ingestion":
        cle = os.getenv("S3_ACCESS_KEY")
        secret = os.getenv("S3_SECRET_KEY")
    else:
        raise ValueError(f"Rôle inconnu : {role}")

    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        aws_access_key_id=cle,
        aws_secret_access_key=secret,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            retries={"max_attempts": 3, "mode": "standard"},
        ),
        region_name="us-east-1",
    )


def compartiment_existe(nom: str = BUCKET, role: str = "ingestion") -> bool:
    """Indique si le compartiment est présent et accessible pour ce rôle."""
    try:
        client(role).head_bucket(Bucket=nom)
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


def systeme_fichiers(role: str = "ingestion"):
    """Retourne un système de fichiers S3 utilisable par pandas et pyarrow."""
    import s3fs

    if role == "admin":
        cle = os.getenv("S3_ADMIN_ACCESS_KEY")
        secret = os.getenv("S3_ADMIN_SECRET_KEY")
    else:
        cle = os.getenv("S3_ACCESS_KEY")
        secret = os.getenv("S3_SECRET_KEY")

    return s3fs.S3FileSystem(
        key=cle,
        secret=secret,
        client_kwargs={"endpoint_url": os.getenv("S3_ENDPOINT")},
        config_kwargs={"signature_version": "s3v4"},
    )
