# A2. Choisir son matériel et ses modèles

> **Objet** : dire sur quelle machine faire tourner Open WebUI et son service de modèles, sans et avec carte graphique NVIDIA : mémoire prise par chaque élément, ce qui reste, volume de documents utilisable et temps d'attente.
> **Prérequis** : [sommaire du manuel](../README.md) ; annexe [A1](A1-evaluation-qualite-et-performances.md) pour les résultats du banc ; annexe [A5](A5-fonctionnement-interne.md) pour l'architecture.
> **Version décrite** : Open WebUI 0.13.3, docling-serve 1.38.2 ; service LLM central (LiteLLM v1.109.0, llama-swap v272, llama.cpp b12282, speaches 0.8.3), branche `service-llamacpp`, commit `8568e75` ; essais du 13 novembre 2026.
> **Statut des informations** : [Vérifié] mesuré sur la machine d'essai (profil B), fichier cité ; [Source] repris des mesures de LLM-Service (`~/mes_projets/Projet-IA/LLM-Service/README.md`, section « Mesures », et dossiers `mesures/cpu`, `mesures/gpu`) ; [Estimation] calcul expliqué ; [À tester] non mesuré.
> **Précautions** : le profil A (sans carte graphique) n'a pas été mesuré avec Open WebUI ; tous ses temps sont des estimations calculées à partir des débits du service central.

## Sommaire

