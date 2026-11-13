# A1. Évaluation : qualité et performances

> **Objet** : mesurer la justesse, les citations et les temps de réponse d'Open WebUI 0.13.3 sur un jeu de 38 questions, avec six réglages successifs (lecture par défaut, recherche hybride et tri par `rerank`, lecteur Docling, génération des requêtes coupée, réglage serré, réflexion coupée), et en tirer des préconisations.
> **Prérequis** : [sommaire du manuel](../README.md) ; installation des chapitres [02](../manuel/02-installer-open-webui.md) et [03](../manuel/03-premiers-pas.md) ; réglages de lecture du [chapitre 08](../manuel/08-regler-la-lecture-des-documents.md) ; corpus et questions de `corpus/`.
> **Version décrite** : Open WebUI 0.13.3 (`ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158…2f14`), docling-serve 1.38.2 ; service LLM central en profil `gpu` (`chat` Qwen3.5-4B, `embed` bge-m3, `rerank` bge-reranker-v2-m3, `transcribe` faster-whisper-small) ; essais du 13 novembre 2026.
> **Statut des informations** : [Vérifié] résultat brut cité, dans `outils/resultats/open-webui/` ; [Source] lu dans le code ou dans la documentation du service central ; [Estimation] calcul expliqué ; [À tester] non mesuré.
> **Précautions** : un seul passage par réglage ; les réponses du modèle varient d'un passage à l'autre (section 5). Les réglages de recherche d'Open WebUI sont communs à toute l'instance : un banc change les réglages de tous les comptes pendant sa durée.

## Sommaire

