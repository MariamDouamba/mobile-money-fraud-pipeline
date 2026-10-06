# Registre des captures d'écran

Les captures constituent les preuves d'exécution exigées par le référentiel.
Elles sont produites au fil de la réalisation, jamais reconstituées après coup.

## Convention de nommage

`<epreuve>-<objet>.png` — exemple : `e7-stockage-cluster.png`

## Captures réalisées

| Fichier | Objet | Épreuve | Critère | Date |
|---|---|---|---|---|
| `e4-extraction-paysim.png` | Extraction Kaggle : journal, progression, empreinte | E4 | C8 | 2026-10-05 |
| `e4-extraction-idempotence.png` | Second lancement : téléchargement ignoré | E4 | C8 | 2026-10-05 |
| `e4-tests-unitaires.png` | Dix tests au vert en local | E4 | — | 2026-10-05 |
| `e4-ci-github-actions.png` | Trois travaux de la CI au vert | E4 | — | 2026-10-05 |
| `e4-depot-github.png` | Dépôt public, arborescence, Release | E4 | C8, C11 | 2026-10-05 |
| `e7-stockage-cluster.png` | État du cluster de stockage, topologie, volumes | E7 | C19 | 2026-10-06 |
| `e7-stockage-filer.png` | Interface de navigation du stockage objet | E7 | C19 | 2026-10-06 |

## Captures restant à produire

| Objet attendu | Épreuve | Critère |
|---|---|---|
| Lakehouse : les trois couches visibles dans le stockage | E7 | C19, C20 |
| Base opérationnelle : schémas et tables | E4 | C11 |
| Modèle conceptuel, logique et physique en formalisme MERISE | E4 | C11 |
| Interface d'orchestration : vue des chaînes de traitement | E5 | C15 |
| Exécution d'une chaîne complète, étapes au vert | E5 | C15 |
| Documentation générée des transformations | E5 | C15 |
| Interface programmable : spécification des points d'entrée | E4 | C12 |
| Deux appels avec deux rôles aux droits distincts | E4 | C12 |
| Entrepôt : modèle dimensionnel et requête d'analyse | E5 | C13, C14 |
| Historisation d'une dimension : lignes avant et après | E6 | C17 |
| Journalisation : alertes et erreurs catégorisées | E6 | C16 |
| Alerte reçue par messagerie après un incident simulé | E6 | C16 |
| Sauvegarde planifiée et restauration vérifiée | E6 | C16 |
| Tableau de bord des indicateurs de service | E6 | C16 |
| Flux d'événements : production et consommation | E7 | C19 |
| Catalogue de données : métadonnées et lignage | E7 | C20 |
| Supervision : indicateurs système et alerte sur rupture | E7 | C20 |
| Habilitations par groupes, trois paramétrages distincts | E7 | C21 |
| Démonstration d'un refus d'accès lié aux droits | E7 | C21 |
| Portabilité : une table lue depuis une plateforme managée | E2, E7 | C3, C18 |

## Règle

Toute capture est prise **au moment où le composant fonctionne pour la première
fois**. Reconstituer une capture en fin de projet suppose de relancer l'ensemble
de la plateforme, ce qui est coûteux et rarement fidèle.
