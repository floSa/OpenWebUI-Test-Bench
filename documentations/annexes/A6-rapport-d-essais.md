# A6. Rapport d'essais

> **Objet** : décrire comment ce manuel a été produit et vérifié : méthode, machine, versions, liste des essais avec leur preuve, constats et incidents, ce qui n'a pas été vérifié, sens des étiquettes.
> **Prérequis** : aucun ; renvoie aux autres annexes et aux résultats bruts de `banc-essai/resultats/open-webui/`.
> **Version décrite** : Open WebUI 0.13.3 (image `ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158…2f14`, code relu au commit `b0e6098e`), docling-serve 1.38.2 (`quay.io/docling-project/docling-serve-cpu:v1.38.2@sha256:7a480a16…`), essais du 13 novembre 2026.
> **Statut des informations** : [Vérifié] observé sur la machine d'essai, avec son résultat brut ; [Source] lu dans le code ou dans une documentation ; [Estimation] calcul expliqué ; [À tester] non essayé.
> **Précautions** : les identifiants de démonstration sont dans `donnees/IDENTIFIANTS-LOCAUX.txt` (non versionné) ; la clé du service de modèles reste dans `service/.env`. L'export de configuration d'Open WebUI contient cette clé (section 4) : ne pas le diffuser.

## Sommaire

