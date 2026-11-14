# Relecture avant installation — Open WebUI v0.13.3

Date : 13 novembre 2026. Code relu au tag `v0.13.3` (commit b0e6098e) par sous-agent, en lecture seule ; synthèse détaillée avec références `fichier:ligne` dans `cadrage-source-v0.13.3.md`.

## Ce qui a été relu

| Élément | Points relevés | Conséquence pour l'installation |
|---|---|---|
| `docker-compose.yaml` officiel | deux services (`ollama`, `open-webui`), étiquette `main`, port `3000:8080` publié sur toutes les interfaces, `WEBUI_SECRET_KEY` vide, bloc `build` | `outils/open-webui/compose.yml` : service `ollama` retiré, image figée `v0.13.3@sha256:46b5…2f14`, port `127.0.0.1:3000:8080`, secret généré par `installer.sh` |
| `Dockerfile`, `backend/start.sh` | conteneur exécuté en root ; modèles locaux (MiniLM-L6-v2, Whisper base, tiktoken) déjà dans l'image sous `/app/backend/data/cache` ; secret généré hors volume s'il manque | volume `donnees/open-webui/data` ; secret fixé dans `donnees/open-webui/options.env` ; embeddings et transcription confiés au service central (aucun téléchargement : `premier-demarrage-2026-11-13.log`) |
| `backend/open_webui/config.py`, `env.py` | réglages lus dans l'environnement au premier démarrage seulement, puis gardés en base (table `config`) ; défauts des connexions OpenAI, embeddings et transcription vers `api.openai.com` | toutes les adresses et clés du service central renseignées par variables dans le compose ; Ollama coupé (`ENABLE_OLLAMA_API=false`) |
| `routers/retrieval.py`, `retrieval/utils.py` | reranker externe : `POST` sur l'URL donnée, corps `{model, query, documents, top_n}`, lecture `results[].index` et `relevance_score` ; utilisé seulement avec la recherche hybride | compatible avec la route `/v1/rerank` du service central (`http://llm-central:8080/v1/rerank`, modèle `rerank`) |
| `routers/files.py`, `routers/knowledge.py` | traitement des fichiers en tâche de fond, statut par `/api/v1/files/{id}/process/status` ; ajout à une base refusé si le contenu est vide | adaptateur du banc `outils/open-webui/banc.py` |
| `LICENSE`, `LICENSE_HISTORY` | BSD 3 clauses et clause de marque (au-delà de 50 utilisateurs sur 30 jours, marque « Open WebUI » non modifiable sans accord) ; code ancien sous MIT puis BSD 3 | marque laissée intacte ; contrainte expliquée dans l'annexe A4 |
| Image `quay.io/docling-project/docling-serve-cpu:v1.38.2` | déjà relue et essayée au banc Kotaemon (`kit/PROMPT.md` §11) ; service HTTP `/v1/convert/file`, sans clé | lancée sur le réseau `llm-net`, sans port publié, nom `rag-docling-serve` |

## Connexions sortantes repérées

- Vérification de nouvelle version et appels à Hugging Face : coupés par `OFFLINE_MODE` (essai à part, chapitre exploitation).
- Connexions par défaut à `api.openai.com` (chat, embeddings, transcription, synthèse vocale, temps réel) : chat, embeddings et transcription remplacés par le service central dès le premier démarrage ; synthèse vocale laissée sur le moteur du navigateur (aucun appel) ; temps réel désactivé (défaut).
- Aucun clic de test sur une connexion en ligne n'a été fait.
