# Registre des captures d'écran

Chaque capture est une **preuve** rattachée à une exigence précise du règlement de certification.
Une capture qui ne prouve rien n'a pas sa place ici.

**Mise à jour** : 8 octobre 2026 — 7 captures réalisées, 29 restantes.

---

## Règles de prise de vue

| Règle | Pourquoi |
|---|---|
| **Jamais de secret à l'écran** | ne jamais capturer `.env`, `s3.json`, un jeton ou une clé d'accès. Vérifier l'image avant de l'enregistrer |
| **Horodatage visible** | les journaux affichent la date et l'heure : les laisser dans le cadre prouve la chronologie du projet |
| **Cadrage serré** | la fenêtre concernée, pas tout l'écran. Un bureau encombré rend la preuve illisible |
| **Texte lisible à l'impression** | agrandir la police du terminal avant la capture ; un rapport imprimé en noir et blanc doit rester déchiffrable |
| **Avant / après quand c'est pertinent** | deux exécutions successives prouvent l'idempotence ; un refus d'accès prouve le cloisonnement |
| **Format PNG** | pas de JPEG sur du texte, qui crée des artefacts autour des caractères |

**Nommage** : `<epreuve>-<sujet>-<precision>.png`, en minuscules, sans accent.

---

## E7 — Data lake (C18 à C21)

> *« présenter la documentation de la procédure d'installation du système de stockage »*
> *« tester la procédure d'installation dans un environnement de développement »*
> *« faire une démonstration du monitorage du système de stockage »*

| Capture | Ce qu'elle prouve | État |
|---|---|---|
| `e7-stockage-cluster.png` | le service de stockage démarré, état du cluster | ✅ |
| `e7-stockage-filer.png` | l'interface de navigation dans le stockage | ✅ |
| `e7-lakehouse-couches.png` | les trois couches créées | ✅ |
| `e7-lakehouse-couches-visuelles.png` | les couches dans l'interface | ✅ |
| `e7-bronze-chargement.png` | le chargement des 7 morceaux et son bilan | ✅ |
| `e7-bronze-idempotence.png` | deux exécutions successives, la seconde sans effet | ✅ |
| `e7-bronze-filer.png` | les fichiers Parquet dans la partition | ✅ |
| `e7-dictionnaire-synthese.png` | le dictionnaire généré, colonnes « Nulles » et « À zéro » | ⬜ |
| `e7-moindre-privilege-refus.png` | l'`AccessDenied` de l'identité d'ingestion sur une création de compartiment | ⬜ |
| `e7-empreinte-reproductible.png` | deux extractions, même empreinte SHA-256 | ⬜ |
| `e7-installation-rejouee.png` | la procédure d'installation rejouée depuis zéro, conteneurs détruits puis recréés | ⬜ |
| `e7-image-archivee.png` | `docker load` depuis l'archive locale, sans réseau | ⬜ |
| `e7-catalogue-connecte.png` | le catalogue relié au système de stockage | ⬜ |
| `e7-catalogue-lignage.png` | le lignage d'une table affiché dans le catalogue | ⬜ |
| `e7-catalogue-metadonnees.png` | les métadonnées mises à jour après une alimentation | ⬜ |
| `e7-batch-programme.png` | l'exécution du programme d'alimentation par lots | ⬜ |
| `e7-tempsreel-programme.png` | l'exécution du programme d'alimentation en continu | ⬜ |
| `e7-monitorage-espace.png` | espace disque, mémoire, état des services | ⬜ |
| `e7-droits-alimentation.png` | le paramétrage des droits d'écriture | ⬜ |
| `e7-droits-acces.png` | le paramétrage des droits de lecture et de recherche | ⬜ |
| `e7-cycle-vie-purge.png` | l'exécution de la purge selon la durée de conservation | ⬜ |
| `e7-ports-locaux.png` | les ports du stockage liés à `127.0.0.1` et non à toutes les interfaces | ⬜ |

---

## E4 — Collecte, base de données et API (C8 à C12)

> *« faire une démonstration des appels à l'API développée, avec un client http (Postman par exemple),
> illustrant les différentes règles d'accès aux données »*

