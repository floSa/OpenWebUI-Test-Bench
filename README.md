# Open WebUI — banc d'essai et manuels vérifiés

**Interroger ses propres documents dans une interface de conversation complète (bases de connaissances, assistants, notes, outils, comptes et permissions), sur sa machine et sans service en ligne : Open WebUI 0.13.3 installé, branché sur un service de modèles local, mesuré sur 38 questions et documenté en un manuel utilisateur de 18 chapitres suivis de 6 annexes, illustré de captures d'écran annotées.**

Trois dossiers : `service/` pour lancer Open WebUI, `banc-essai/` pour rejouer les tests, `documentations/` pour lire.

```text
OpenWebUI-Test-Bench/
├── README.md
├── LICENSE
│
├── service/                 lancer Open WebUI (Docker)
│   ├── installer.sh         première installation
│   ├── demarrer.sh
│   ├── arreter.sh
│   └── …                    état, sauvegarde, réglages
│
├── banc-essai/              rejouer les tests
│   ├── corpus/              9 documents et 38 questions
│   ├── open-webui/          scripts du banc et des captures propres à Open WebUI
│   ├── communs/             outils partagés par les cinq bancs
│   ├── exemples/            appels à l'API, avec leurs sorties vérifiées
│   └── resultats/           scores et preuves brutes
│
└── documentations/          lire
    ├── README.md            sommaire du manuel
    ├── manuel/              le guide, chapitre par chapitre
    ├── annexes/             évaluation, matériel, API, exploitation
    ├── img/                 captures d'écran
    ├── index-serie.md       comparaison des cinq solutions
    ├── fiche-technique.md   architecture, réglages, versions, licences
    ├── rapport.md           bilan
    └── journal.md           avancement
```

Les fichiers locaux, ignorés par git, restent à la racine : `donnees/` (volumes et identifiants), `sources/` le cas échéant.

## Lancer le service

Prérequis : Docker, le service de modèles LLM-Service en marche, sa clé dans `service/.env` (copie de `service/.env.example`).

```bash
cd service
./installer.sh     # première fois seulement
./demarrer.sh
./arreter.sh
```

## Rejouer le banc

Le service doit tourner.

```bash
banc-essai/open-webui/serie_banc.sh <étiquette> [options de banc.py]
```

## Lire la documentation

| Besoin | Page |
|---|---|
| Utiliser Open WebUI pas à pas | [Manuel](documentations/README.md) |
| Installer | [Chapitre 02](documentations/manuel/02-installer-open-webui.md) |
| Résultats détaillés du banc | [Annexe A1](documentations/annexes/A1-evaluation-qualite-et-performances.md) |
| Comparer aux quatre autres solutions | [Index de la série](documentations/index-serie.md) |
| Architecture, réglages, versions, licences | [Fiche technique](documentations/fiche-technique.md) |
| Bilan | [Rapport](documentations/rapport.md) |

## Résultats

Banc de 38 questions (34 avec réponse, 4 pièges), modèles du service central : Qwen3.5-4B avec réflexion, bge-m3, bge-reranker-v2-m3.

| Réglage | OCR | Recherche | Passages | Reranker | Exactes /34 | Pièges refusés /4 | Médiane | Pic RAM de l'application |
|---|---|---|---|---|---|---|---|---|
| défaut |  | vecteurs | 10 |  | 28 | 4 | 60,1 s | 2,3 Go |
| meilleur | Docling déporté | hybride | 10 | bge-reranker-v2-m3 | 34 | 4 | 24,0 s | 3,6 Go |

Meilleur réglage : génération des requêtes de recherche coupée (laissée active, la médiane passe à 58 s). Réflexion du modèle coupée en plus : 34/34, médiane 1,3 s.

Toutes les variantes : [annexe A1](documentations/annexes/A1-evaluation-qualite-et-performances.md). Méthode et preuves : [annexe A6](documentations/annexes/A6-rapport-d-essais.md). Bilan : [documentations/rapport.md](documentations/rapport.md). Comparaison avec les quatre autres solutions : [index de la série](documentations/index-serie.md).
