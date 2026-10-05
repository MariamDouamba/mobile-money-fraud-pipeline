"""Tests de la configuration du projet."""

import os
from unittest.mock import patch

import pytest

from src.config import DATA_RAW, LOGS, RACINE, verifier_identifiants_kaggle


def test_racine_contient_le_projet():
    """La racine calculée doit contenir les dossiers attendus."""
    assert (RACINE / "src").is_dir()
    assert (RACINE / "docs").is_dir()


def test_chemins_sous_la_racine():
    """Aucun chemin ne doit sortir du projet — pas de chemin absolu en dur."""
    assert DATA_RAW.is_relative_to(RACINE)
    assert LOGS.is_relative_to(RACINE)


def test_identifiants_manquants_leve_une_erreur():
    """L'absence d'identifiants doit échouer tôt, avec un message explicite."""
    with patch.dict(os.environ, {"KAGGLE_USERNAME": "", "KAGGLE_KEY": ""}, clear=False):
        with pytest.raises(RuntimeError, match="Identifiants Kaggle absents"):
            verifier_identifiants_kaggle()


def test_identifiants_presents_passent():
    """Des identifiants renseignés ne doivent lever aucune erreur."""
    with patch.dict(
        os.environ,
        {"KAGGLE_USERNAME": "utilisateur", "KAGGLE_KEY": "cle"},
        clear=False,
    ):
        verifier_identifiants_kaggle()
