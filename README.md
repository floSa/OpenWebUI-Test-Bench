# Open WebUI — banc d'essai et manuels vérifiés

**Interroger ses propres documents dans une interface de conversation complète (bases de connaissances, assistants, notes, outils, comptes et permissions), sur sa machine et sans service en ligne : Open WebUI 0.13.3 installé, branché sur un service de modèles local, mesuré sur 38 questions et documenté en un manuel utilisateur de 18 chapitres suivis de 6 annexes, illustré de captures d'écran annotées.**

**Le manuel utilisateur commence ici : [docs/open-webui/README.md](docs/open-webui/README.md).**

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Open WebUI](https://img.shields.io/badge/Open%20WebUI-0.13.3-111827)
![LLM-Service](https://img.shields.io/badge/LLM--Service-LiteLLM%20%2B%20llama.cpp-6A1B9A)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![WSL2](https://img.shields.io/badge/Windows%2011-WSL2-0078D4)

Open WebUI 0.13.3 (image officielle standard, sans Ollama intégré) branché sur le service LLM central (LLM-Service : `chat`, `embed`, `rerank`, `transcribe`), le corpus d'entreprise fictive de la série avec ses pièges (scan, tableaux, audio, document en anglais), un banc de 38 questions dont les réponses sont connues, et un manuel écrit à partir de ce qui a réellement tourné. Chaque action de la partie 1 a été faite à la souris par Playwright et photographiée. Chaque chiffre renvoie à un résultat brut dans `outils/resultats/`.

Cinquième banc de la série après Open Notebook, RAGFlow, AnythingLLM et Kotaemon : mêmes documents, mêmes questions, même machine. Le comparatif est dans [docs/README.md](docs/README.md).

## Sommaire

- [Le parcours](#le-parcours)
- [Architecture](#architecture)
- [Démarrage](#démarrage)
- [Configuration](#configuration)
- [API / Endpoints](#api--endpoints)
- [Tests](#tests)
- [Structure du projet](#structure-du-projet)
- [Licences & composants](#licences--composants)
- [Commandes utiles](#commandes-utiles)
- [Données du banc](#données-du-banc)
- [Les pièges que ce banc documente](#les-pièges-que-ce-banc-documente)
- [Résultats](#résultats)
- [Versions](#versions)
- [Ressources](#ressources)

## Le parcours

| Manuel | Ce qu'on saura faire |
|---|---|
| [01 Découvrir](docs/open-webui/manuel/01-decouvrir-open-webui.md) | dire à quoi sert l'outil, pour qui, sur quelle machine |
| [02 Installer](docs/open-webui/manuel/02-installer-open-webui.md) | installer, ouvrir, arrêter, redémarrer, supprimer |
| [03 Premiers pas](docs/open-webui/manuel/03-premiers-pas.md) | créer le compte administrateur, se repérer, vérifier la connexion aux modèles |
| [04 Première question](docs/open-webui/manuel/04-premiere-question.md) | joindre un document, poser une question, lire la source citée |
| [05 Bases de connaissances](docs/open-webui/manuel/05-bases-de-connaissances.md) à [08 Lecture des documents](docs/open-webui/manuel/08-regler-la-lecture-des-documents.md) | bases, questions citées, assistant lié à une base, Docling, recherche hybride, tri par `rerank` |
| [09 Converser au quotidien](docs/open-webui/manuel/09-converser-au-quotidien.md) à [13 Automatisations](docs/open-webui/manuel/13-automatisations-canaux-calendrier.md) | conversations, notes et mémoire, prompts, outils, fonctions, MCP, voix, automatisations, canaux |
| [14 Comptes](docs/open-webui/manuel/14-comptes-groupes-permissions.md) et [15 Administrer](docs/open-webui/manuel/15-administrer.md) | comptes, groupes, permissions, réglages de l'instance, clés d'API, sauvegarde |
| [16 Cas pratiques](docs/open-webui/manuel/16-cas-pratiques.md), [17 En cas de problème](docs/open-webui/manuel/17-en-cas-de-probleme.md), [18 Glossaire](docs/open-webui/manuel/18-glossaire.md) | trois usages complets, erreurs réelles, vocabulaire |
| [Annexes A1 à A6](docs/open-webui/README.md#partie-2--évaluation-et-compléments) | banc, matériel, API, exploitation, fonctionnement interne, rapport d'essais |

Parcours conseillés : interroger ses documents seul (01 à 08, puis 16) ; équipe (01 à 07, 14, 15, A4) ; automatiser (01 à 04, 15, A3) ; choisir (01, A1, A2).

## Architecture

Open WebUI ne contient aucun modèle : il appelle le service LLM central, partagé avec les autres applications et géré à part.

| Service | Conteneur | Image | Rôle |
|---|---|---|---|
| Open WebUI | `rag-open-webui` | `ghcr.io/open-webui/open-webui:v0.13.3` (figée par empreinte) | interface, API, lecture et découpage des documents, base SQLite, vecteurs, comptes |
| Docling (facultatif) | `rag-docling-serve` | `quay.io/docling-project/docling-serve-cpu:v1.38.2` (figée par empreinte) | lecteur de documents avec lecture optique (PDF scanné) ; profil compose `docling`, sans port publié |
| Serveur MCP d'essai (facultatif) | `rag-mcp-velanor` | image Open WebUI ci-dessus, lancée sur `outils/open-webui/extensions/serveur_mcp_velanor.py` | deux fonctions sur l'entreprise fictive, pour le chapitre 11 ; sans port publié |
| Modèles | `llm-central`, `llm-swap`, `llm-speaches` | LiteLLM v1.109.0, llama-swap v272 (llama.cpp b12282), speaches 0.8.3 | `chat`, `embed`, `rerank`, `transcribe` servis par [LLM-Service](https://github.com/floSa/llm-service) (dépôt séparé) |
| Captures | `rag-captures` (éphémère) | `mcr.microsoft.com/playwright/python:v1.65.1-noble` | scénarios Playwright du manuel |

```mermaid
flowchart LR
  nav[Navigateur Windows] -->|127.0.0.1:3000| app
  subgraph app["rag-open-webui"]
    ui[Interface et API]
    db[(SQLite et vecteurs)]
  end
  ui --> db
  ui -->|llm-net, http://llm-central:8080/v1| llm[service LLM central : chat, embed, rerank, transcribe]
  ui -->|llm-net, http://rag-docling-serve:5001| doc[rag-docling-serve]
  ui -->|rag-local, http://rag-mcp-velanor:8000/mcp| mcp[rag-mcp-velanor]
  pw[rag-captures Playwright] -->|rag-local| ui
```

Réseaux Docker externes : `llm-net` (créé par LLM-Service) relie Open WebUI au service de modèles et à Docling ; `rag-local` relie Open WebUI au serveur MCP d'essai, aux captures et au banc. Un seul port publié, `127.0.0.1:3000` (`outils/resultats/open-webui/installation-2026-11-13.log`).

## Démarrage

Prérequis : Windows 11 avec WSL2 et Docker Desktop ; [LLM-Service](https://github.com/floSa/llm-service) installé et démarré ; environ 5 Go de disque pour l'image d'Open WebUI (4,59 Go).

```bash
cp .env.example .env
~/mes_projets/Projet-IA/LLM-Service/scripts/cle.sh creer openwebui-test-bench --dans "$PWD/.env" --noms LLM_CENTRAL_URL,LLM_CENTRAL_KEY   # clé propre au banc, écrite sans affichage
outils/communs/llm_central_sante.sh --essai   # le service répond-il, modèle par modèle ?
outils/open-webui/installer.sh                # image, secret de session, démarrage, contrôle des ports
```

| Service | URL | Note |
|---|---|---|
| Open WebUI | http://127.0.0.1:3000 | compte administrateur créé dans le navigateur au premier accès (chapitre 03) ; identifiants fictifs du jeu de démonstration dans `donnees/IDENTIFIANTS-LOCAUX.txt` |
| Service LLM central | http://127.0.0.1:8080/v1 | clé dans `.env` |

Ensuite : [chapitre 02](docs/open-webui/manuel/02-installer-open-webui.md) (installation pas à pas) et [chapitre 03](docs/open-webui/manuel/03-premiers-pas.md) (premier compte, connexion aux modèles). Options : `outils/open-webui/docling.sh start` (lecture des scans, chapitre 08) et `outils/open-webui/mcp.sh start` (serveur MCP d'essai, chapitre 11).

## Configuration

- **Variables générées** : `installer.sh` écrit `WEBUI_SECRET_KEY` (secret de session) dans `donnees/open-webui/options.env`, jamais versionné ni affiché.
- **Variables du compose** (`outils/open-webui/compose.yml`) : `DEFAULT_LOCALE=fr-FR` ; `ENABLE_OLLAMA_API=false`, `ENABLE_OPENAI_API=true` ; embeddings `RAG_EMBEDDING_ENGINE=openai`, `RAG_EMBEDDING_MODEL=embed`, `RAG_EMBEDDING_BATCH_SIZE=4` ; transcription `AUDIO_STT_ENGINE=openai`, `AUDIO_STT_MODEL=transcribe` ; télémétrie coupée (`SCARF_NO_ANALYTICS`, `DO_NOT_TRACK`, `ANONYMIZED_TELEMETRY`).
- **Écarts au compose officiel** : service `ollama` retiré ; image standard figée par étiquette et empreinte ; projet, conteneurs et réseaux préfixés `rag-` ; port publié sur `127.0.0.1` seulement ; données dans `donnees/open-webui/data` au lieu d'un volume nommé ; réseaux externes `llm-net` et `rag-local` ; Docling ajouté en service facultatif.
- **Branchement au service LLM central** : connexion compatible OpenAI vers `http://llm-central:8080/v1` (réseau `llm-net`), noms de modèles fixes `chat`, `embed`, `rerank`, `transcribe`. La clé `LLM_CENTRAL_KEY` reste dans `.env` (modèle : `.env.example`) ; `outils/open-webui/compose.sh` la transmet au compose sans l'afficher. Ces valeurs ne sont lues qu'au premier démarrage, puis gardées en base et modifiables dans « Paramètres d'administration ». Le tri par `rerank` se règle dans l'interface (moteur « Externe », `http://llm-central:8080/v1/rerank`), [chapitre 08](docs/open-webui/manuel/08-regler-la-lecture-des-documents.md).

## API / Endpoints

Routes de l'API d'Open WebUI utilisées par le banc et les essais (client minimal, bibliothèque standard seulement : [outils/open-webui/client.py](outils/open-webui/client.py)) :

| Méthode | Route | Rôle |
|---|---|---|
| `GET` | `/health` | état de l'application, sans connexion |
| `POST` | `/api/v1/auths/signin` | connexion, renvoie un jeton |
| `POST` | `/api/v1/files/?process=true` | téléverser un fichier (lecture, découpage, vecteurs) |
| `GET` | `/api/v1/files/{id}/process/status` | suivre le traitement d'un fichier |
| `POST` | `/api/v1/knowledge/create`, `/api/v1/knowledge/{id}/file/add` | créer une base, y rattacher un fichier |
| `POST` | `/api/chat/completions` | poser une question (réponse et sources citées) |
| `GET`, `POST` | `/api/v1/retrieval/config`, `/api/v1/retrieval/config/update` | lire et écrire les réglages de recherche |
| `GET`, `POST` | `/api/v1/tasks/config`, `/api/v1/tasks/config/update` | lire et écrire les tâches du modèle (génération des requêtes de recherche) |
| `GET` | `/api/v1/configs/export` | exporter toute la configuration (contient la clé du service) |

Détail : [annexe A3](docs/open-webui/annexes/A3-automatiser-par-l-api.md).

## Tests

```bash
outils/communs/llm_central_sante.sh --essai                    # santé du service LLM central, une requête par usage
outils/open-webui/serie_banc.sh <étiquette> [options de banc.py]   # banc de 38 questions sur la base « Banc »
python3 outils/communs/verifier_docs.py                        # documentation : liens, ancres, ton, captures, carte
```

Exemple de série : `outils/open-webui/serie_banc.sh hybride-rerank --rerank` (recherche hybride et tri par `rerank`) ; `--taches '{"ENABLE_RETRIEVAL_QUERY_GENERATION": false}'` coupe la génération des requêtes de recherche.

Sortie du contrôle de santé en début de session (`outils/resultats/open-webui/sante-llm-central-2026-11-13-debut.log`, extrait) :

```text
== embed
  dimensions : 1024
== rerank
  doc 0 score 9.05
  doc 1 score -8.63
```

Sortie de l'installation (`outils/resultats/open-webui/installation-2026-11-13.log`, extrait) :

```text
Open WebUI prêt : http://127.0.0.1:3000 (24 s)
rag-open-webui 127.0.0.1:3000->8080/tcp
ports : tous liés à 127.0.0.1
{"version":"0.13.3","deployment_id":""}
```

## Structure du projet

```text
docs/open-webui/      manuel : README (sommaire), manuel/ (partie 1), annexes/ (partie 2), img/ (captures)
docs/README.md        index de la série et comparatif du banc
docs/glossaire.md     glossaire partagé par la série
outils/open-webui/    compose, installer, démarrer, arrêter, état, Docling, MCP, client, banc, extensions/, captures/
outils/communs/       outils partagés par la série (diagnostic, santé du service, versions, banc, captures, vérification)
outils/resultats/     résultats bruts (open-webui/, bancs précédents, machine/)
corpus/               documents fictifs et questions de référence
kit/                  consigne de mission et fiches des solutions
donnees/              données, identifiants locaux (non versionné)
```

Détail des scripts : [outils/README.md](outils/README.md).

## Licences & composants

| Composant | Licence |
|---|---|
| Open WebUI | Open WebUI License : BSD-3 avec clause de marque (la marque « Open WebUI » doit rester visible) |
| Docling | MIT |
| LiteLLM, llama.cpp, llama-swap, speaches | MIT |
| bge-m3 (`embed`), faster-whisper-small (`transcribe`) | MIT |
| Playwright | Apache 2.0 |

Ce projet : MIT — Copyright (c) 2026 floSa (fichier [LICENSE](LICENSE)).

## Commandes utiles

```bash
outils/open-webui/etat.sh            # conteneurs, ports, santé, mémoire, disque, santé du service central
outils/open-webui/demarrer.sh        # démarrage (données conservées)
outils/open-webui/arreter.sh         # arrêt (données conservées) ; LLM-Service n'est jamais arrêté
outils/open-webui/docling.sh start   # lecteur Docling (stop pour l'arrêter)
outils/open-webui/mcp.sh start       # serveur MCP d'essai (stop pour l'arrêter)
outils/open-webui/client.py GET /api/v1/retrieval/config   # lire les réglages de recherche
docker logs --tail 100 rag-open-webui
outils/communs/nettoyer.sh open-webui   # suppression complète, sur confirmation
```

## Données du banc

Corpus fictif (entreprise Vélanor, vélos électriques) : 9 documents (`corpus/MANIFEST.json`) et 38 questions (`corpus/questions.json`), repris tels quels des bancs précédents.

```text
rapport-annuel-2025.pdf          contrat-batterix-scan.pdf (scan, image seule)
procedure-batteries.docx         strategie-2026.pptx
stocks-octobre-2025.xlsx         faq-sav.html, cse-2025-10-14.md
supplier-audit-batterix-en.pdf   message-vocal-production.mp3
```

Questions : 13 faits simples, 10 tableaux, 4 sur le scan, 3 multi-documents, 2 en anglais, 2 sur l'audio, et 4 pièges dont la réponse n'est pas dans les documents.

## Les pièges que ce banc documente

1. Les réglages passés par variables d'environnement ne sont lus qu'au premier démarrage, puis gardés en base : changer le compose ensuite n'a plus d'effet ([annexe A5](docs/open-webui/annexes/A5-fonctionnement-interne.md)).
2. Le reranker externe `rerank` n'agit que si « Recherche hybride » est activée ([chapitre 08](docs/open-webui/manuel/08-regler-la-lecture-des-documents.md)).
3. PDF scanné refusé à l'ajout dans une base avec la lecture par défaut : « The content provided is empty ». Seul Docling le lit (chapitre 08).
4. La génération des requêtes de recherche, active par défaut, lance trois recherches par question et un appel de plus au modèle : la médiane passe de 58 s à 24 s quand elle est coupée (chapitre 08).
5. Tout est privé par défaut, modèles compris : un nouveau compte ne voit aucun modèle tant que l'administrateur ne l'a pas partagé ([chapitre 14](docs/open-webui/manuel/14-comptes-groupes-permissions.md)).
6. L'export de la configuration contient la clé du service de modèles (`outils/resultats/open-webui/essai-export-config-2026-11-13.txt`, [chapitre 15](docs/open-webui/manuel/15-administrer.md)).
7. L'export d'une base donne le texte extrait de chaque fichier, pas les fichiers d'origine (`essai-export-base-2026-11-13.txt`, [chapitre 05](docs/open-webui/manuel/05-bases-de-connaissances.md)).
8. L'identifiant d'un modèle personnalisé est généré sans les lettres accentuées : « Assistant qualité Vélanor » devient `assistant-qualit-vlanor` ([chapitre 07](docs/open-webui/manuel/07-assistant-lie-a-une-base.md)).

## Résultats

Banc de 38 questions (34 avec réponse, 4 pièges), modèles du service central : Qwen3.5-4B avec réflexion, bge-m3, bge-reranker-v2-m3.

| Réglage | OCR | Recherche | Passages | Reranker | Exactes /34 | Pièges refusés /4 | Médiane | Pic RAM de l'application |
|---|---|---|---|---|---|---|---|---|
| défaut | aucun : scan refusé | vecteurs | 10 | aucun | 28 | 4 | 60,1 s | 2,3 Go |
| meilleur | Docling déporté | hybride | 10 | bge-reranker-v2-m3 | 34 | 4 | 24,0 s | 3,6 Go |

Meilleur réglage : génération des requêtes de recherche coupée (laissée active, la médiane passe à 58 s). Réflexion du modèle coupée en plus : 34/34, médiane 1,3 s.

Toutes les variantes : [annexe A1](docs/open-webui/annexes/A1-evaluation-qualite-et-performances.md). Méthode et preuves : [annexe A6](docs/open-webui/annexes/A6-rapport-d-essais.md). Bilan : [RAPPORT-open-webui.md](RAPPORT-open-webui.md). Comparaison avec les quatre autres solutions : [index de la série](docs/README.md).

## Versions

| Composant | Version |
|---|---|
| Open WebUI | 0.13.3 (8 novembre 2026), image `ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158e6558eeb980bc828e0f1b30238ad24d82ed84d5e5eda1dab2a082f14` |
| docling-serve | v1.38.2 (27 octobre 2026), image `docling-serve-cpu` |
| Playwright | 1.65.1 |
| Service central | LiteLLM v1.109.0, llama-swap v272, llama.cpp b12282, speaches 0.8.3 |
| Docker / Compose | 29.9.3 / 5.7.0 |
| WSL / Ubuntu | 3.0.5.0 / 24.04.5 |

Relevés : `outils/resultats/open-webui/versions-2026-11-13.json` et `outils/resultats/machine/diagnostic-2026-11-13.json`. La version est figée par étiquette et empreinte dans `outils/open-webui/compose.yml`.

## Ressources

- Open WebUI : https://github.com/open-webui/open-webui, site https://openwebui.com
- LLM-Service : https://github.com/floSa/llm-service
- Bancs précédents : https://github.com/floSa/Open-Notebook-Test-Bench, https://github.com/floSa/RAGFlow-Test-Bench, https://github.com/floSa/AnythingLLM-Test-Bench, https://github.com/floSa/Kotaemon-Test-Bench
