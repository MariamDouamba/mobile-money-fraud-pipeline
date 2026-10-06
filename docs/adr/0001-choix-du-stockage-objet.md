# ADR 0001 — Choix du système de stockage objet

- **Date** : 2026-10-06
- **Statut** : accepté
- **Décideur** : équipe data

## Contexte

L'architecture prévoit un lakehouse organisé en trois couches — brute, normalisée,
agrégée — reposant sur un stockage objet compatible avec le protocole S3. Ce choix
de protocole conditionne la portabilité de la plateforme vers un service managé,
puisque le code d'accès reste identique quel que soit le serveur sous-jacent.

Le projet s'exécutant intégralement en local sur un poste unique, le stockage doit
être conteneurisé, de faible empreinte mémoire, et doté d'un mécanisme de droits
permettant de démontrer une gouvernance par groupes.

## Décision initiale et incident rencontré

MinIO avait été retenu dans l'étude technique initiale : implémentation S3 de
référence, console web, système d'habilitations complet.

Lors de la mise en œuvre, le téléchargement de l'image a échoué sur les deux
registres publics. Les vérifications ont établi que l'éditeur a retiré ses images
publiques de Docker Hub en septembre 2026, puis fermé l'accès sur le registre
alternatif. L'édition communautaire n'est plus distribuée que sous forme de code
source.

Le composant retenu est donc devenu indisponible entre la conception et la
réalisation, sans préavis ni version de remplacement.

## Alternatives évaluées

| Solution | API S3 | Gouvernance | Empreinte | Interface | Retenue |
|---|---|---|---|---|---|
| SeaweedFS | Complète | Identités avec droits par action et par compartiment | Faible | Oui | **Oui** |
| Garage | Complète | Clés d'accès par compartiment | Très faible | Non | Non |
| LocalStack | Émulation | Limitée en version gratuite | Moyenne | Non | Non |
| PostgreSQL | Sans objet | Rôles SQL | Faible | Non | Non |

PostgreSQL a été écarté bien qu'il figure déjà dans l'architecture : il porte la
base opérationnelle, non le lac de données. Y stocker les couches du lakehouse
reviendrait à supprimer la dimension data lake de la plateforme.

Garage présente l'empreinte la plus faible mais ne propose pas d'interface
permettant de donner à voir le contenu du stockage et les habilitations.

LocalStack est positionné comme émulateur de test plutôt que comme système de
stockage, et sa gestion fine des droits relève de l'offre payante.

## Décision

**SeaweedFS** est retenu comme système de stockage objet.

Il satisfait les trois critères déterminants : compatibilité S3 assurant la
portabilité, mécanisme d'identités permettant d'attribuer des droits par action et
par compartiment, et interface web rendant le stockage démontrable.

## Conséquences

Positives :

- Le code d'accès au stockage reste inchangé, puisqu'il s'appuie sur l'API S3 et
  non sur une bibliothèque propriétaire. La portabilité vers un service managé est
  préservée.
- La décision est désormais argumentée par une contrainte réelle et documentée,
  et non par un choix par défaut.

Négatives :

- SeaweedFS est moins répandu que MinIO, ce qui peut demander un effort
  d'explication supplémentaire.
- La configuration des identités suit une syntaxe propre à l'outil, qui diffère
  des politiques de MinIO.

## Mesure de réduction du risque

L'incident révèle une dépendance à la disponibilité de registres publics tiers,
que l'épinglage de version ne suffit pas à couvrir : une image retirée du registre
devient inaccessible quelle que soit sa version.

Mesure adoptée : toutes les images utilisées par la plateforme sont archivées
localement au format d'export Docker, dans `docker/images/`, et la procédure de
rechargement est documentée. La plateforme peut ainsi être reconstruite sans accès
réseau, y compris si un éditeur retire ses images.

Ce risque est inscrit à l'analyse de risques du projet.