1. [Ce qui consomme la mémoire et le disque](#1-ce-qui-consomme-la-mémoire-et-le-disque)
2. [Profil A : sans carte graphique](#2-profil-a--sans-carte-graphique)
3. [Profil B : avec carte graphique NVIDIA](#3-profil-b--avec-carte-graphique-nvidia)
4. [Budget de contexte et volume de documents](#4-budget-de-contexte-et-volume-de-documents)
5. [Modèles](#5-modèles)
6. [Dépannage](#dépannage)
7. [Sources](#sources)

## 1. Ce qui consomme la mémoire et le disque

| Élément | Mémoire ou disque | Statut |
|---|---|---|
| Open WebUI au repos | 969 Mio | [Vérifié] ([installation](../../banc-essai/resultats/open-webui/installation-2026-11-13.log)) |
| Open WebUI pendant un banc | 1 440 à 1 595 Mo | [Vérifié] (`pic_ram_mo` des [bancs](A1-evaluation-qualite-et-performances.md#4-temps-et-mémoire)) |
| Docling (lecture des scans, facultatif) | 902 Mo au démarrage, 2 393 Mo au plus fort de l'indexation, environ 1 970 Mo ensuite | [Vérifié] ([docling-demarrage](../../banc-essai/resultats/open-webui/docling-demarrage-2026-11-13.log), [banc Docling](../../banc-essai/resultats/open-webui/banc-2026-11-13-docling-rerank.json)) |
| Image d'Open WebUI | 4,59 Go sur disque (4 586 452 578 octets) | [Vérifié] ([installation](../../banc-essai/resultats/open-webui/installation-2026-11-13.log)) |
| Image de Docling (`docling-serve-cpu`) | 5,06 Go sur disque (5 060 911 843 octets) | [Vérifié] ([pull-docling](../../banc-essai/resultats/open-webui/pull-docling-2026-11-13.log)) |
| Service central, profil `cpu` : LiteLLM, llama-swap, speaches | 593 Mio + 3,6 Gio + 127 Mio, soit environ 4,3 Go | [Source] (`LLM-Service/documentation/verification/mesures/cpu/memoire-vive-conteneurs.txt`) |
| Service central, profil `gpu` : mémoire vive | LiteLLM 0,8, llama-swap 4,4, speaches 0,2 Go (1,5 Go avec Whisper chargé), soit environ 5,4 Go | [Source] (`LLM-Service/README.md`, « Mesures », `mesures/gpu/memoire-vive-cache-ram-2048.txt`) |
| Service central, profil `gpu` : mémoire vive relevée pendant les bancs | 722 à 746 Mo + 5 262 à 5 443 Mo + 1 309 à 1 364 Mo, soit environ 7,5 Go (transcription chargée) | [Vérifié] (`pic_ram_mo` des six bancs) |
| Service central, profil `gpu` : carte graphique | 7,0 Go pour `chat`, `embed` et `rerank` ; 1 818 Mio pris par Windows service arrêté | [Source] (`LLM-Service/README.md`, « Mesures ») |
| Carte graphique relevée en fin de banc | 9 436 à 9 890 Mo sur 16 380, bureau Windows compris | [Vérifié] (`vram` des six bancs) |
| Disque des modèles du service central | non relevé ici | [À tester] |

Le nombre de documents d'une base change peu la mémoire : textes et vecteurs sont sur disque (Chroma intégré, SQLite), et seuls les passages retrouvés partent au modèle. [Source] (annexe [A5](A5-fonctionnement-interne.md))

## 2. Profil A : sans carte graphique

Machine type : PC portable Intel Core Ultra 7 255H, 15,3 Go de mémoire dans WSL ; service central en profil `cpu` (`service/scripts/demarrer.sh cpu`). Rien ne change pour Open WebUI : même adresse, mêmes noms de modèles. [Source] (`kit/PROMPT.md` §1, `LLM-Service/README.md`)

**Calcul des temps [Estimation].** Le temps de réponse d'Open WebUI est dominé par la génération des jetons par `chat` : à la question Q01, 1 458 jetons produits en 21,4 s contre 2 093 jetons lus en 0,68 s ([essai-minimal-api](../../banc-essai/resultats/open-webui/essai-minimal-api-2026-11-13.json), `timings`). Le service central mesure 68 jetons/s sur la carte graphique et 14 jetons/s sur le processeur pour une requête [Source] (`LLM-Service/README.md`, « Processeur seul » ; `mesures/cpu/banc-chat-partiel.md`). Les temps mesurés en profil B sont donc multipliés par 68 / 14 ≈ 4,9. Contrôle : 1 458 jetons à 14 jetons/s font 104 s, ce qui rejoint les « environ 2 min » de réponse avec réflexion relevées par le service central. Ces temps sont des minimums : la lecture de la question et des passages (2 000 jetons environ) sur processeur n'a pas été mesurée [À tester], et les mesures `cpu` du service ont été faites sur le Ryzen 5 9600X, pas sur le processeur portable.

| Élément | Valeur | Statut |
|---|---|---|
| Processeur | 8 cœurs récents ou plus (AVX2) ; débit du Core Ultra 7 255H supposé du même ordre que celui du Ryzen 5 9600X mesuré | [Estimation] |
| Mémoire vive au plus fort | service 4,3 Go + transcription chargée 1,2 Go + Open WebUI 1,6 Go + Docling 2,4 Go ≈ 9,5 Go ; sans Docling ≈ 7,1 Go | [Estimation] (somme des lignes de la section 1 ; 1,2 Go = speaches relevé ici avec Whisper moins speaches au repos) |
| Ce qui reste sur 15,3 Go | environ 5,8 Go pour WSL, Docker et les autres programmes ; un seul essai lourd à la fois | [Estimation] |
| Disque | 10 Go d'images (Open WebUI 4,59 Go, Docling 5,06 Go), plus les modèles du service et les données | [Estimation] (somme des images [Vérifié]) |
| Débit de `chat` | 14 jetons/s pour une requête, 31 jetons/s cumulés pour quatre | [Source] |
| Indexation | `embed` passe de 0,05 à 0,08 s pour 10 passages ; Docling tourne déjà sur le processeur en profil B : indexation du corpus du même ordre que les 51 s mesurées, plus lente sur un processeur portable | [Source] pour `embed` ; [Estimation] pour la durée |

| Profil A | Valeur |
|---|---|
| Profil du service | `cpu` (`llm-swap-cpu`) |
| Modèles | `chat` = Qwen3.5-4B Q4_K_M, `embed` = bge-m3 Q8_0, `rerank` = bge-reranker-v2-m3 Q8_0, `transcribe` = faster-whisper-small [Source] (`LLM-Service/README.md`, tableau des modèles) |
| Contexte | 16 384 jetons par requête [Source] |
| Mémoire service et application | 4,3 à 5,5 Go pour le service, 1,0 à 1,6 Go pour Open WebUI, 0,9 à 2,4 Go pour Docling [Estimation] |
| Réglages conseillés | Docling pour les scans, recherche hybride et tri `rerank`, « Génération de requête de RAG » coupée, réflexion coupée sur un assistant (`chat_template_kwargs`), « Top K » 10 |
| Résultats du banc | non mesurés sur ce profil ; mêmes modèles, donc même qualité attendue (34/34 avec les réglages conseillés) [Estimation] |
| Temps d'attente, réflexion coupée | médiane 1,3 × 4,9 ≈ 6 s ; 95 % sous 3,1 × 4,9 ≈ 15 s [Estimation] |
| Temps d'attente, génération des requêtes coupée, réflexion active | médiane 24,0 × 4,9 ≈ 2 min ; 95 % sous 86,9 × 4,9 ≈ 7 min [Estimation] |
| Temps d'attente, réglages par défaut | médiane 58,3 × 4,9 = 285,7 s ≈ 4,8 min ; 95 % sous 114,7 × 4,9 ≈ 9 min [Estimation] : à éviter |

Sur processeur, couper la réflexion et la génération des requêtes n'est pas un confort mais une condition d'usage. [Estimation]

## 3. Profil B : avec carte graphique NVIDIA

Machine d'essai : AMD Ryzen 5 9600X (12 cœurs logiques), 32 098 Mo dans WSL, NVIDIA GeForce RTX 4060 Ti 16 380 Mio, pilote 616.92, 530 Go libres ; service central en profil `gpu`. [Vérifié] ([diagnostic](../../banc-essai/resultats/machine/diagnostic-2026-11-13.json))

| Profil B | Valeur | Statut |
|---|---|---|
| Profil du service | `gpu` (`llm-swap`, image `llama-swap:v272-cuda-b12282`) | [Vérifié] ([diagnostic](../../banc-essai/resultats/machine/diagnostic-2026-11-13.json)) |
| Modèles | `chat`, `embed`, `rerank`, `transcribe` et leurs noms réels (`qwen3.5-4b`, `bge-m3`, `bge-reranker-v2-m3`, `faster-whisper-small`), plus `gemma-4-e4b` à la demande | [Vérifié] ([santé du service](../../banc-essai/resultats/open-webui/sante-llm-central-2026-11-13-debut.log)) ; quantifications Q4_K_M et Q8_0 : [Source] |
| Contexte | 16 384 jetons par requête | [Source] (`LLM-Service/README.md`, tableau des modèles) |
| Carte graphique | 12 Go conseillés : 7,0 Go pour les trois modèles permanents [Source] plus le bureau Windows (1 818 Mio service arrêté [Source]) ; 9,4 à 9,9 Go relevés sur la carte de 16 Go [Vérifié] ; une carte de 8 Go est trop juste (7,0 + 1,8 = 8,8 Go) [Estimation] | |
| Mémoire vive | 16 Go dans WSL au minimum : service 7,5 Go et application 2,3 à 4,0 Go relevés au plus fort [Vérifié] (`pic_ram_mo`, `pic_ram_application_mo`), soit 11,5 Go [Estimation] ; 32 Go confortables | |
| Débit de `chat` | 68 jetons/s pour une requête, 174 jetons/s cumulés pour quatre [Source] ; 68,0 jetons/s relevés à la question Q01 [Vérifié] ([essai-minimal-api](../../banc-essai/resultats/open-webui/essai-minimal-api-2026-11-13.json)) | |
| Réglages | Docling, recherche hybride, tri `rerank`, génération des requêtes coupée, « Top K » 10 ; réflexion coupée pour les questions factuelles | [Vérifié] (annexe [A1](A1-evaluation-qualite-et-performances.md#6-préconisations)) |
| Résultats du banc | 28/34 avec la lecture par défaut ; 34/34 avec Docling ; 32/34 au réglage serré ; 4/4 refus partout | [Vérifié] (annexe [A1](A1-evaluation-qualite-et-performances.md#2-résultats)) |
| Temps d'attente | médiane 58 à 66 s par défaut, 24 s requêtes coupées, 1,3 s réflexion coupée (95 % sous 3,1 s) ; indexation des 9 fichiers par Docling 51 s, dont 14 s pour le scan de 2 pages | [Vérifié] (annexe [A1](A1-evaluation-qualite-et-performances.md#4-temps-et-mémoire)) |

Première question et questions suivantes : le banc pose chaque question dans une conversation neuve, sans historique ; aucune différence de temps entre la première et les suivantes n'apparaît dans les journaux (Q01 du banc sans réflexion : 1,7 s ; Q02 : 1,0 s). [Vérifié] ([banc sans réflexion](../../banc-essai/resultats/open-webui/banc-2026-11-13-sans-reflexion.json)) Les trois modèles permanents restent chargés ; seul `gemma-4-e4b` se charge à la demande. [Source]

## 4. Budget de contexte et volume de documents

Le modèle `chat` accepte 16 384 jetons par requête : consigne, passages, historique, réflexion et réponse compris. [Source]

| Poste | Jetons |
|---|---|
| question, consigne de citation et 10 passages (question Q01) | 2 093 mesurés [Vérifié] ([essai-minimal-api](../../banc-essai/resultats/open-webui/essai-minimal-api-2026-11-13.json), `usage`) |
| réflexion et réponse (question Q01) | 1 458 mesurés [Vérifié] |
| total d'une question isolée | 3 551, soit 22 % de la fenêtre [Estimation] (3 551 / 16 384) |
| reste pour l'historique d'une conversation | environ 12 800 [Estimation] (16 384 − 3 551) |

- **Mode passages (par défaut)** : seuls « Top K » passages de 1 024 caractères au plus partent au modèle, quelle que soit la taille de la base. Le nombre de documents n'est donc pas limité par le contexte, seulement par le disque. [Source] (annexe [A5](A5-fonctionnement-interne.md))
- **Mode texte intégral** (« Mode avec injection complète dans le contexte », [chapitre 08](../manuel/08-regler-la-lecture-des-documents.md)) : tout le texte des documents part au modèle. Place disponible : 16 384 − environ 500 de consigne − environ 4 000 réservés à la réflexion et à la réponse = 11 884, soit environ 11 900 jetons, environ 47 500 caractères à 4 caractères par jeton, une quinzaine de pages de 3 000 caractères. [Estimation] Le corpus d'essai entier (9 808 caractères lus par Docling, somme des lignes d'indexation du [journal du banc Docling](../../banc-essai/resultats/open-webui/banc-2026-11-13-docling-rerank.log)) tiendrait, soit environ 2 500 jetons. [Estimation] Non passé au banc. [À tester]
- **Réglage serré** (« Top K » 3) : il réduit le texte envoyé, mais perd deux réponses sur 34 (annexe [A1](A1-evaluation-qualite-et-performances.md#3-ce-qui-fait-réussir-ou-échouer)) ; avec 16 384 jetons, la place ne manque pas pour 10 passages : il n'est pas utile. [Vérifié] pour la perte ; [Estimation] pour la conclusion.

## 5. Modèles

- Open WebUI utilise les quatre modèles du service central sous leurs noms fixes : `chat` pour les réponses et les tâches, `embed` pour les vecteurs, `rerank` pour le tri, `transcribe` pour la dictée et les fichiers audio. [Vérifié] (champ `config` des bancs ; transcription du MP3 au [banc Docling](../../banc-essai/resultats/open-webui/banc-2026-11-13-docling-rerank.log)) Aucun modèle n'est téléchargé par Open WebUI au démarrage. [Vérifié] ([premier-demarrage](../../banc-essai/resultats/open-webui/premier-demarrage-2026-11-13.log), [relecture](../../banc-essai/resultats/open-webui/relecture.md))
- La réflexion de `chat` se coupe depuis Open WebUI, sans toucher au service : réglage personnalisé `chat_template_kwargs` = `{"enable_thinking": false}` sur un modèle personnalisé ([chapitre 07](../manuel/07-assistant-lie-a-une-base.md)). Effet mesuré : 34/34, médiane de 24 s à 1,3 s. [Vérifié]
- Un second modèle de réponse est exposé sans modification du service : `gemma-4-e4b` (5,3 Go de carte graphique de plus que Qwen3.5-4B [Source]). Il est listé par le service ([santé du service](../../banc-essai/resultats/open-webui/sante-llm-central-2026-11-13-debut.log)) [Vérifié] ; il n'a pas été passé au banc. [À tester]
- Un modèle plus léger, pour situer un plancher de qualité, demande une modification de LLM-Service : proposition inscrite dans les décisions en attente du [journal](../journal.md#décisions-en-attente).

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| WSL ralentit fortement pendant une indexation | Docling au plus fort (2,4 Go) et service central chargé | indexer par petits lots ; `free -m` ; arrêter Docling hors indexation |
| réponses de plusieurs minutes | profil `cpu`, réflexion et génération des requêtes actives | couper « Génération de requête de RAG » et la réflexion (annexe [A1](A1-evaluation-qualite-et-performances.md#6-préconisations)) |
| la carte graphique est pleine | `gemma-4-e4b` chargé en plus des trois modèles permanents | ne pas le choisir sur une carte de moins de 16 Go [Estimation] |

## Sources

- LLM-Service, branche `service-llamacpp`, commit `8568e75` (12 novembre 2026) : `README.md`, section « Mesures » (« Carte graphique » et « Processeur seul ») et tableau des modèles ; `mesures/cpu/memoire-vive-conteneurs.txt`, `mesures/cpu/banc-chat-partiel.md`, `mesures/gpu/memoire-vive-cache-ram-2048.txt`.
- Bancs : [banc-essai/resultats/open-webui/](../../banc-essai/resultats/open-webui/) (`banc-2026-11-13-*.json`).
- Diagnostic de la machine : [diagnostic-2026-11-13.json](../../banc-essai/resultats/machine/diagnostic-2026-11-13.json).
