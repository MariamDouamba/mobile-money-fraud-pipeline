"""Tests de la journalisation."""

import logging

from src.journal import obtenir_journal


def test_journal_est_configure():
    """Le journal doit écrire à la fois en console et en fichier."""
    journal = obtenir_journal("test_unitaire")

    assert journal.level == logging.INFO
    types = {type(gestionnaire).__name__ for gestionnaire in journal.handlers}
    assert "StreamHandler" in types
    assert "FileHandler" in types


def test_journal_ne_duplique_pas_les_gestionnaires():
    """Deux appels successifs ne doivent pas doubler les sorties."""
    premier = obtenir_journal("test_duplication")
    nombre = len(premier.handlers)

    second = obtenir_journal("test_duplication")

    assert len(second.handlers) == nombre
