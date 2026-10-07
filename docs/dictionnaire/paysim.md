# Dictionnaire de donnees — Transactions mobile money (PaySim)

> **Document genere automatiquement — ne pas modifier a la main.**
> Le sens metier provient de `docs/dictionnaire/paysim.yml`.
> Les caracteristiques techniques sont mesurees sur la couche bronze.

| | |
|---|---|
| Origine | Kaggle — ealaxi/paysim1, simulateur calibré sur un mois de journaux réels |
| Granularite | Une ligne = une transaction mobile money |
| Responsable | Mariam Douamba |
| Partition analysee | `lakehouse/bronze/paysim/dt=2026-10-06` |
| Enregistrements | 6 362 620 |
| Colonnes | 14 |
| Genere le | 07/10/2026 a 15:14 UTC |

## Synthese

| Colonne | Type | Libelle | Nulles | A zero | Distinctes | RGPD |
|---|---|---|---|---|---|---|
| `step` | int64 | Pas de temps | 0 (0.00%) | 0 (0.00%) | 743 | Non personnelle |
| `type` | large_string | Nature de l'opération | 0 (0.00%) | — | 5 | Non personnelle |
| `amount` | double | Montant de la transaction | 0 (0.00%) | 16 (0.00%) | 5 316 900 | Donnee financiere rattachable |
| `nameOrig` | large_string | Compte émetteur | 0 (0.00%) | — | 6 353 307 | Identifiant indirect |
| `oldbalanceOrg` | double | Solde émetteur avant | 0 (0.00%) | 2 102 449 (33.04%) | 1 845 844 | Donnee financiere rattachable |
| `newbalanceOrig` | double | Solde émetteur après | 0 (0.00%) | 3 609 566 (56.73%) | 2 682 586 | Donnee financiere rattachable |
| `nameDest` | large_string | Compte destinataire | 0 (0.00%) | — | 2 722 362 | Identifiant indirect |
| `oldbalanceDest` | double | Solde destinataire avant | 0 (0.00%) | 2 704 388 (42.50%) | 3 614 697 | Donnee financiere rattachable |
| `newbalanceDest` | double | Solde destinataire après | 0 (0.00%) | 2 439 433 (38.34%) | 3 555 499 | Donnee financiere rattachable |
| `isFraud` | int64 | Fraude avérée | 0 (0.00%) | 6 354 407 (99.87%) | 2 | Non personnelle |
| `isFlaggedFraud` | int64 | Signalement du dispositif existant | 0 (0.00%) | 6 362 604 (100.00%) | 2 | Non personnelle |
| `_source` | large_string | Source d'origine | 0 (0.00%) | — | 1 | Non personnelle |
| `_lot` | large_string | Lot d'ingestion | 0 (0.00%) | — | 1 | Non personnelle |
| `_ingere_le` | timestamp[us, tz=UTC] | Date d'ingestion | 0 (0.00%) | — | 1 | Non personnelle |

## Detail par colonne

### `step` — Pas de temps

Heure simulée écoulée depuis le début de la période d'observation. 743 pas successifs, numerotes de 1 a 743 sans rupture, soit 30 jours et 23 heures d'observation continue.

- **Type mesure** : `int64`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 743
- **Valeurs a zero** : 0 (0.00%)
- **Etendue** : 1 a 743
- **Regle de gestion** : Converti en horodatage réel en couche silver, à partir d'une date d'origine conventionnelle.
- **Classification RGPD** : Non personnelle

### `type` — Nature de l'opération

Famille d'opération mobile money. CASH_IN et CASH_OUT correspondent aux dépôts et retraits en espèces chez un agent, TRANSFER à un virement entre comptes, PAYMENT à un paiement marchand, DEBIT à un prélèvement.

