# Outils

Principe : rien n'est écrit de mémoire. Chaque affirmation des manuels vient d'un script de ce dossier et d'un résultat brut rangé dans `banc-essai/resultats/`. Les actions de la partie 1 du manuel sont faites à la souris par des scénarios Playwright, exécutés dans le conteneur officiel `mcr.microsoft.com/playwright/python` (rien à installer dans WSL). Les modèles viennent tous du service LLM central (`chat`, `embed`, `rerank`, `transcribe`) ; aucun script de ce dossier ne l'arrête ni ne le modifie. La clé `LLM_CENTRAL_KEY` reste dans `service/.env` et n'est jamais affichée.

## Communs (`banc-essai/communs/`)

| Fichier | Rôle |
|---|---|
| `diagnostic.sh` | relevé de la machine et du service LLM central → `resultats/machine/diagnostic-<date>.json` |
| `llm_central_sante.sh` | santé du service central (liste des modèles, puis un essai par usage avec `--essai`) ; lecture seule |
| `versions.py` | dernière version stable de chaque composant (GitHub) → `resultats/<solution>/versions-<date>.json` |
| `identite_github.py` | étoiles, activité, licence du projet → `resultats/<solution>/identite-github-<date>.json` |
| `banc/commun.py` | banc commun : notation, juge LLM (`chat` du service central), mémoire, sorties JSON et Markdown |
| `banc/tableau.py` | tableau Markdown des bancs (comparatif de `documentations/index-serie.md`) |
| `banc/renoter.py` | renotation d'un banc enregistré |
| `banc/tests/test_commun.py` | contrôles de la notation du banc |
| `captures/annoter.py` | rectangle rouge, pastille numérotée, masquage des secrets, capture |
| `captures/lancer.sh` | lance un scénario dans le conteneur Playwright `rag-captures` (réseau `rag-local`, clé du service transmise sans affichage) |
| `verifier_docs.py` | vérification de la documentation (liens, ancres, ton, captures, carte de l'interface) ; 0 point avant chaque commit |
| `nettoyer.sh` | suppression d'une solution (ressources `rag-<solution>` et `donnees/<solution>/`), sur confirmation |
| `nouvelle_solution.sh` | prépare le dépôt de la solution suivante |
| `generer_corpus.py`, `generer_audio.py` | corpus fictif (graine fixe) |
| `inventaire_modeles.py`, `llm_service.sh`, `llm_service_vllm.sh`, `voix.sh`, `mesure_modeles.py` | ancienne pile (Ollama, vLLM, speaches local), plus lancés ; gardés pour l'historique |

## Open WebUI (`banc-essai/open-webui/`)

| Fichier | Rôle |
|---|---|
| `compose.yml` | projet compose `rag-open-webui` : conteneur `rag-open-webui` (image figée par empreinte, `127.0.0.1:3000`, réseaux `llm-net` et `rag-local`, branchement au service central, télémétrie coupée) et service facultatif `rag-docling-serve` (profil `docling`, sans port publié) |
| `compose.sh` | `docker compose` du projet, avec le `service/.env` du dépôt pour la clé (jamais affichée) |
| `installer.sh` | installation rejouable : image, secret de session dans `donnees/open-webui/options.env`, démarrage, contrôle des ports, mesures |
| `demarrer.sh`, `arreter.sh`, `etat.sh` | exploitation courante (LLM-Service n'est ni démarré ni arrêté par ces scripts) |
| `docling.sh` | démarre ou arrête le lecteur Docling (`start` ou `stop`), joint à `http://rag-docling-serve:5001` |
| `mcp.sh` | démarre ou arrête le serveur MCP d'essai `rag-mcp-velanor` (réseau `rag-local`, lecture seule, sans port publié) |
| `client.py` | client minimal de l'API (bibliothèque standard), connexion par les identifiants fictifs de `donnees/IDENTIFIANTS-LOCAUX.txt` ; aussi en ligne de commande |
| `banc.py` | adaptateur du banc commun : base « Banc » créée par l'API, questions par `/api/chat/completions`, options `--rerank`, `--reglages`, `--taches` |
| `serie_banc.sh` | lance un banc avec une étiquette, après `free -m` et contrôle de santé du service central |
| `extensions/outil_stocks.py` | outil « Stocks Vélanor » (chapitre 11) |
| `extensions/filtre_signature.py` | filtre « Mention de source interne » (chapitre 11) |
| `extensions/serveur_mcp_velanor.py` | serveur MCP d'essai, deux fonctions sur l'entreprise fictive (chapitre 11) |
| `essais/note-de-test.md` | fichier jetable pour l'essai de retrait d'un fichier d'une base (chapitre 05) |
| `captures/ui.py`, `captures/_dom.py` | socle des scénarios (connexion, navigation, captures annotées, masquage de la clé) |
| `captures/c03_…` à `captures/c17_…` | un scénario par chapitre du manuel |
| `captures/carte.py` | texte et éléments cliquables de chaque page, pour la carte de l'interface |
| `captures/explorer.py`, `captures/explorer_clic.py` | repérage de l'interface pendant l'écriture des scénarios (sans capture annotée) |
| `captures/retouches.py` | reprise de captures dont l'annotation était fautive |

## Résultats (`banc-essai/resultats/`)

| Dossier | Contenu |
|---|---|
| `machine/` | diagnostics de la machine |
| `socle/` | mesures de l'ancienne pile (historique) |
| `open-webui/` | versions, identité du projet, cadrage, relecture, installation, essais, bancs (`banc-*.json`, `.md`, `.log`), Docling, MCP, exports, captures (texte des pages, notes, scénarios) |
| `open-notebook/`, `ragflow/`, `anythingllm/`, `kotaemon/` | bancs des solutions précédentes, pour le comparatif |