| Capture | Ce qu'elle prouve | État |
|---|---|---|
| `e4-extraction-fichier.png` | le script d'extraction du fichier de transactions | ⬜ |
| `e4-extraction-base.png` | la collecte depuis la base relationnelle source | ⬜ |
| `e4-extraction-api.png` | l'appel au service web des taux et plafonds | ⬜ |
| `e4-extraction-scraping.png` | la collecte des pages réglementaires | ⬜ |
| `e4-sgbd-installation.png` | l'installation du système de base de données | ⬜ |
| `e4-sgbd-schema.png` | les tables créées avec leurs contraintes | ⬜ |
| `e4-import-execution.png` | l'exécution du script d'import en base | ⬜ |
| `e4-requetes-sql.png` | les requêtes d'extraction et leurs résultats | ⬜ |
| `e4-api-documentation.png` | la documentation interactive de l'API | ⬜ |
| `e4-api-appel-autorise.png` | un appel réussi avec un profil autorisé | ⬜ |
| `e4-api-appel-refuse.png` | **le même appel refusé** avec un profil non autorisé | ⬜ |
| `e4-modeles-donnees.png` | les modèles conceptuel, logique et physique | ⬜ |

La paire **appel autorisé / appel refusé** est la plus importante de cette épreuve : le règlement demande
explicitement d'illustrer *les différentes règles d'accès*. Un seul appel réussi ne le démontre pas.

---

## E5 — Entrepôt de données (C13 à C15)

| Capture | Ce qu'elle prouve | État |
|---|---|---|
| `e5-modele-etoile.png` | le schéma en étoile : faits et dimensions | ⬜ |
| `e5-entrepot-tables.png` | les tables de l'entrepôt créées | ⬜ |
| `e5-datamart.png` | un datamart alimenté | ⬜ |
| `e5-etl-execution.png` | l'exécution des traitements de transformation | ⬜ |
| `e5-tests-qualite.png` | les résultats de la phase de test | ⬜ |
| `e5-acces-analystes.png` | les rôles de lecture configurés pour l'équipe d'analyse | ⬜ |

---

## E6 — Maintien en conditions opérationnelles (C16, C17)

> *« modéliser les variations de dimension (type 1, 2 ou 3 de Ralph Kimball) »*
> *« mettre en place la procédure de backup complet et partiel »*

| Capture | Ce qu'elle prouve | État |
|---|---|---|
| `e6-journalisation-alertes.png` | les alertes et erreurs journalisées en exploitation | ⬜ |
| `e6-sauvegarde-complete.png` | l'exécution d'une sauvegarde complète | ⬜ |
| `e6-sauvegarde-partielle.png` | l'exécution d'une sauvegarde partielle | ⬜ |
| `e6-restauration-testee.png` | **la restauration effectivement rejouée**, pas seulement décrite | ⬜ |
| `e6-source-ajoutee.png` | l'intégration d'une nouvelle source à l'entrepôt | ⬜ |
| `e6-scd-historique.png` | une dimension à variation lente conservant son historique | ⬜ |
| `e6-suivi-maintenance.png` | l'outil de suivi des tâches de maintenance | ⬜ |

La capture `e6-restauration-testee.png` est celle qu'aucun candidat ne pense à faire. Le règlement
distingue pourtant « mettre en place la procédure » de sa simple description : rejouer une restauration
et la capturer vaut mieux qu'une page de documentation.

---

### Captures transverses

| Capture | Ce qu'elle prouve | État |
|---|---|---|
| `commun-hook-local-secrets.png` | le hook local bloque un commit contenant un secret | ✅ |
| `commun-ci-secrets-echec.png` | l'intégration continue rattrape un secret poussé malgré le hook | ✅ |
| `commun-ci-verte.png` | les trois contrôles au vert sur un dépôt propre | ✅ |
| `commun-branche-protegee.png` | la fusion est bloquée tant qu'un contrôle échoue | ⬜ |
| `commun-tests-passes.png` | la suite de tests exécutée — E4 et E5 | ⬜ |
| `commun-historique-git.png` | commits conventionnels, versions publiées | ⬜ |

Les trois premières forment une démonstration complète : le contrôle bloque avant le commit,
rattrape après, et laisse passer ce qui est propre. Un contrôle qu'on n'a jamais vu échouer
n'est pas un contrôle vérifié.
---

## Suivi

| Épreuve | Réalisées | Total |
|---|---|---|
| E4 | 0 | 12 |
| E5 | 0 | 6 |
| E6 | 0 | 7 |
| E7 | 8 | 22 |
| Transverses | 3 | 6 |
| **Total** | **11** | **53** |

Mettre ce tableau à jour à chaque capture ajoutée.
