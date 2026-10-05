"""Tests de l'extracteur PaySim."""

import hashlib

from src.extraction.extraire_paysim import empreinte_fichier


def test_empreinte_est_deterministe(tmp_path):
    """Deux calculs sur le même contenu doivent donner la même empreinte."""
    fichier = tmp_path / "exemple.txt"
    fichier.write_text("contenu de test", encoding="utf-8")

    assert empreinte_fichier(fichier) == empreinte_fichier(fichier)


def test_empreinte_correspond_a_la_reference(tmp_path):
    """L'empreinte doit correspondre au SHA-256 calculé directement."""
    contenu = b"transactions mobile money"
    fichier = tmp_path / "exemple.bin"
    fichier.write_bytes(contenu)

    assert empreinte_fichier(fichier) == hashlib.sha256(contenu).hexdigest()


def test_empreinte_detecte_une_modification(tmp_path):
    """Un seul octet modifié doit changer l'empreinte."""
    fichier = tmp_path / "exemple.txt"

    fichier.write_text("montant: 1000", encoding="utf-8")
    avant = empreinte_fichier(fichier)

    fichier.write_text("montant: 1001", encoding="utf-8")
    apres = empreinte_fichier(fichier)

    assert avant != apres


def test_empreinte_gere_un_fichier_volumineux(tmp_path):
    """La lecture par blocs doit fonctionner au-delà d'un bloc."""
    fichier = tmp_path / "volumineux.bin"
    fichier.write_bytes(b"x" * (3 * 1024 * 1024))  # 3 Mo, soit 3 blocs

    assert len(empreinte_fichier(fichier)) == 64