1. [Méthode](#1-méthode)
2. [Résultats](#2-résultats)
3. [Ce qui fait réussir ou échouer](#3-ce-qui-fait-réussir-ou-échouer)
4. [Temps et mémoire](#4-temps-et-mémoire)
5. [Limites de la mesure](#5-limites-de-la-mesure)
6. [Préconisations](#6-préconisations)
7. [Dépannage](#dépannage)
8. [Sources](#sources)

## 1. Méthode

- **Corpus** : 9 documents d'une entreprise fictive (`corpus/MANIFEST.json`) : rapport annuel PDF de 10 pages, contrat PDF scanné de 2 pages, procédure DOCX, présentation PPTX, classeur XLSX, page HTML, note Markdown, audit PDF en anglais, message vocal MP3. [Vérifié]
- **Questions** : 38 (`corpus/questions.json`), dont 34 avec une réponse attendue (faits simples 13, tableaux 10, scan 4, anglais 2, multi-documents 3, audio 2) et 4 pièges dont la réponse n'est pas dans le corpus. [Vérifié] (`par_type` de chaque synthèse)
- **Adaptateur** : `outils/open-webui/banc.py`, lancé par `outils/open-webui/serie_banc.sh`. Il crée une base de connaissances par l'API de l'instance, y dépose les 9 fichiers (lecture, découpage et vecteurs calculés par `embed`), puis pose chaque question à `chat` par `POST /api/chat/completions`, base attachée, sans historique (une conversation neuve par question). Les réglages de recherche sont écrits avant le banc par `POST /api/v1/retrieval/config/update`, puis relus et gardés dans le champ `config` du JSON. [Vérifié] Exception : le JSON du banc par défaut ne relève pas l'état de « Génération de requête de RAG » (pas de bloc `taches`) ; ce réglage y était activé par défaut [Source] ([cadrage-source-v0.13.3.md](../../../outils/resultats/open-webui/cadrage-source-v0.13.3.md), `ENABLE_RETRIEVAL_QUERY_GENERATION`, `config.py:2400`).
- **Notation** (`outils/communs/banc/commun.py`) : exactitude par mots attendus ; refus correct sur les pièges ; avis complémentaire du modèle `chat`, réflexion coupée (« juge LLM ») ; document et page cités, relevés dans le champ `sources` de la réponse. [Vérifié]
- **Mesures** : latence de bout en bout de chaque question, médiane (p50) et 95e centile (p95) ; pic de mémoire des conteneurs (`docker stats`) ; mémoire de la carte graphique en fin de banc (`nvidia-smi`). `free -m` et `outils/communs/llm_central_sante.sh --essai` sont relevés en tête de chaque journal `banc-*.log`. [Vérifié]

## 2. Résultats

| Réglage (étiquette) | Exactes (34) | Refus pièges (4) | Juge LLM (38) | Bon document cité (34) | Bonne page / citations avec page | p50 (s) | p95 (s) | Fichier |
|---|---|---|---|---|---|---|---|---|
| lecture par défaut, recherche par vecteurs seule, sans tri (`defaut-sans-rerank`) | 28 | 4 | 32 | 30 | 18/18 | 60,1 | 106,0 | [JSON](../../../outils/resultats/open-webui/banc-2026-11-13-defaut-sans-rerank.json) |
| lecture par défaut, recherche hybride, tri `rerank` (`hybride-rerank`) | 28 | 4 | 32 | 30 | 18/18 | 66,2 | 119,5 | [JSON](../../../outils/resultats/open-webui/banc-2026-11-13-hybride-rerank.json) |
| Docling, recherche hybride, tri `rerank` (`docling-rerank`) | 34 | 4 | 36 | 34 | 22/24 | 58,3 | 114,7 | [JSON](../../../outils/resultats/open-webui/banc-2026-11-13-docling-rerank.json) |
| idem, « Génération de requête de RAG » coupée (`taches`) | 34 | 4 | 37 | 34 | 22/24 | 24,0 | 86,9 | [JSON](../../../outils/resultats/open-webui/banc-2026-11-13-taches.json) |
| idem, réglage serré : « Top K » 3 et « Top K Reranker » 3 (`serre`) | 32 | 4 | 34 | 34 | 21/24 | 17,1 | 71,1 | [JSON](../../../outils/resultats/open-webui/banc-2026-11-13-serre.json) |
| comme `taches` (« Top K » 10), réflexion de `chat` coupée (`sans-reflexion`) | 34 | 4 | 37 | 34 | 22/24 | 1,3 | 3,1 | [JSON](../../../outils/resultats/open-webui/banc-2026-11-13-sans-reflexion.json) |

[Vérifié] Chaque ligne reprend le champ `synthese` du fichier cité ; chaque fichier a sa version lisible `.md` et son journal `.log` de même nom dans [outils/resultats/open-webui/](../../../outils/resultats/open-webui/). Aucune erreur d'appel dans les six bancs (`erreurs` : 0).

Réglages communs aux six bancs (champ `config`) : « Top K » 10 et « Top K Reranker » 10 sauf au banc serré, « Seuil de pertinence » 0, découpage par défaut (1 024 caractères, chevauchement 100), embeddings `embed` par lots de 4, modèle de réponse `chat`. [Vérifié] « Génération de requête de RAG » : activée aux bancs `hybride-rerank` et `docling-rerank` (`taches.ENABLE_RETRIEVAL_QUERY_GENERATION` : true) [Vérifié], coupée ensuite [Vérifié] ; au banc par défaut, activée par défaut [Source] ([cadrage-source-v0.13.3.md](../../../outils/resultats/open-webui/cadrage-source-v0.13.3.md), `ENABLE_RETRIEVAL_QUERY_GENERATION`), non relevée dans le JSON du banc par défaut.

Résultats par type de question : [Vérifié] (`par_type`)

| Type | défaut | hybride + tri | Docling + tri | requêtes coupées | serré | sans réflexion |
|---|---|---|---|---|---|---|
| faits simples (13) | 13 | 13 | 13 | 13 | 13 | 13 |
| tableaux (10) | 10 | 10 | 10 | 10 | 9 | 10 |
| scan (4) | 0 | 0 | 4 | 4 | 4 | 4 |
| anglais (2) | 2 | 2 | 2 | 2 | 2 | 2 |
| multi-documents (3) | 1 | 1 | 3 | 3 | 2 | 3 |
| audio (2) | 2 | 2 | 2 | 2 | 2 | 2 |
| pièges (4) | 4 | 4 | 4 | 4 | 4 | 4 |

## 3. Ce qui fait réussir ou échouer

1. **Le lecteur de documents, pas le tri.** Les deux premiers bancs ont exactement les mêmes six échecs : Q15, Q16, Q17, Q18 (scan) et Q30, Q31 (multi-documents, dont une moitié de la réponse est dans le contrat scanné). Le contrat `contrat-batterix-scan.pdf` est une image de page : la lecture par défaut n'en tire aucun texte et Open WebUI refuse de l'ajouter à la base (« The content provided is empty. Please ensure that there is text or data present before proceeding. »). La base des deux premiers bancs ne compte que 8 documents sur 9. [Vérifié] ([capture 05/08](../../../outils/resultats/open-webui/captures/05-bases-de-connaissances/08-scan-refuse.txt), champ `indexation` de [defaut-sans-rerank](../../../outils/resultats/open-webui/banc-2026-11-13-defaut-sans-rerank.json) : `documents` 8)
2. **Ce que répond le modèle sans le scan** : il refuse proprement (« aucune information n'est disponible concernant le plafond des pénalités », Q17) ou répond à côté avec un autre document (Q16 : 24 jours, délai moyen constaté dans le classeur, au lieu des 21 jours du contrat). Pour Q30 et Q31, il donne la moitié trouvée ailleurs (24 jours ; score d'audit 87) et dit ne pas trouver l'autre. [Vérifié] (champ `reponse` de Q15 à Q18, Q30, Q31 dans les deux premiers JSON)
3. **Docling lit le scan** : le contrat est lu en 13,9 s (887 caractères) pendant l'indexation du banc, et les six questions passent : 34/34. [Vérifié] ([journal du banc Docling](../../../outils/resultats/open-webui/banc-2026-11-13-docling-rerank.log), lignes d'indexation) ; lecture isolée du même scan par docling-serve en 8,85 s ([docling-scan](../../../outils/resultats/open-webui/docling-scan-2026-11-13.log)). [Vérifié]
4. **Le tri `rerank`** ne change pas le score sur ce corpus (28 dans les deux cas) et ajoute 6 s à la médiane (60,1 puis 66,2 s). Il est bien appelé : le journal du conteneur montre « ExternalReranker:predict:model rerank » après chaque recherche hybride. [Vérifié] ([preuve-reranker-externe](../../../outils/resultats/open-webui/preuve-reranker-externe-2026-11-13.log)) Le tri n'agit qu'avec « Recherche hybride » activée. [Source] (`relecture.md`, `routers/retrieval.py`) L'effet de Docling sans le tri n'a pas été mesuré. [À tester]
5. **L'audio est lu** : le message vocal MP3 est transcrit par `transcribe` à l'ajout (351 caractères), et Q33, Q34 réussissent dans les six bancs. [Vérifié] ([journal du banc Docling](../../../outils/resultats/open-webui/banc-2026-11-13-docling-rerank.log), `par_type`)
6. **Les pièges** : 4/4 refus dans tous les réglages ; le modèle dit ne pas pouvoir déterminer l'information plutôt que d'inventer. [Vérifié]
7. **Le réglage serré coûte deux réponses** : avec 3 passages, Q01 (chiffre d'affaires 2025, page 3 du rapport) n'est plus retrouvée (les 3 passages gardés viennent des pages 10, 2 et 1) et Q30 ne trouve plus le délai constaté du classeur (le délai du contrat, 21 jours, est trouvé). [Vérifié] ([banc serré](../../../outils/resultats/open-webui/banc-2026-11-13-serre.json), Q01 et Q30)
8. **Les pages** : quand un passage cité porte une page, elle est juste 18 fois sur 18 avec la lecture par défaut. Avec Docling, 22 sur 24 : les deux écarts (Q22, Q23) viennent de la présentation PPTX, dont Docling numérote les diapositives avec un décalage d'une unité par rapport à la grille (2 au lieu de 3, 3 au lieu de 4) ; la bonne réponse est donnée. [Vérifié] (champ `citations` de Q22 et Q23 dans [docling-rerank](../../../outils/resultats/open-webui/banc-2026-11-13-docling-rerank.json)) La cause du décalage n'a pas été cherchée. [À tester]

## 4. Temps et mémoire

**D'où vient l'attente.** Avec les réglages par défaut, une question dans une base déclenche d'abord une « génération de requête de RAG » : `chat` réécrit la question en plusieurs requêtes de recherche (2 ou 3 dans le journal : « Starting hybrid search for 3 queries »), avec sa réflexion, avant de rédiger la réponse, elle aussi précédée d'une réflexion. [Vérifié] ([preuve-reranker-externe](../../../outils/resultats/open-webui/preuve-reranker-externe-2026-11-13.log)) Couper cette réécriture divise la médiane par 2,4 (58,3 puis 24,0 s) sans perte de qualité ; couper ensuite la réflexion de la réponse ramène la médiane à 1,3 s. [Vérifié]

| Mesure | Valeur | Statut |
|---|---|---|
| Temps de réponse, médiane | 58 à 66 s (réglages par défaut) ; 24 s (requêtes coupées) ; 17 s (serré) ; 1,3 s (requêtes et réflexion coupées) | [Vérifié] (`latence_p50_s`) |
| Temps de réponse, 95 % des questions sous | 106 à 120 s ; 87 s ; 71 s ; 3,1 s | [Vérifié] (`latence_p95_s`) |
| Génération de la réponse seule (Q01, essai minimal) | 1 458 jetons produits en 21,4 s, soit 68 jetons/s ; 2 093 jetons lus en 0,68 s | [Vérifié] ([essai-minimal-api](../../../outils/resultats/open-webui/essai-minimal-api-2026-11-13.json), `usage` et `timings`) |
| Indexation des 9 fichiers par Docling | 50,9 s, dont 13,9 s pour le scan et 10,8 s pour le rapport de 10 pages | [Vérifié] ([journal du banc Docling](../../../outils/resultats/open-webui/banc-2026-11-13-docling-rerank.log)) |
| Open WebUI au repos (juste installé) | 969 Mio | [Vérifié] ([installation](../../../outils/resultats/open-webui/installation-2026-11-13.log)) |
| Open WebUI pendant un banc (pic) | 1 440 à 1 595 Mo | [Vérifié] (`pic_ram_mo`, `rag-open-webui`) |
| Docling (pic) | 902 Mo au démarrage ; 2 393 Mo pendant l'indexation ; 1 971 à 1 978 Mo ensuite | [Vérifié] ([docling-demarrage](../../../outils/resultats/open-webui/docling-demarrage-2026-11-13.log), `pic_ram_mo`, `rag-docling-serve`) |
| Application entière (Open WebUI et Docling, pic) | 2,3 Go (lecture par défaut) à 4,0 Go (indexation Docling) | [Vérifié] (`pic_ram_application_mo` : 2 342 à 3 988 Mo) |
| Service central pendant les bancs (pic) | LiteLLM 722 à 746 Mo, llama-swap 5 262 à 5 443 Mo, speaches 1 309 à 1 364 Mo (transcription chargée), soit environ 7,5 Go | [Vérifié] (`pic_ram_mo`) |
| Mémoire de la carte graphique en fin de banc | 9 436 à 9 890 Mo sur 16 380 Mo, bureau Windows compris | [Vérifié] (`vram`) |

## 5. Limites de la mesure

- Un seul passage par réglage : une réponse peut changer d'un passage à l'autre. Les deux premiers bancs, de même résultat (28/34), ne permettent pas de mesurer cette variation. [Vérifié]
- Le banc passe par l'API, base attachée à la requête. Dans l'interface, la base est consultée par appels d'outils (« Exploré list_knowledge, view_knowledge_file, search_knowledge_files ») : chemin différent, avec des étapes en plus. [Vérifié] ([notes du chapitre 06](../../../outils/resultats/open-webui/captures/06-interroger-ses-documents/notes.log)) Les temps de l'interface peuvent donc s'écarter de ceux du banc ; l'assistant sans réflexion a répondu en 10 s, attente de stabilité de l'écran comprise. [Vérifié] ([notes du chapitre 07](../../../outils/resultats/open-webui/captures/07-assistant-lie-a-une-base/notes.log))
- Aucune question n'a été posée à `chat` par une capture pendant un banc. Les bancs sont horodatés en heure de Paris (champ `date` des `banc-*.json`, heure de fin du fichier), les `notes.log` des captures en temps universel (une heure de moins) : `defaut-sans-rerank` 08:08 à 08:50 UTC, `hybride-rerank` 08:59 à 09:45 UTC, `docling-rerank` 13:01 à 13:43 UTC, `taches` 13:43 à 14:04 UTC, `serre` 14:05 à 14:22 UTC, `sans-reflexion` 14:23 à 14:24 UTC. Les deux questions du chapitre 04 (réponses à 08:53 et 08:57 UTC) tombent entre la fin du banc par défaut et le début du banc hybride. Pendant `hybride-rerank`, le chapitre 05 a indexé par `embed` un fichier de 87 octets (`note-de-test.md`, vers 09:03 UTC) ; effet négligeable sur les temps du banc [Estimation] (un appel `embed` sur 10 passages prend 0,05 à 0,11 s d'après le README du service central, contre 66 s de médiane par question). Les captures des chapitres 06 à 17 qui interrogent le modèle sont toutes postérieures au dernier banc (14:27 UTC et après). Les autres captures prises pendant les bancs ne font que des réglages ou des lectures d'écran. [Vérifié] (champ `date` et heure des `banc-*.json` ; [notes du chapitre 04](../../../outils/resultats/open-webui/captures/04-premiere-question/notes.log), [notes du chapitre 05](../../../outils/resultats/open-webui/captures/05-bases-de-connaissances/notes.log), « Indexed text » ; [notes du chapitre 06](../../../outils/resultats/open-webui/captures/06-interroger-ses-documents/notes.log))
- Deux captures du chapitre 08 ont ouvert les réglages communs pendant un banc (13:45 UTC pendant `taches`, choix de lecteur montré puis fenêtre fermée sans « Enregistrer » ; 14:05 UTC pendant `serre`, interrupteur « Génération de requête de RAG » seulement lu). Aucune n'enregistre : étapes `extraction_seule` et `requetes` de `outils/open-webui/captures/c08_lecture.py`, sans clic sur « Enregistrer ». La configuration relue par l'API juste après la première (Docling, recherche hybride, tri `external`, Top K 10) était inchangée ; ce relevé n'a pas été enregistré dans un fichier [Estimation].
- Le juge LLM et le comptage par mots attendus divergent sur 0 à 2 questions selon le banc : aucune au banc par défaut, Q01 et Q06 au banc Docling (jugées fausses alors que le chiffre attendu y est), Q13 au banc `taches`, Q33 et Q37 au banc serré, Q33 au banc sans réflexion ; aucune au banc `hybride-rerank`. Les chiffres « Exactes » font foi. [Vérifié] (champs `exacte` et `juge_llm` de chaque question)
- La réflexion coupée n'a pas été essayée sur des questions de calcul ou de raisonnement ; le corpus n'en contient pas. [À tester]
- Un second modèle de réponse (`gemma-4-e4b`, exposé par le service central) n'a pas été passé au banc. [À tester]
- Le profil sans carte graphique n'a pas été mesuré ; ses temps sont seulement estimés dans l'annexe [A2](A2-choisir-son-materiel-et-ses-modeles.md). [À tester]

## 6. Préconisations

1. **Lire les PDF scannés avec Docling** (« Moteur d'extraction de contenu » › « Docling », serveur `http://rag-docling-serve:5001`, [chapitre 08](../manuel/08-regler-la-lecture-des-documents.md)) : c'est le seul réglage qui change le score (28 puis 34 sur 34). Sans lui, un scan est refusé à l'ajout. [Vérifié]
2. **Activer « Recherche hybride » et le tri par `rerank`** (« Moteur de ré-ranking » « Externe », `http://llm-central:8080/v1/rerank`, modèle `rerank`) : aucun gain mesuré sur ce petit corpus, mais aucune perte de qualité, et le tri n'agit qu'avec la recherche hybride. Coût : quelques secondes. [Vérifié] pour le score et l'appel du tri ; gain sur un grand corpus : [À tester]
3. **Couper « Génération de requête de RAG »** (menu du compte › « Réglages » › groupe « Administrateur » › « Interface utilisateur », section « Tâches ») : médiane de 58 à 24 s, 34/34 conservé. [Vérifié]
4. **Couper la réflexion de `chat`** pour les questions factuelles : sur un modèle personnalisé ([chapitre 07](../manuel/07-assistant-lie-a-une-base.md)), « Réglages avancés » › « Ajoutez votre réglage personnalisé », nom `chat_template_kwargs`, valeur `{"enable_thinking": false}`, puis « Enregistrer & Mettre à jour ». Au banc : 34/34, médiane 1,3 s. [Vérifié] (banc `sans-reflexion` ; réglage fait dans l'interface : [notes du chapitre 07](../../../outils/resultats/open-webui/captures/07-assistant-lie-a-une-base/notes.log), « Modèle mis à jour avec succès », réponse sans réflexion) Garder un modèle avec réflexion pour les questions de calcul. [À tester]
5. **Garder « Top K » et « Top K Reranker » à 10** : à 3, deux réponses sont perdues (Q01, Q30) pour 7 s de gagnées en médiane. Le contexte de 16 384 jetons accueille sans peine 10 passages (annexe [A2](A2-choisir-son-materiel-et-ses-modeles.md)). [Vérifié]

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `banc.py` : la base compte 8 documents sur 9 | scan refusé par la lecture par défaut | régler Docling, puis `banc.py --base Banc-docling --reindexer` |
| le tri `rerank` n'apparaît pas dans le journal du conteneur | « Recherche hybride » désactivée | la réactiver ; le tri n'agit qu'avec elle |
| latences de plus d'une minute | génération des requêtes et réflexion actives ; autre essai en parallèle | couper la génération des requêtes ; un seul essai à la fois ; `free -m` |
| un banc modifie les réglages de l'interface | réglages de recherche communs à l'instance | relire les réglages après chaque banc (champ `config`) et les remettre |

## Sources

- Résultats bruts : [outils/resultats/open-webui/](../../../outils/resultats/open-webui/) (`banc-2026-11-13-*.json`, `.md`, `.log`).
- Adaptateur : `outils/open-webui/banc.py`, `outils/open-webui/serie_banc.sh` ; banc commun : `outils/communs/banc/commun.py`.
- Relecture du code au tag v0.13.3 : [relecture.md](../../../outils/resultats/open-webui/relecture.md), [cadrage-source-v0.13.3.md](../../../outils/resultats/open-webui/cadrage-source-v0.13.3.md).
