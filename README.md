# Plateforme de détection de fraude — transactions mobile money

Projet de certification Data Engineer (RNCP 37638) — session avril 2027.

Plateforme d'ingestion, d'historisation et de mise à disposition des données
de transactions mobile money, destinée à la détection de fraude.

## Prérequis

- Python 3.11
- Docker Desktop (7,5 Go alloués)
- Un compte Kaggle avec un jeton API

## Installation

1. Cloner le dépôt et se placer dedans
2. Créer l'environnement : `python3.11 -m venv .venv`
3. L'activer : `source .venv/bin/activate`
4. Installer les dépendances : `pip install -r requirements.txt`
5. Copier `.env.example` vers `.env` et renseigner les valeurs

## Structure

Voir `docs/architecture.md`.
