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