1. [Méthode](#1-méthode)
2. [Machine et versions](#2-machine-et-versions)
3. [Essais et preuves](#3-essais-et-preuves)
4. [Constats et incidents](#4-constats-et-incidents)
5. [Ce qui n'a pas été vérifié](#5-ce-qui-na-pas-été-vérifié)
6. [Étiquettes](#6-étiquettes)
7. [Dépannage](#dépannage)
8. [Sources](#sources)

## 1. Méthode

- **Cadrage par le code** : lecture du code au tag `v0.13.3` par un sous-agent, en lecture seule, références `fichier:ligne` ([cadrage-source-v0.13.3.md](../../banc-essai/resultats/open-webui/cadrage-source-v0.13.3.md)) ; relecture des composants avant installation et connexions sortantes repérées ([relecture.md](../../banc-essai/resultats/open-webui/relecture.md)). [Vérifié]
- **Installation figée** : dernière version stable relevée par `banc-essai/communs/versions.py` ([versions](../../banc-essai/resultats/open-webui/versions-2026-11-13.json)) ; image figée par empreinte ; port publié sur `127.0.0.1` seulement ; Ollama coupé ; chat, embeddings et transcription branchés sur le service central dès le premier démarrage. [Vérifié] ([installation](../../banc-essai/resultats/open-webui/installation-2026-11-13.log), [premier-demarrage](../../banc-essai/resultats/open-webui/premier-demarrage-2026-11-13.log))
- **Santé du service central** relevée en début de session et en tête de chaque banc (`banc-essai/communs/llm_central_sante.sh --essai`) ; `free -m` avant chaque banc. [Vérifié] ([santé](../../banc-essai/resultats/open-webui/sante-llm-central-2026-11-13-debut.log), en-têtes des `banc-*.log`)
- **Partie 1 à la souris** : chaque action a été faite dans l'interface par Playwright, scénarios `banc-essai/open-webui/captures/c03_*.py` à `c17_*.py` et `carte.py`, socle commun `ui.py`. Pour chaque capture : texte de la page dans `banc-essai/resultats/open-webui/captures/<chapitre>/<capture>.txt`, libellés des pastilles dans `scenario.json`, observations datées dans `notes.log`. [Vérifié]
- **Banc de 38 questions** par l'API de l'instance, six réglages (annexe [A1](A1-evaluation-qualite-et-performances.md)). [Vérifié]
- **Exemples d'API** exécutés, sorties dans `banc-essai/exemples/sorties_verifiees.txt` (annexe A3). [Vérifié]
- **Masquage** : la clé du service central n'est écrite dans aucun fichier suivi ; les captures passent par des masques posés après l'annotation ; une revue visuelle des 131 captures existant à 15 h 30, par un sous-agent, n'a relevé aucun secret visible [Vérifié] pour la revue (`documentations/journal.md`, entrée de 15 h 30, constat consigné, pas de résultat brut séparé). Les captures prises ensuite ont été contrôlées une à une à leur prise, puis relues lors de la relecture novice, qui a ouvert toutes les captures ; ces deux contrôles ne sont consignés dans aucun fichier de résultat.

## 2. Machine et versions

| Élément | Valeur | Statut |
|---|---|---|
| Machine | AMD Ryzen 5 9600X (12 cœurs logiques), 32 098 Mo dans WSL2, NVIDIA GeForce RTX 4060 Ti 16 380 Mio (pilote 616.92), 530 Go libres ; Ubuntu 24.04.5 LTS | [Vérifié] ([diagnostic](../../banc-essai/resultats/machine/diagnostic-2026-11-13.json)) |
| Docker | 29.9.3, Compose 5.7.0 | [Vérifié] ([diagnostic](../../banc-essai/resultats/machine/diagnostic-2026-11-13.json)) |
| Open WebUI | 0.13.3 (publiée le 8 novembre 2026), dernière version stable ; image de 4,59 Go, téléchargée en 85 s | [Vérifié] ([versions](../../banc-essai/resultats/open-webui/versions-2026-11-13.json), [installation](../../banc-essai/resultats/open-webui/installation-2026-11-13.log), [pull](../../banc-essai/resultats/open-webui/pull-2026-11-13.log)) |
| Docling | docling-serve 1.38.2 (27 octobre 2026), image `docling-serve-cpu` de 5,06 Go, réseau `llm-net`, sans port publié | [Vérifié] ([pull-docling](../../banc-essai/resultats/open-webui/pull-docling-2026-11-13.log), [docling-demarrage](../../banc-essai/resultats/open-webui/docling-demarrage-2026-11-13.log)) |
| Service de modèles | LiteLLM v1.109.0, llama-swap v272 (CUDA, llama.cpp b12282), speaches 0.8.3 (processeur) ; noms fixes `chat`, `embed`, `rerank`, `transcribe` et `gemma-4-e4b` à la demande ; profil `gpu` | [Vérifié] ([diagnostic](../../banc-essai/resultats/machine/diagnostic-2026-11-13.json), [santé](../../banc-essai/resultats/open-webui/sante-llm-central-2026-11-13-debut.log)) |
| Projet | 158 532 étoiles, 893 contributeurs, 2 565 commits sur 90 jours au 13 novembre 2026 ; licence non reconnue par GitHub (« NOASSERTION » : BSD 3 clauses avec clause de marque, voir [relecture](../../banc-essai/resultats/open-webui/relecture.md)) | [Vérifié] ([identite-github](../../banc-essai/resultats/open-webui/identite-github-2026-11-13.json)) |

## 3. Essais et preuves

| Essai | Résultat | Preuve |
|---|---|---|
| Installation | prête en 24 s, 35 s en tout, 969 Mio au repos, port `127.0.0.1:3000` seulement | [installation](../../banc-essai/resultats/open-webui/installation-2026-11-13.log) |
| Premier démarrage | migrations de la base, aucun modèle téléchargé | [premier-demarrage](../../banc-essai/resultats/open-webui/premier-demarrage-2026-11-13.log) |
| Réglages de recherche par défaut | relevés par l'API avant tout changement | [retrieval-config-defaut](../../banc-essai/resultats/open-webui/retrieval-config-defaut-2026-11-13.json) |
| Essai minimal par l'API | base, rapport PDF, question Q01 : « 48,6 M€ [1] », sources avec page, 2 093 jetons lus, 1 458 produits à 68 jetons/s | [essai-minimal-api](../../banc-essai/resultats/open-webui/essai-minimal-api-2026-11-13.json) |
| Docling | prêt en 14 s (16 s au redémarrage) ; scan de 2 pages lu en 8,85 s | [docling-demarrage](../../banc-essai/resultats/open-webui/docling-demarrage-2026-11-13.log), [docling-redemarrage](../../banc-essai/resultats/open-webui/docling-redemarrage-2026-11-13.log), [docling-scan](../../banc-essai/resultats/open-webui/docling-scan-2026-11-13.log) |
| Tri par `rerank` | appel « ExternalReranker:predict:model rerank » après chaque recherche hybride | [preuve-reranker-externe](../../banc-essai/resultats/open-webui/preuve-reranker-externe-2026-11-13.log) |
| Six bancs de 38 questions | 28/34 à 34/34, 4/4 refus partout ; médiane de 66 s à 1,3 s | annexe [A1](A1-evaluation-qualite-et-performances.md), `banc-2026-11-13-*.json`, `.md`, `.log` |
| Outils, serveur MCP et filtre dans une conversation | stock (238) et jours ouvrés (10) justes par les outils au second essai ; mention du filtre enregistrée dans la réponse | [essai-outils-filtre](../../banc-essai/resultats/open-webui/essai-outils-filtre-2026-11-13.json), [notes du chapitre 11](../../banc-essai/resultats/open-webui/captures/11-prompts-outils-fonctions/notes.log) |
| Serveur MCP de démonstration | prêt en 2 s ; « Connexion réussie » à la vérification dans l'interface | [mcp-demarrage](../../banc-essai/resultats/open-webui/mcp-demarrage-2026-11-13.log), [notes du chapitre 11](../../banc-essai/resultats/open-webui/captures/11-prompts-outils-fonctions/notes.log) |
| Export d'une base | archive `Démo Vélanor.zip` de 8 fichiers texte | [essai-export-base](../../banc-essai/resultats/open-webui/essai-export-base-2026-11-13.txt) |
| Export de la configuration | 22 024 caractères, contient la clé du service central (valeur non affichée) | [essai-export-config](../../banc-essai/resultats/open-webui/essai-export-config-2026-11-13.txt) |
| Assistant sans réflexion par l'interface | « Modèle mis à jour avec succès », réponse sans étape de réflexion en 10 s | [notes du chapitre 07](../../banc-essai/resultats/open-webui/captures/07-assistant-lie-a-une-base/notes.log) |
| Dictée | texte dicté par un faux micro de Chromium (extrait du message vocal du corpus), transcrit par `transcribe` | [notes du chapitre 12](../../banc-essai/resultats/open-webui/captures/12-voix-et-recherche-web/notes.log) |
| Automatisation | exécutée puis mise en pause (« En pause », prochaine exécution 14/11/2026 09:00) | [notes du chapitre 13](../../banc-essai/resultats/open-webui/captures/13-automatisations-canaux-calendrier/notes.log) |
| Erreurs du chapitre 17 | mot de passe faux, Docling arrêté, serveur MCP arrêté | [notes du chapitre 17](../../banc-essai/resultats/open-webui/captures/17-en-cas-de-probleme/notes.log) |

**Captures par chapitre** (images de `documentations/img/`) : 03 : 12 ; 04 : 5 ; 05 : 11 ; 06 : 8 ; 07 : 13 ; 08 : 8 ; 09 : 11 ; 10 : 10 ; 11 : 20 ; 12 : 6 ; 13 : 12 ; 14 : 15 ; 15 : 13 ; 16 : 3 ; 17 : 4 ; carte de l'interface : 45 ; total : 196. [Vérifié] (`ls documentations/img/<dossier> | wc -l` pour chaque dossier) Chaque dossier `banc-essai/resultats/open-webui/captures/<chapitre>/` garde le texte de la page, les pastilles et les observations correspondantes.

## 4. Constats et incidents

| Constat | Effet | Suite | Statut |
|---|---|---|---|
| PDF scanné avec la lecture par défaut | refus à l'ajout : « The content provided is empty. Please ensure that there is text or data present before proceeding. » ; six questions du banc échouent | Docling ([chapitre 08](../manuel/08-regler-la-lecture-des-documents.md)) | [Vérifié] ([capture 05/08](../../banc-essai/resultats/open-webui/captures/05-bases-de-connaissances/08-scan-refuse.txt)) |
| Génération des requêtes de RAG active par défaut | 2 ou 3 recherches et une réflexion de plus par question ; médiane de 58 s | réglage coupé (annexe [A1](A1-evaluation-qualite-et-performances.md#6-préconisations)) | [Vérifié] |
| Outils non appelés au premier essai | `chat` n'appelle que `recall_memories` et invente les chiffres (8 moteurs au lieu de 238, 12 jours ouvrés au lieu de 10) ; réussi au second essai | vérifier la ligne « Exploré … » sous la réponse | [Vérifié] ([essai-outils-filtre](../../banc-essai/resultats/open-webui/essai-outils-filtre-2026-11-13.json), [notes du chapitre 11](../../banc-essai/resultats/open-webui/captures/11-prompts-outils-fonctions/notes.log), 14:54 puis 15:02) |
| Mention ajoutée par un filtre (sortie) | enregistrée dans la conversation (« Réponse générée par l'assistant interne Vélanor. ») mais non affichée à l'écran | documenté | [Vérifié] ([essai-outils-filtre](../../banc-essai/resultats/open-webui/essai-outils-filtre-2026-11-13.json), « 20-mention : élément absent » dans les [notes du chapitre 11](../../banc-essai/resultats/open-webui/captures/11-prompts-outils-fonctions/notes.log)) |
| Serveur MCP arrêté | une seule ligne « Failed to connect to MCP server 'velanor-mcp' » dans les étapes, puis une réponse « Je ne trouve pas d'informations… » sans autre alerte | documenté au chapitre 17 | [Vérifié] ([notes du chapitre 17](../../banc-essai/resultats/open-webui/captures/17-en-cas-de-probleme/notes.log), [notes du chapitre 06](../../banc-essai/resultats/open-webui/captures/06-interroger-ses-documents/notes.log)) |
| Docling arrêté | ajout d'un fichier en échec : « HTTPConnectionPool(host='rag-docling-serve', port=5001) … NameResolutionError » | documenté au chapitre 17 | [Vérifié] ([notes du chapitre 17](../../banc-essai/resultats/open-webui/captures/17-en-cas-de-probleme/notes.log)) |
| Titres automatiques des conversations | parfois en anglais (« Stock Trends ») ou laissés au gabarit (« your concise title here ») | renommer la conversation (chapitre 09) | [Vérifié] ([capture 09/11](../../banc-essai/resultats/open-webui/captures/09-converser-au-quotidien/11-comparaison.txt), [essai-outils-filtre](../../banc-essai/resultats/open-webui/essai-outils-filtre-2026-11-13.json)) |
| Micro hors contexte sûr | « Accès au microphone refusé » quand la page n'est pas servie en contexte sûr ; dictée possible sur `127.0.0.1` ou une adresse en `.localhost` | documenté au chapitre 12 | [Vérifié] ([notes du chapitre 12](../../banc-essai/resultats/open-webui/captures/12-voix-et-recherche-web/notes.log), « contexte sûr : False » puis « True ») |
| Transcription imparfaite | « VVTSEC », « assoblage » dans le texte dicté et dans la transcription du message vocal | relire le texte dicté avant envoi | [Vérifié] ([notes du chapitre 12](../../banc-essai/resultats/open-webui/captures/12-voix-et-recherche-web/notes.log), [santé](../../banc-essai/resultats/open-webui/sante-llm-central-2026-11-13-debut.log)) |
| Automatisation sans base attachée | réponse non tirée des documents | attacher la base ou un assistant lié | [Vérifié] pour l'exécution ([notes du chapitre 13](../../banc-essai/resultats/open-webui/captures/13-automatisations-canaux-calendrier/notes.log), « Dernière exécution \| Aujourd'hui à 15:11 », « Modèle \| chat », sans base) ; contenu de la réponse : constat de `documentations/journal.md` (entrée de 16 h 30), absent des résultats bruts [À tester] |
| Export de la configuration | le fichier contient la clé du service central | ne pas diffuser l'export | [Vérifié] ([essai-export-config](../../banc-essai/resultats/open-webui/essai-export-config-2026-11-13.txt)) |
| Numéros de diapositive par Docling | décalés d'une unité par rapport à la grille du banc (Q22, Q23) | sans effet sur les réponses | [Vérifié] (annexe [A1](A1-evaluation-qualite-et-performances.md#3-ce-qui-fait-réussir-ou-échouer)) |
| Annotation des captures | un masque faisait défiler la fenêtre et décalait les pastilles ; cinq annotations fautives repérées, quatre reprises (05/03, 10/01, 14/03, 15/01) et une gardée car lisible (11/02), par `banc-essai/open-webui/captures/retouches.py` ; plusieurs autres reprises après la relecture novice | outil `annoter.py` corrigé | constat de `documentations/journal.md` (entrée de 15 h 30), sans résultat brut séparé ; reprises après la relecture novice non consignées |
| Captures pendant les bancs | aucune question à `chat` pendant un banc (les deux questions du chapitre 04, 08:53 et 08:57 UTC, tombent entre le banc par défaut et le banc hybride) ; une indexation par `embed` d'un fichier de 87 octets pendant `hybride-rerank`, effet négligeable [Estimation] ; captures des chapitres 06 à 17 qui interrogent le modèle toutes postérieures au dernier banc (14:27 UTC et après) ; bancs en heure de Paris, notes de captures en temps universel | annexe [A1](A1-evaluation-qualite-et-performances.md#5-limites-de-la-mesure) | [Vérifié] (heures des `banc-*.json` et des `notes.log`) |

## 5. Ce qui n'a pas été vérifié

- **Profil A** (sans carte graphique) : non mesuré avec Open WebUI ; temps calculés à partir des débits du service central (annexe [A2](A2-choisir-son-materiel-et-ses-modeles.md#2-profil-a--sans-carte-graphique)). [Estimation]
- **Recherche web** : SearXNG n'a pas été installé (facultatif d'après la fiche) ; le chapitre 12 montre la page « Recherche Web » désactivée (« recherche web activée : false »). [À tester]
- **Synthèse vocale du navigateur** (« Lire à voix haute ») : le bouton a été actionné, mais le son produit n'a pas été écouté. [À tester]
- **Second modèle de réponse** `gemma-4-e4b` : utilisé pour la comparaison côte à côte du chapitre 09, non passé au banc. [À tester]
- **Réflexion coupée sur des questions de calcul** : le corpus n'en contient pas. [À tester]
- **Docling sans tri `rerank`**, mode texte intégral, seuil de pertinence non nul : non passés au banc. [À tester]
- **Une seule mesure par réglage** : variabilité des réponses non chiffrée. [À tester]
- **Relecture par un lecteur novice** (partie 1, sous-agent neuf à chaque passage, sans accès au logiciel ni aux annexes) : cinq passages, 43, 23, 4, 5 puis 0 remarque ; chaque remarque corrigée (textes, renvois, captures réannotées) entre deux passages. **Relecture adversariale** (partie 2) : 25 points, appliqués (preuves citées, étiquettes requalifiées, calculs). Constat consigné dans `documentations/journal.md` et dans l'historique git (commits « corrections de la … relecture »), pas dans un fichier de résultat brut.

## 6. Étiquettes

| Étiquette | Sens | Exemple |
|---|---|---|
| [Vérifié] | constaté sur la machine d'essai ; le résultat brut est cité (fichier de `banc-essai/resultats/`) | 34/34 au banc Docling |
| [Source] | lu dans le code au tag v0.13.3 ou dans une documentation (README et mesures de LLM-Service), sans essai ici | le tri n'agit qu'avec la recherche hybride |
| [Estimation] | calcul à partir de mesures, avec le calcul écrit à côté | temps du profil A : temps du profil B × 68 / 14 |
| [À tester] | non essayé ; à confirmer avant de s'y fier | recherche web par SearXNG |

Dans la partie 1, les étiquettes ne sont pas écrites : chaque étape y a été faite à la souris et montrée par une capture, ce qui vaut [Vérifié]. Les réserves de la partie 1 sont reprises dans cette annexe.

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| un fichier de preuve cité manque | résultat regroupé dans un autre journal | chercher dans `banc-essai/resultats/open-webui/` par date ou dans `captures/<chapitre>/notes.log` |
| une capture ne correspond plus à l'interface | version différente de 0.13.3 | vérifier l'empreinte de l'image (`docker image inspect`) |
| un chiffre de banc diffère après un nouveau passage | réponses variables du modèle, réglages communs changés entre-temps | comparer le champ `config` des deux JSON |

## Sources

- Résultats bruts : [banc-essai/resultats/open-webui/](../../banc-essai/resultats/open-webui/) ; diagnostic : [banc-essai/resultats/machine/](../../banc-essai/resultats/machine/).
- Scénarios : `banc-essai/open-webui/captures/` ; installation et banc : `banc-essai/open-webui/`.
- Journal de la mission : [documentations/journal.md](../journal.md).
