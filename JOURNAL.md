# Journal — Open WebUI

Mission : `kit/PROMPT.md` pour la fiche `kit/fiches/05-open-webui.md`. Une entrée par étape (date, phase, fait, résultat, fichiers, prochaine étape).

## Décisions en attente

1. LLM-Service : modèle de réponse plus léger pour situer un plancher de qualité. Hors mission (modification de LLM-Service).

### 2026-11-13 09:00 — Phase A : diagnostic de la machine et santé du service central

- Fait : `outils/communs/llm_central_sante.sh --essai` en début de session : `chat`, `embed`, `rerank`, `transcribe` et alias listés, une requête réussie par usage (`outils/resultats/open-webui/sante-llm-central-2026-11-13-debut.log`).
- Kotaemon (banc précédent) arrêté par son `outils/kotaemon/arreter.sh` (données conservées) avant de commencer.
- `outils/communs/diagnostic.sh` : `outils/resultats/machine/diagnostic-2026-11-13.json`. Machine du profil B (Ryzen 5 9600X, 32 Go dans WSL, RTX 4060 Ti 16 Go, pilote 616.92), Docker 29.9.3, Compose 5.7.0, 530 Go libres, service central en profil `gpu`.
- Versions (`outils/communs/versions.py`) : Open WebUI v0.13.3 (8 novembre 2026) dernière stable ; docling-serve v1.38.2. Image `ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158e6558eeb980bc828e0f1b30238ad24d82ed84d5e5eda1dab2a082f14` (4,59 Go, 85 s de téléchargement).
- Prochaine étape : cadrage (sous-agent sur le code au tag), compose et installation.

### 2026-11-13 09:30 — Phases C et D : cadrage, installation, branchement, essai minimal

- Cadrage par sous-agent sur le code au tag (`outils/resultats/open-webui/cadrage-source-v0.13.3.md`) ; relecture consignée (`relecture.md`). Points clés : réglages lus dans l'environnement au premier démarrage puis gardés en base ; écriture des réglages de recherche par `/api/v1/retrieval/config/update` ; reranker externe compatible `/v1/rerank`, actif seulement en recherche hybride ; dans l'interface, les bases passent par l'appel d'outils natif.
- Installation `outils/open-webui/installer.sh` : 35 s, prêt en 24 s, 969 Mio au repos, port `127.0.0.1:3000` seulement (`installation-2026-11-13.log`) ; aucun modèle téléchargé au premier démarrage (`premier-demarrage-2026-11-13.log`). Interface en français d'emblée.
- Compte administrateur créé à la souris (scénario `captures/c03_premiers_pas.py premier_compte`) ; identifiants fictifs dans `donnees/IDENTIFIANTS-LOCAUX.txt`.
- Configuration effective vérifiée par l'API : connexion OpenAI `http://llm-central:8080/v1` (9 modèles listés), embeddings `openai`/`embed`, transcription `openai`/`transcribe`, synthèse vocale du navigateur.
- Essai minimal API (`essai-minimal-api-2026-11-13.json`) : base, rapport PDF (2,1 s), question Q01 : « 48,6 M€ [1] », sources avec page, 53 s (réflexion de 1 458 jetons).
- Constat : le PDF scanné est refusé à l'ajout dans une base avec l'extraction par défaut (« The content provided is empty »).
- Prochaine étape : banc sans puis avec reranker ; plan du manuel ; carte de l'interface.

### 2026-11-13 11:00 — Phases E et F en cours : bancs, captures, chapitres

