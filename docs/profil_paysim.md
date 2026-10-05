# Profil du jeu de données PaySim

Source : API Kaggle (`ealaxi/paysim1`)  
Fichier : `PS_20174392719_1491204439457_log.csv`  
Volumétrie : 6 362 620 lignes  11 colonnes


## Colonnes

| Colonne | Type | Valeurs manquantes | Valeurs distinctes |
|---|---|---|---|
| `step` | int64 | 0 | 743 |
| `type` | str | 0 | 5 |
| `amount` | float64 | 0 | 5 316 900 |
| `nameOrig` | str | 0 | 6 353 307 |
| `oldbalanceOrg` | float64 | 0 | 1 845 844 |
| `newbalanceOrig` | float64 | 0 | 2 682 586 |
| `nameDest` | str | 0 | 2 722 362 |
| `oldbalanceDest` | float64 | 0 | 3 614 697 |
| `newbalanceDest` | float64 | 0 | 3 555 499 |
| `isFraud` | int64 | 0 | 2 |
| `isFlaggedFraud` | int64 | 0 | 2 |

## Types d'opération

| Type | Nombre | Part |
|---|---|---|
| CASH_OUT | 2 237 500 | 35.2 % |
| PAYMENT | 2 151 495 | 33.8 % |
| CASH_IN | 1 399 284 | 22.0 % |
| TRANSFER | 532 909 | 8.4 % |
| DEBIT | 41 432 | 0.7 % |

## Fraude

- Transactions frauduleuses : **8 213** sur 6 362 620 (**0.129 %**)
- Transactions signalées par le système existant : 16

### Fraude par type d'opération

| Type | Transactions | Fraudes | Taux |
|---|---|---|---|
| CASH_IN | 1 399 284 | 0 | 0.000 % |
| CASH_OUT | 2 237 500 | 4 116 | 0.184 % |
| DEBIT | 41 432 | 0 | 0.000 % |
| PAYMENT | 2 151 495 | 0 | 0.000 % |
| TRANSFER | 532 909 | 4 097 | 0.769 % |

## Montants

| Statistique | Valeur |
|---|---|
| min | 0.00 |
| 25% | 13 389.57 |
| 50% | 74 871.94 |
| 75% | 208 721.48 |
| max | 92 445 516.64 |
| mean | 179 861.90 |

## Dimension temporelle

- Pas de temps : de 1 à 743 (1 pas = 1 heure, soit 31 jours simulés)

## Parties impliquées

- Émetteurs distincts : 6 353 307
- Destinataires distincts : 2 722 362
- Opérations vers un marchand (préfixe M) : 2 151 495 (33.8 %)