- **Type mesure** : `large_string`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 5
- **Etendue** : CASH_IN a TRANSFER
- **Valeurs observees** : CASH_OUT (2 237 500), PAYMENT (2 151 495), CASH_IN (1 399 284), TRANSFER (532 909), DEBIT (41 432)
- **Regle de gestion** : Seules TRANSFER et CASH_OUT portent de la fraude dans ce jeu. Le périmètre de détection est restreint à ces deux familles. La correspondance entre PAYMENT et les destinataires marchands est exacte et réciproque, ce qui exclut du périmètre toute ambiguïté sur les soldes.
- **Classification RGPD** : Non personnelle

### `amount` — Montant de la transaction

Montant dans la monnaie locale du simulateur.

- **Type mesure** : `double`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 5 316 900
- **Valeurs a zero** : 16 (0.00%)
- **Etendue** : 0.0 a 92445516.64
- **Regle de gestion** : Doit être strictement positif. Un montant nul signale une anomalie de collecte.
- **Classification RGPD** : Donnee financiere rattachable

### `nameOrig` — Compte émetteur

Identifiant du compte à l'origine de l'opération. Pseudonyme de la forme C suivi d'une suite numérique.

- **Type mesure** : `large_string`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 6 353 307
- **Etendue** : C1000000639 a C999999784
- **Regle de gestion** : Pseudonymisé par empreinte avec sel en couche silver.
- **Classification RGPD** : Identifiant indirect

### `oldbalanceOrg` — Solde émetteur avant

Solde du compte émetteur avant l'opération.

- **Type mesure** : `double`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 1 845 844
- **Valeurs a zero** : 2 102 449 (33.04%)
- **Etendue** : 0.0 a 59585040.37
- **Regle de gestion** : Cohérence attendue avec newbalanceOrig et amount. L'écart à cette cohérence est un signal de détection étudié.
- **Classification RGPD** : Donnee financiere rattachable

### `newbalanceOrig` — Solde émetteur après

Solde du compte émetteur après l'opération.

- **Type mesure** : `double`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 2 682 586
- **Valeurs a zero** : 3 609 566 (56.73%)
- **Etendue** : 0.0 a 49585040.37
- **Regle de gestion** : Voir oldbalanceOrg.
- **Classification RGPD** : Donnee financiere rattachable

### `nameDest` — Compte destinataire

Identifiant du compte destinataire. Préfixe C pour un client, M pour un marchand.

- **Type mesure** : `large_string`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 2 722 362
- **Etendue** : C1000004082 a M999999784
- **Regle de gestion** : Pseudonymisé par empreinte avec sel en couche silver.
- **Classification RGPD** : Identifiant indirect

### `oldbalanceDest` — Solde destinataire avant

Solde du compte destinataire avant l'opération. L'absence d'information n'est pas encodée par une valeur nulle mais par la valeur 0.0 : les 2 151 495 destinataires marchands portent tous un solde à zéro.

- **Type mesure** : `double`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 3 614 697
- **Valeurs a zero** : 2 704 388 (42.50%)
- **Etendue** : 0.0 a 356015889.35
- **Regle de gestion** : Un zéro est ambigu. Il signale soit l'absence d'information (destinataire marchand, donc famille PAYMENT), soit un solde réellement nul (destinataire client). Les deux cas se distinguent par le préfixe de nameDest. En couche silver, l'absence d'information devient une valeur nulle explicite ; le solde réellement nul reste à zéro.
- **Classification RGPD** : Donnee financiere rattachable

### `newbalanceDest` — Solde destinataire après

Solde du compte destinataire après l'opération. Même encodage de l'absence d'information que oldbalanceDest.

- **Type mesure** : `double`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 3 555 499
- **Valeurs a zero** : 2 439 433 (38.34%)
- **Etendue** : 0.0 a 356179278.92
- **Regle de gestion** : Voir oldbalanceDest — distinction par le préfixe de nameDest.
- **Classification RGPD** : Donnee financiere rattachable

### `isFraud` — Fraude avérée

Indique une opération menée par un agent frauduleux ayant pris le contrôle d'un compte : vidage du solde par virement, puis retrait en espèces.