- Bancs (`outils/open-webui/serie_banc.sh`, `banc.py`) : `defaut-sans-rerank` 28/34, 4/4 pièges, p50 60 s ; `hybride-rerank` (`--rerank` : recherche hybride + `http://llm-central:8080/v1/rerank`, preuve `preuve-reranker-externe-2026-11-13.log`) 28/34, 4/4, p50 66 s. Les 6 échecs = scan refusé par la lecture par défaut (Q15-18, Q30-31).
- En cours (arrière-plan) : `docling-rerank` sur base `Banc-docling` réindexée. À faire ensuite : banc `taches` (génération des requêtes de recherche coupée, `--taches '{"ENABLE_RETRIEVAL_QUERY_GENERATION": false}'`) et banc serré (`--reglages '{"TOP_K": 3}'`) pour la phase G. Chaque question déclenche 3 recherches (réécriture par le modèle de tâche avec réflexion) : cause principale de la latence.
- Réglages actuels de l'instance (faits à la souris, chapitre 08) : Docling `http://rag-docling-serve:5001`, recherche hybride, reranker externe `rerank`. Scan lu par Docling en 8,9 s (`docling-scan-2026-11-13.log`) et ajouté à « Démo Vélanor ».
- État de l'instance : admin Claire Admin, utilisateur Julien Moreau, groupe « Équipe production » (chat et Démo Vélanor partagés en lecture) ; modèles actifs `chat` et `gemma-4-e4b` ; base « Démo Vélanor » (9 fichiers) ; prompt `/synthese` ; outil « Stocks Vélanor » ; filtre « Mention de source interne » (désactivé) ; serveur MCP « Vélanor MCP » (`outils/open-webui/mcp.sh`, conteneur `rag-mcp-velanor`) ; automatisation « Point qualité du lundi » (quotidienne 9 h, à mettre en pause en fin de mission) ; canal `atelier-nantes` ; note « Réunion qualité du 13 novembre » ; souvenir en mémoire ; clés API autorisées, clé créée pour l'admin.
- Captures faites : 03 (12), 04 (5), 05 (11), 08 (6), 10 (7, menu de note à réannoter), 11 (13, partie création), 13 (9), 14 (15), 15 (13), carte (45). Scénarios dans `outils/open-webui/captures/` (socle `ui.py` : `reglages()`, `onglet()`, `champ()`, `el()`, `autre_session()`).
- Chapitres écrits (non commités, `verifier_docs.py` pas encore à 0) : 02, 03, 04, 05, 13, 14, 15, 18 ; `docs/open-webui/README.md` (plan 01-18 + A1-A6) ; `annexes/carte-interface.md` ; `annexes/A5`.
- Reste : captures avec modèle 06 (scénario `c06_interroger.py` prêt), 07 (assistant lié à une base), 09 (conversations, plusieurs modèles), 11 (usage outil/MCP/filtre dans le chat), 12 (voix : faux micro Chromium + `transcribe` ; SearXNG facultatif), 10 (conversation avec une note, test mémoire), 13 (lancer l'automatisation) ; chapitres 01, 06-12, 16, 17 ; annexes A1-A4, A6 ; exemples API `exemples/open-webui/` + `sorties_verifiees.txt` ; README racine, `docs/README.md`, `docs/glossaire.md` (copié, à compléter), `outils/README.md` ; jeu de démonstration (3 conversations citées), ménage ; relecture novice et adversariale ; RAPPORT ; commit final.

### 2026-11-13 15:30 — Phase E/F : banc Docling, chapitre 08, captures 07 et 09, reprises

- Banc `docling-rerank` (base `Banc-docling` réindexée par Docling, recherche hybride, `rerank`) : **34/34**, 4/4 pièges, 34 citations du bon document, p50 58 s, p95 115 s, indexation 51 s (scan 13,9 s), pic RAM application 4,0 Go (dont Docling 2,4 Go), VRAM 9,7 Go. Le scan (Q15-18) et les questions multi-documents passent.
- Banc `taches` (génération des requêtes de recherche coupée) en cours ; latences visiblement divisées par deux.
- Outil commun `annoter.py` : masques posés après l'annotation et sans défilement (un masque faisait défiler la fenêtre et décalait les pastilles). Revue visuelle des 131 captures par sous-agent : aucun secret visible ; 5 annotations fautives reprises par `captures/retouches.py` (05/03, 10/01, 14/03, 15/01 ; 11/02 lisible, gardée).
- Chapitre 08 rédigé (7 captures, dont « Zone de danger » › « Réindexer », sans clic). Seuil « Full Text Threshold » : fichiers joints seulement (cadrage).
- Chapitre 07 : assistant « Assistant qualité Vélanor » (base `chat`, base « Démo Vélanor », consigne, partagé en lecture à « Équipe production ») ; reste l'étape `utiliser` (modèle). Identifiant généré sans accents : `assistant-qualit-vlanor`.
- Chapitre 09 : menu d'une conversation (Partager, Télécharger, Renommer, Marquer comme non lu, Épingler, Cloner, Déplacer quand un dossier existe, Archiver, Supprimer), renommage « Chiffre d'affaires 2025 », épingle, dossier « Questions rapport annuel » (glisser-déposer), partage (Privé, « Copier le lien »), téléchargement PDF/texte/JSON (PDF obtenu), recherche. Restent : comparaison en écran partagé (modèle), archive.
- Prochaine étape : fin du banc `taches`, banc serré `TOP_K 3`, puis captures avec modèle (06, 07 utiliser, 09 comparer, 10, 11, 12, 13).

### 2026-11-13 16:30 — Phase F/G : derniers bancs et captures avec le modèle

- Bancs : `serre` (TOP_K et TOP_K_RERANKER 3) 32/34, p50 17 s (Q01 tableau et Q30 multi-documents manquées) ; `sans-reflexion` (`chat_template_kwargs.enable_thinking=false` dans chaque requête, option `--corps` de banc.py) **34/34, 4/4, p50 1,3 s, p95 3,1 s**. Réglages remis : TOP_K 10, génération des requêtes de RAG coupée (recommandée).
- Réflexion coupée aussi par l'interface : réglage personnalisé `chat_template_kwargs` = `{"enable_thinking": false}` sur l'assistant (capture 07/12) ; réponse en 10 s attente comprise, sans étape « Réflexion ».
- Captures avec modèle faites : 06 (8), 07 (13), 09 (11), 10 (10), 11 (20), 12 (6), 13 (13), 17 (4).
- Constats : titres automatiques des conversations parfois en anglais (« Stock Trends ») ; un premier essai d'outils où `chat` a prévu les appels puis répondu sans les faire, chiffres inventés (8 au lieu de 238, 12 au lieu de 10), réussi au second essai (`essai-outils-filtre-2026-11-13.json`) ; la mention ajoutée par un filtre (outlet) est enregistrée dans la conversation mais n'apparaît pas à l'écran ; serveur MCP arrêté : seule une ligne « Failed to connect to MCP server » et une réponse « je ne trouve pas » ; Docling arrêté : « HTTPConnectionPool… NameResolutionError » à l'ajout ; dictée : micro seulement en contexte sûr (127.0.0.1 ou *.localhost), transcription avec erreurs (« VVTSEC ») ; automatisation sans base : réponse non tirée des documents ; une croix rouge sur « Exploré » signale un appel d'outil échoué puis repris.
- SearXNG : hors périmètre (fiche : facultatif) ; chapitre 12 montre la page « Recherche Web » désactivée.
- Prochaine étape : rédaction 06, 07 (fin), 09 (fin), 10, 11, 12, 13 (fin), 17, 01, 16 ; annexes A1-A4, A6 ; exemples API ; jeu de démonstration ; ménage.

### 2026-11-13 18:00 — Phase H : rédaction terminée, relectures

- Rédaction : chapitres 01, 06, 07, 09 à 12, 16, 17 ; annexes A1, A2, A6 (sous-agent), A3 et exemples exécutés (sous-agent : 6 exemples, ménage fait, constat : un assistant ne consulte sa base par l'API qu'avec `params.function_calling = "legacy"`), A4 (sauvegarde à froid `sauvegarder.sh` 6,1 Mo, restauration vérifiée sur une instance à part `essai_restauration.sh` en 127.0.0.1:3001, supprimée ensuite) ; glossaire de la série fusionné (77 termes) ; README, `docs/README.md`, `outils/README.md`.
- Jeu de démonstration : trois cas pratiques (chapitre 16) faits à la souris, conversations gardées. Ménage : 3 conversations d'essai supprimées (`menage-2026-11-13.log`) ; accès de `bge-m3` au groupe retiré (il était resté partagé).
- Relecture novice 1 : 43 remarques, toutes traitées (renvois, étapes manquantes, fenêtre « Variables d'entrée » des prompts capturée, archivage déplacé après la comparaison, captures réannotées : 13/13, 14/09-10 sur `chat`, 15/05 et 15/10, 11/15 et 11/17, 16/01 ; conventions des masques dans le README du manuel).
- Relecture adversariale : 25 points, appliqués (preuves citées, étiquettes requalifiées, calculs arrondis, carte : Skills, sous-agents et réglages personnels d'affichage « Non couvert »). Correction de fond : aucune question au modèle par une capture pendant un banc (bancs en heure de Paris, notes de captures en UTC).
- `verifier_docs.py` : 0 point. Relecture novice 2 en cours.

### 2026-11-13 19:30 — Phase H : clôture

- Relectures novice 2 à 5 : 23, 4, 5 puis **0 remarque** (cinquième lecteur : « Aucune remarque »). Corrections : renvois d'étapes, chemin Windows vers le corpus, relecture d'un document par retrait et remise (au lieu de « Réindexer »), captures 14/10 reprise après retrait du partage de `bge-m3`, légendes de captures prises à un autre moment, glossaire (Bearer, JSON, Collection, RAG, Skills, OpenAPI, Exploré, image).
- Vérifications finales : `curl http://127.0.0.1:3000` → HTTP 200 (version 0.13.3) ; aucun port publié hors de 127.0.0.1 ; `verifier_docs.py` 0 point ; fichiers attendus présents. Instance laissée en marche (Open WebUI, Docling, serveur MCP d'essai ; automatisation en pause).
- Mission terminée.

### 2026-11-13 17:40 — Clôture : deux preuves non affichables

- Contrôle `--essai` du début de session : fait à 08:56, sortie dans `outils/resultats/open-webui/sante-llm-central-2026-11-13-debut.log` (versé par `c9cd08c` à 09:00) ; la sortie d'origine n'est plus visible dans la conversation après la compaction du contexte. Relance de fin de session réussie (mêmes réponses).
- Relecture novice : cinquième lecteur sans remarque, détail par chapitre (156 renvois de captures) ; trois captures tirées au hasard affichées (§10.8) ; l'affichage des 153 captures dans la conversation n'a pas été fait (taille du contexte).
- Tous les autres critères de fin sont prouvés dans la conversation. Mission close de mon côté.

### 2026-11-13 — Uniformisation de la série

- `docs/README.md` remplacé par l'index commun aux cinq dépôts (Open Notebook, RAGFlow, AnythingLLM, Kotaemon, Open WebUI) : modèles utilisés, services déportables (OCR, audio, reranker), comparatif à deux lignes par solution (défaut, meilleur réglage). Chiffres repris des résultats bruts du 12 et du 13 novembre, aucun nouveau banc.
- README : section « Résultats » au même format que les autres dépôts, « Le parcours » placé juste après le sommaire.
- `verifier_docs.py` : 0 point.
