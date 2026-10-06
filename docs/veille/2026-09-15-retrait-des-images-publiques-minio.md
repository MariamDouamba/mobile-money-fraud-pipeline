# Retrait des images publiques MinIO des registres de conteneurs

**Date de la fiche** : 15 septembre 2026
**Thème** : chaîne d'approvisionnement logicielle, stockage objet

## Source

Constat direct en tentant un téléchargement d'image, puis recherche
documentaire sur l'état du projet MinIO (dépôt GitHub, annonces de l'éditeur).

## Constat

Les images publiques de MinIO ne sont plus téléchargeables depuis les
registres habituels. Le registre principal refuse l'accès, le registre
alternatif répond une erreur d'autorisation, y compris sur une version
figée. L'édition communautaire n'est désormais distribuée que sous forme de
code source, et le dépôt a été archivé.

## Analyse

Il ne s'agit pas d'un incident passager mais d'un changement de modèle de
distribution de l'éditeur. Le risque est générique et ne concerne pas que
MinIO : toute brique dont la distribution dépend d'un registre public peut
devenir indisponible du jour au lendemain, sans préavis et sans recours.

La dépendance à un registre public est donc un point de fragilité au même
titre qu'une dépendance réseau, et doit être traitée comme tel.

## Impact sur le projet

Le stockage objet est la brique centrale de l'architecture en couches.
Son indisponibilité bloque l'intégralité de la chaîne d'ingestion.

## Décision et action

1. Remplacement par SeaweedFS, consigné dans `docs/adr/0001-choix-du-stockage-objet.md`.
2. Archivage local de l'image retenue (`docker save` vers `docker/images/`),
   de sorte que la plateforme reste démarrable sans accès réseau.
3. Règle retenue pour la suite du projet : toute brique critique voit son
   image archivée localement dès sa validation.

## À surveiller

Évolution du modèle de distribution des autres briques auto-hébergées du
projet, en particulier celles portées par un éditeur commercial.