- **Type mesure** : `int64`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 2
- **Valeurs a zero** : 6 354 407 (99.87%)
- **Etendue** : 0 a 1
- **Valeurs observees** : 0 (6 354 407), 1 (8 213)
- **Regle de gestion** : Vérité terrain servant à évaluer les règles de détection. Jamais utilisée comme signal d'entrée d'une règle.
- **Classification RGPD** : Non personnelle

### `isFlaggedFraud` — Signalement du dispositif existant

Marquage produit par la règle métier historique du simulateur, qui signale les tentatives de virement dépassant un seuil fixe.

- **Type mesure** : `int64`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 2
- **Valeurs a zero** : 6 362 604 (100.00%)
- **Etendue** : 0 a 1
- **Valeurs observees** : 0 (6 362 604), 1 (16)
- **Regle de gestion** : Sert de référence de comparaison : toute règle que je propose doit faire mieux que ce dispositif existant.
- **Classification RGPD** : Non personnelle

### `_source` — Source d'origine

Système dont provient l'enregistrement.

- **Type mesure** : `large_string`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 1
- **Etendue** : paysim a paysim
- **Valeurs observees** : paysim (6 362 620)
- **Regle de gestion** : Ajouté à l'ingestion. Ne provient pas de la source.
- **Classification RGPD** : Non personnelle

### `_lot` — Lot d'ingestion

Identifiant horodaté de l'exécution qui a chargé l'enregistrement.

- **Type mesure** : `large_string`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 1
- **Etendue** : 20261006T145557Z a 20261006T145557Z
- **Valeurs observees** : 20261006T145557Z (6 362 620)
- **Regle de gestion** : Ajouté à l'ingestion. Permet de rejouer ou d'isoler un chargement.
- **Classification RGPD** : Non personnelle

### `_ingere_le` — Date d'ingestion

Horodatage UTC de l'entrée dans la plateforme.

- **Type mesure** : `timestamp[us, tz=UTC]`
- **Valeurs nulles** : 0 sur 6 362 620 (0.00%)
- **Valeurs distinctes** : 1
- **Etendue** : 2026-10-06 14:55:57.812241+00:00 a 2026-10-06 14:55:57.812241+00:00
- **Valeurs observees** : 2026-10-06 14:55:57.812241+00:00 (6 362 620)
- **Regle de gestion** : Ajouté à l'ingestion.
- **Classification RGPD** : Non personnelle

## Constats de qualite

- L'etendue de `step` est 1 a 743, sans aucune valeur manquante. La periode couverte est de 30 jours et 23 heures, et non de 31 jours pleins comme l'annonce la documentation courante du jeu de donnees.
- L'activite varie dans un rapport de 1 a 25 000 selon l'heure : 2 transactions sur les pas 112 et 662, contre 51 352 sur le pas 19. Le simulateur reproduit un cycle jour/nuit marque. Tout dimensionnement de debit se fait sur le pic, jamais sur la moyenne.
- `nameOrig` compte 6 353 307 valeurs distinctes pour 6 362 620 enregistrements, soit 99,85 % d'identifiants uniques. Cette cardinalite explique le plafond du taux de compression observe en Parquet.
- `nameDest` compte 2 722 362 valeurs distinctes, soit 2,3 receptions par destinataire en moyenne. Cette asymetrie entre emetteurs et destinataires est le terrain des regles de detection : un destinataire concentrant les receptions est un signal.
- La correspondance entre la famille PAYMENT et les destinataires marchands est exacte et reciproque : 2 151 495 lignes des deux cotes. Aucun marchand n'apparait dans une autre famille d'operation.
- Les 2 704 388 soldes destinataire a zero se repartissent en 2 151 495 absences d'information (marchands) et 552 893 soldes reellement nuls (clients). Quatre zeros sur cinq ne sont pas des zeros.
- Sur le perimetre de detection (TRANSFER et CASH_OUT, 2 770 409 lignes), aucun destinataire marchand n'est present. Les 389 320 soldes a zero qui s'y trouvent sont tous des soldes reellement nuls, donc du signal exploitable.
