# Cadrage technique Open WebUI v0.13.3 (lecture du code source)

- Source : `git clone --depth 1 --branch v0.13.3 https://github.com/open-webui/open-webui`, commit `b0e6098e940942281d9c83f3529ea117287a3a22` (2026-11-09 08:48:12 +0900).
- Méthode : lecture et `grep` uniquement ; aucun conteneur lancé, rien exécuté. La documentation en ligne n'a pas été consultée (le code a suffi).
- Références : `chemin:ligne`, relatives à la racine du dépôt cloné.

## 1. Image Docker

| Point | Valeur | Source |
|---|---|---|
| Image à utiliser | `ghcr.io/open-webui/open-webui:v0.13.3` (tags publiés aussi : `0.13.3`, `0.13`) | `.github/workflows/docker.yaml:98-110` (type=ref tag + semver) |
| Variantes à éviter | suffixes `-cuda`, `-cuda126`, `-ollama`, `-slim` | `.github/workflows/docker.yaml:35-53` |
| Note sur `-slim` | sans sentence-transformers ni outils locaux ; `VECTOR_DB` par défaut = `pgvector` (au lieu de `chroma`) donc exige un Postgres | `Dockerfile:144-154,164-165`, `backend/open_webui/config.py:483` |
| Port interne | `8080` (`ENV PORT=8080`, `EXPOSE 8080`) | `Dockerfile:79,215` |
| Volume | `/app/backend/data` (DATA_DIR = `backend/data`) | `Dockerfile:185`, `docker-compose.yaml:18`, `backend/open_webui/env.py:220` |
| Healthcheck | `curl --silent --fail http://localhost:${PORT:-8080}/health \| jq -ne 'input.status == true'` ; `/health` renvoie `{"status": true}` ; existe aussi `/ready` et `/health/db` | `Dockerfile:217`, `backend/open_webui/main.py:3153-3160,3199` |
| Utilisateur | `UID=0`, `GID=0` par défaut (root) ; non-root « non testé » | `Dockerfile:23-25,230` |
| Démarrage | `CMD ["bash","start.sh"]` ; uvicorn sur `0.0.0.0:8080`, 1 worker | `Dockerfile:236`, `backend/start.sh:96-110` |
| WEBUI_SECRET_KEY | si vide, `start.sh` en génère une et la stocke dans `.webui_secret_key` (dans `/app/backend`, donc hors volume : perdue si le conteneur est recréé, ce qui invalide les sessions) | `backend/start.sh:29-48` |

### Modèles embarqués et téléchargements

- À la construction de l'image standard (non slim) sont déjà téléchargés : `sentence-transformers/all-MiniLM-L6-v2` (embedding), `TaylorAI/bge-micro-v2` (embedding auxiliaire), faster-whisper `base`, encodage tiktoken `cl100k_base` — `Dockerfile:14,16,19,102-116,176-182`. Ils sont rangés sous `/app/backend/data/cache/...` (`SENTENCE_TRANSFORMERS_HOME`, `HF_HOME`, `WHISPER_MODEL_DIR`, `TIKTOKEN_CACHE_DIR`) : un volume vide monté sur `/app/backend/data` **masque ces caches** et provoque leur re-téléchargement à la première utilisation.
- Au démarrage, le modèle sentence-transformers n'est chargé **que si** `rag.embedding_engine == ''` : `get_ef()` renvoie `None` dès que le moteur vaut `openai` — `backend/open_webui/routers/retrieval.py:143-163`, appelé par `backend/open_webui/main.py:694`. Donc avec `RAG_EMBEDDING_ENGINE=openai`, rien n'est chargé ni téléchargé pour l'embedding.
- Le reranker local (CrossEncoder) n'est chargé que si la recherche hybride est active et que le moteur de reranking n'est pas `external` — `backend/open_webui/main.py:695-703`, `backend/open_webui/routers/retrieval.py:166-186`.
- Whisper local est chargé paresseusement, à la première transcription, seulement si le moteur STT est vide — `backend/open_webui/routers/audio/__init__.py:869-874`, `backend/open_webui/main.py:768`.
- Le modèle auxiliaire `TaylorAI/bge-micro-v2` est chargé paresseusement par les évaluations (classement Elo pondéré) — `backend/open_webui/routers/evaluations.py:51-66`.
- `get_model_path()` appelle `snapshot_download` ; `local_files_only = not auto_update` et forcé à `True` si `OFFLINE_MODE` — `backend/open_webui/retrieval/utils.py:1761-1797`.
- Variables utiles :
  - `OFFLINE_MODE` (défaut `false`) : positionne `HF_HUB_OFFLINE=1` et coupe `ENABLE_VERSION_UPDATE_CHECK` — `backend/open_webui/env.py:1196-1203`.
  - `RAG_EMBEDDING_MODEL_AUTO_UPDATE` (défaut `True`, forcé à faux si OFFLINE_MODE) — `backend/open_webui/config.py:1022-1024` ; idem `RAG_RERANKING_MODEL_AUTO_UPDATE` — `config.py:1049-1051`.
  - `WHISPER_MODEL` (défaut `base`), `WHISPER_MODEL_AUTO_UPDATE` (défaut faux) — `config.py:1568,1572`.
  - `ENABLE_VERSION_UPDATE_CHECK` (défaut `true`) — `env.py:1198`.
  - `SCARF_NO_ANALYTICS=true`, `DO_NOT_TRACK=true`, `ANONYMIZED_TELEMETRY=false` déjà dans l'image — `Dockerfile:94-98`.
  - `CUSTOM_NAME` (si non vide) appelle `api.openwebui.com` — `config.py:192-222` : le laisser vide.
- Recommandation pour le banc : `RAG_EMBEDDING_ENGINE=openai`, `OFFLINE_MODE=true` (aucun appel Hugging Face, pas de vérification de version), `AUDIO_STT_ENGINE=openai` si la transcription passe par LLM-Service.

## 2. Variables d'environnement

### Mécanisme de configuration persistante (nouveau en 0.13)

- La classe `PersistentConfig` a disparu. La configuration est une table `config` à une ligne par clé pointée (`rag.top_k`, `openai.api_base_urls`…) — `backend/open_webui/models/config.py:1-9,103-116`.
- Au démarrage, `seed_defaults(DEFAULT_CONFIG)` **insère seulement les clés absentes** ; « Existing DB values take precedence over defaults » — `models/config.py:248-273`, appelé par `config.py:43-46` et `main.py:391`. Conséquence : les variables d'environnement ne servent qu'au **premier démarrage** (base vide) ; ensuite la base fait foi, y compris après modification dans l'interface.
- `ENABLE_PERSISTENT_CONFIG` (défaut `True`) — `config.py:3421-3428`. À `False`, toutes les lectures renvoient les valeurs d'environnement (`Config.DEFAULTS`) et les écritures de l'interface ne vont qu'en mémoire (perdues au redémarrage) — `models/config.py:131-145,206-213`.
- `ENABLE_OAUTH_PERSISTENT_CONFIG` (défaut `False`) : les clés `oauth.*` viennent toujours de l'environnement — `config.py:3422`.
- Un ancien `config.json` dans DATA_DIR est importé puis renommé `old_config.json` — `config.py:84-90`.
- La table de correspondance variable → clé est le dictionnaire `DEFAULT_CONFIG` — `config.py:2960-3418`.

### Connexions et comptes

| Variable | Défaut | Clé / remarque | Source |
|---|---|---|---|
| `ENABLE_OPENAI_API` | `True` | `openai.enable` | `config.py:309,2970` |
| `OPENAI_API_BASE_URL` | `''` → `https://api.openai.com/v1` | | `config.py:313-323` |
| `OPENAI_API_BASE_URLS` | = `OPENAI_API_BASE_URL` ; liste séparée par `;` | `openai.api_base_urls` | `config.py:331-337,2972` |
| `OPENAI_API_KEY` / `OPENAI_API_KEYS` | `''` ; liste `;` alignée sur les URL | `openai.api_keys` | `config.py:312,325-328,2971` |
| `OPENAI_API_CONFIGS` | `{}` (JSON : prefix_id, model_ids, provider…) | `openai.api_configs` | `config.py:339-348`, `models/config.py:24-58` |
| Piège | après lecture, `OPENAI_API_KEY` est **réécrite** avec la clé associée à `api.openai.com` (donc `''` ici) et `OPENAI_API_BASE_URL` remise à `https://api.openai.com/v1` ; or `RAG_OPENAI_API_BASE_URL`/`KEY` et `AUDIO_STT_OPENAI_API_BASE_URL`/`KEY` prennent ces valeurs comme défaut : **il faut les renseigner explicitement** | | `config.py:350-357,1108-1109,1586-1588` |
| `ENABLE_OLLAMA_API` | `True` (à mettre à `False` ; sinon l'image vise `http://host.docker.internal:11434`) | `ollama.enable` | `config.py:229,242-251,2967` |
| `ENABLE_DIRECT_CONNECTIONS` | `False` | onglet utilisateur Connexions | `config.py:224` |
| `WEBUI_SECRET_KEY` | `''` ; arrêt si vide avec auth active (start.sh la génère) | | `env.py:774-800` |
| `WEBUI_AUTH` | `True` | | `env.py:765` |
| `ENABLE_SIGNUP` | `True` (forcé `False` si pas d'auth) ; repassé à `False` automatiquement après création du premier compte (admin) | `ui.enable_signup` | `config.py:1687`, `routers/auths.py:825-829` |
| `ENABLE_LOGIN_FORM` | `True` | | `config.py:1689` |
| `DEFAULT_USER_ROLE` | `pending` | | `config.py:1749` |
| `WEBUI_ADMIN_EMAIL` / `WEBUI_ADMIN_PASSWORD` / `WEBUI_ADMIN_NAME` | `''`/`''`/`Admin` : crée l'admin au démarrage si aucun utilisateur | | `env.py:808-810`, `main.py:414-418` |
| `DEFAULT_LOCALE` | `''` (sinon langue du navigateur, repli `en-US`) ; `fr-FR` existe | `ui.default_locale` | `config.py:1695`, `src/routes/+layout.svelte:1362-1371` |
| `ENABLE_API_KEYS` | **`False`** (à activer pour les clés `sk-…`) | `auth.enable_api_keys` | `config.py:2566,3343` |
| `ENABLE_API_KEYS_ENDPOINT_RESTRICTIONS` / `API_KEYS_ALLOWED_ENDPOINTS` | `False` / `''` | | `config.py:2572-2580` |
| `USER_PERMISSIONS_FEATURES_API_KEYS` | `False` (les admins passent outre) | | `config.py:1963`, `routers/auths.py:1497-1505` |
| `BYPASS_MODEL_ACCESS_CONTROL` | `False` | | `env.py:842` |
| `JWT_EXPIRES_IN` | `4w` | | `config.py:2582` |

### RAG

| Variable | Défaut | Source |
|---|---|---|
| `RAG_EMBEDDING_ENGINE` | `''` (= sentence-transformers local) ; valeurs `openai`, `ollama`, `azure_openai` | `config.py:1011`, `retrieval/utils.py:1104-1120` |
| `RAG_EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | `config.py:1017` |
| `RAG_OPENAI_API_BASE_URL` / `RAG_OPENAI_API_KEY` | voir piège ci-dessus ; appel `POST {url}/embeddings` corps `{"input": [...], "model": ...}` | `config.py:1108-1109`, `retrieval/utils.py:888-950` |
| `RAG_EMBEDDING_BATCH_SIZE` | `1` (alias `RAG_EMBEDDING_OPENAI_BATCH_SIZE`) | `config.py:1028-1030` |
| `ENABLE_ASYNC_EMBEDDING` / `RAG_EMBEDDING_CONCURRENT_REQUESTS` | `True` / `0` | `config.py:1032-1034` |
| `RAG_EMBEDDING_QUERY_PREFIX` / `_CONTENT_PREFIX` | `None` | `config.py:1036-1038` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` / `CHUNK_MIN_SIZE_TARGET` | `1024` / `100` / `0` | `config.py:1074-1078` |
| `RAG_TEXT_SPLITTER` | `''` (caractères) ; `ENABLE_MARKDOWN_HEADER_TEXT_SPLITTER` `True` | `config.py:1064-1066` |
| `RAG_TOP_K` / `RAG_TOP_K_RERANKER` | `10` / `10` (3 avant 0.13.1) | `config.py:957-958`, `CHANGELOG.md:164` |
| `RAG_RELEVANCE_THRESHOLD` | `0.0` | `config.py:959` |
| `RAG_HYBRID_BM25_WEIGHT` | `0.5` | `config.py:960` |
| `ENABLE_RAG_HYBRID_SEARCH` | `False` | `config.py:962` |
| `RAG_RERANKING_ENGINE` | `''` (CrossEncoder local) ou `external` | `config.py:1042` |
| `RAG_RERANKING_MODEL` | `''` | `config.py:1044` |
| `RAG_EXTERNAL_RERANKER_URL` / `_API_KEY` / `_TIMEOUT` | `''` | `config.py:1057-1061` |
| `RAG_RERANKING_BATCH_SIZE` | `32` | `config.py:1055` |
| `BYPASS_EMBEDDING_AND_RETRIEVAL` | `False` | `config.py:954` |
| `RAG_FULL_CONTEXT` | `False` (libellé UI : « Always Use Full Text ») | `config.py:968`, `CHANGELOG.md:169` |
| `RAG_FULL_TEXT_CHAR_THRESHOLD` | `50000` : un **fichier** joint (type `file`) dont le texte fait moins de 50 000 caractères est injecté en entier au lieu d'être découpé ; ne s'applique pas aux bases (`collection`) | `config.py:969-977`, `retrieval/utils.py:1398-1430,1588` |
| `CONTENT_EXTRACTION_ENGINE` | `''` (chargeurs internes) ; `tika`, `docling`, `datalab_marker`, `document_intelligence`, `mineru`, `mistral_ocr`, `paddleocr_vl`, `external` | `config.py:847`, `retrieval/loaders/main.py:554-702` |
| `DOCLING_SERVER_URL` / `DOCLING_API_KEY` | `http://docling:5001` / `''` | `config.py:916-918` |
| `DOCLING_PARAMS` | `{}` (JSON) ; ajouté tel quel aux champs du formulaire `POST {url}/v1/convert/file` (avec `image_export_mode=placeholder`, `to_formats=[md,json]`) ; l'OCR se règle donc via ce JSON (ex. `do_ocr`, `ocr_engine`, `ocr_lang` selon l'API docling-serve) ; il n'existe plus de variables `DOCLING_OCR_*` séparées | `config.py:920-926`, `retrieval/loaders/main.py:247-283` |
| `TIKA_SERVER_URL` | `http://tika:9998` | `config.py:912` |
| `RAG_TEMPLATE` | `DEFAULT_RAG_TEMPLATE` (anglais, citations `[id]`, `{{CONTEXT}}`) | `config.py:1080-1106` |
| `RAG_SYSTEM_CONTEXT` | `False` : contexte injecté dans le message utilisateur ; `True` : dans le message système | `env.py:362`, `utils/middleware.py:610-645` |
| `VECTOR_DB` | `chroma` (image standard), stockage `DATA_DIR/vector_db` | `config.py:483-486` |
| `RAG_FILE_MAX_SIZE` / `RAG_FILE_MAX_COUNT` / `KNOWLEDGE_MAX_*` | non définis | `config.py:979-992` |
| `PDF_EXTRACT_IMAGES` / `PDF_LOADER_MODE` | `False` / `page` | `config.py:1013-1015` |
| `ENABLE_RETRIEVAL_QUERY_GENERATION` | `True` : **appel LLM supplémentaire** avant chaque recherche (réécriture des requêtes) | `config.py:2400`, `utils/middleware.py:1697-1723`, `routers/tasks.py:416-417` |

### Reranker externe

- `ExternalReranker.predict` envoie `POST <RAG_EXTERNAL_RERANKER_URL>` (URL complète, aucun suffixe ajouté ; défaut de la classe `http://localhost:8080/v1/rerank`), en-têtes `Authorization: Bearer <clé>`, corps `{"model": ..., "query": ..., "documents": [...], "top_n": len(documents)}` ; lit `results[].index` et `results[].relevance_score` — `backend/open_webui/retrieval/models/external.py:13-60`.
- C'est le format Jina/Cohere (`/v1/rerank`) servi par llama.cpp et vLLM : compatible, à condition de mettre l'URL complète `http://llm-central:8080/v1/rerank`.
- Le reranker n'est créé que si `ENABLE_RAG_HYBRID_SEARCH=True` et `BYPASS_EMBEDDING_AND_RETRIEVAL=False`, et seulement si `RAG_RERANKING_MODEL` est non vide — `main.py:695-703`, `routers/retrieval.py:174-183`. Sans recherche hybride, aucun reranking.

### Audio, web, tâches de fond, fonctions

| Variable | Défaut | Source |
|---|---|---|
| `AUDIO_STT_ENGINE` | `''` (faster-whisper local) ; `openai`, `azure`, `deepgram`, `mistral` | `config.py:1592` |
| `AUDIO_STT_OPENAI_API_BASE_URL` / `_KEY` | défaut = `OPENAI_API_BASE_URL`/`KEY` réécrits (api.openai.com / `''`) | `config.py:1586-1588` |
| `AUDIO_STT_MODEL` | `''` | `config.py:1594` |
| `AUDIO_TTS_ENGINE` / `AUDIO_TTS_MODEL` | `''` (synthèse du navigateur) / `tts-1` | `config.py:1641,1644` |
| `ENABLE_WEB_SEARCH` / `WEB_SEARCH_ENGINE` / `SEARXNG_QUERY_URL` / `WEB_SEARCH_RESULT_COUNT` | `False` / `''` / `''` / `3` | `config.py:1169,1178,1225,1187` |
| `ENABLE_TITLE_GENERATION` / `ENABLE_TAGS_GENERATION` / `ENABLE_FOLLOW_UP_GENERATION` | `True` / `True` / `True` (appels LLM de fond après chaque réponse dans l'UI) | `config.py:2391-2395` |
| `ENABLE_SEARCH_QUERY_GENERATION` / `ENABLE_AUTOCOMPLETE_GENERATION` | `True` / `False` | `config.py:2398,2429` |
| `TASK_MODEL` / `TASK_MODEL_EXTERNAL` | `''` / `''` (sinon modèle courant) ; `TASK_MODEL_EXTERNAL` sert pour les modèles non Ollama | `config.py:2246-2248`, `utils/task.py:17-37` |
| `ENABLE_CHANNELS` | `False` | `config.py:2084` |
| `ENABLE_NOTES` | `True` | `config.py:2118` |
| `ENABLE_MEMORIES` | `True` | `config.py:408` |
| `ENABLE_AUTOMATIONS` | `True` (permission utilisateur `USER_PERMISSIONS_FEATURES_AUTOMATIONS` `False`) | `config.py:2094,1967` |
| `ENABLE_CALENDAR` | `True` | `config.py:2092` |
| `ENABLE_SUBAGENTS` | `False` | `config.py:2096` |
| `ENABLE_APPS` | `False` | `config.py:2088` |
| `ENABLE_FOLDERS` | `True` | `config.py:2066` |
| `ENABLE_EVALUATION_ARENA_MODELS` | `False` | `config.py:2122` |
| `ENABLE_CODE_INTERPRETER` / `CODE_INTERPRETER_ENGINE` | `True` / `pyodide` | `config.py:406,415` |
| `ENABLE_CODE_EXECUTION` / `CODE_EXECUTION_ENGINE` | `True` / `pyodide` | `config.py:391,393` |
| `ENABLE_IMAGE_GENERATION` | `False` | `config.py:1359` |
| `ENABLE_COMMUNITY_SHARING` / `ENABLE_MESSAGE_RATING` | `True` / `True` | `config.py:2164-2166` |
| `ENABLE_CONTEXT_COMPACTION` / `ENABLE_TOOL_SEARCH` | `False` / `False` | `config.py:2260,2286` |
| `TOOL_SERVER_CONNECTIONS` / `TERMINAL_SERVER_CONNECTIONS` | `[]` (JSON) | `config.py:368-382` |
| `ENABLE_FUNCTIONS` | `True` | `env.py:1185` |

## 3. API utile pour un banc

Authentification : en-tête `Authorization: Bearer <jeton JWT ou clé sk-…>` (`utils/auth.py:421,619`).

| Action | Route et corps | Source |
|---|---|---|
| Inscription | `POST /api/v1/auths/signup` `{"name","email","password","profile_image_url"?}` → `{token, token_type, id, email, name, role, ...}` ; le 1er compte devient `admin` | `routers/auths.py:849-902`, `models/auths.py:192-196`, `routers/auths.py:825-829` |
| Connexion | `POST /api/v1/auths/signin` `{"email","password"}` → même réponse avec `token` | `routers/auths.py:660`, `models/auths.py:173-175` |
| Clé API | `POST /api/v1/auths/api_key` (sans corps) → `{"api_key": "sk-<32 hex>"}` ; `GET`/`DELETE` même route ; exige `ENABLE_API_KEYS=True` (et permission `features.api_keys` pour un non-admin) | `routers/auths.py:1497-1560`, `utils/auth.py:383-385` |
| Téléversement | `POST /api/v1/files/?process=true&process_in_background=true` multipart `file=@...` (+ `metadata` facultatif) ; par défaut **traitement asynchrone** (tâche de fond) ; la réponse contient `id` et `data.status` = `pending` | `routers/files.py:284-305,440,459-481` |
| Statut du traitement | `GET /api/v1/files/{id}/process/status` → `{"status": "pending"\|"processing"\|"completed"\|"failed"}` ; `?stream=true` → flux SSE `data: {"status": ...}` jusqu'à `completed`/`failed` (avec `error`) | `routers/files.py:647-695`, statuts posés en `routers/files.py:146,261,268` |
| Créer une base | `POST /api/v1/knowledge/create` `{"name","description","access_grants"?,"meta"?}` | `routers/knowledge.py:315`, `models/knowledge.py:169-173` |
| Ajouter un fichier | `POST /api/v1/knowledge/{id}/file/add` `{"file_id","directory_id"?}` ; refusé si le fichier n'a pas encore de `data` (« FILE_NOT_PROCESSED ») ; ré-indexe dans la collection `{id}` de façon **synchrone** | `routers/knowledge.py:1473-1553` |
| Ajout en lot | `POST /api/v1/knowledge/{id}/files/batch/add` `[{"file_id": ...}, ...]` | `routers/knowledge.py:2114` |
| Lister | `GET /api/v1/knowledge/` ; détail `GET /api/v1/knowledge/{id}` ; fichiers `GET /api/v1/knowledge/{id}/files` | `routers/knowledge.py:171,1095,1347` |
| Modèles | `GET /api/models` (ou `/api/v1/models`) | `main.py:876-877` |
| Chat | `POST /api/chat/completions` (alias `/api/v1/chat/completions`) | `main.py:1103-1104` |
| Récupération seule | `POST /api/v1/retrieval/query/collection` `{"collection_names":[<knowledge_id>], "query", "k"?, "k_reranker"?, "r"?, "hybrid"?, "hybrid_bm25_weight"?, "enable_enriched_texts"?}` ; `query/doc` existe aussi | `routers/retrieval.py:2891-2960,2836` |
| Lire la config RAG | `GET /api/v1/retrieval/config` (admin) : clés `RAG_TEMPLATE`, `TOP_K`, `ENABLE_RAG_HYBRID_SEARCH`, `TOP_K_RERANKER`, `RELEVANCE_THRESHOLD`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `CONTENT_EXTRACTION_ENGINE`, `DOCLING_*`, `RAG_RERANKING_*`, `RAG_EXTERNAL_RERANKER_*`, `web{...}`… | `routers/retrieval.py:610-700` |
| Écrire la config RAG | **`POST /api/v1/retrieval/config/update`** (pas `POST /config`) ; corps `ConfigForm` : mêmes noms de champs, tous facultatifs, seuls les champs fournis sont écrits ; recharge le reranker | `routers/retrieval.py:860-880,954-1080` |
| Embedding | `GET /api/v1/retrieval/embedding` ; `POST /api/v1/retrieval/embedding/update` `{"RAG_EMBEDDING_ENGINE":"openai","RAG_EMBEDDING_MODEL":"embed","RAG_EMBEDDING_BATCH_SIZE":..,"ENABLE_ASYNC_EMBEDDING":..,"RAG_EMBEDDING_CONCURRENT_REQUESTS":..,"openai_config":{"url":..,"key":..}}` | `routers/retrieval.py:439-610` |

### Chat avec base attachée

- Corps : `{"model": "chat", "messages": [...], "files": [{"type": "collection", "id": "<knowledge_id>"}], "stream": false}`. `files` est recopié dans `metadata.files` — `main.py:1312`.
- Appel API **sans `session_id`** : le RAG « classique » s'applique (`is_file_context_enabled` vrai quand pas de `session_id` ou `function_calling == 'legacy'`) — `utils/tools.py:588-593`, `utils/middleware.py:2932-2938`. Depuis l'interface (avec `session_id`) et en appel de fonctions natif (défaut `native`, `main.py:1349-1353`), les bases sont au contraire proposées au modèle comme **outils** (liste `<attached_knowledge>` en résultat d'outil caché) et non pré-injectées — `utils/middleware.py:2825-2851`, `CHANGELOG.md:163,165`. Pour forcer l'ancien comportement : `params.function_calling = "legacy"` ou capacité de modèle `file_context`.
- Traitement : génération de requêtes par LLM (si activée) → `get_sources_from_items` → contexte `<source id="n" name="...">…</source>` inséré via `RAG_TEMPLATE` dans le dernier message utilisateur — `utils/middleware.py:1685-1803,570-645`.
- Réponse non streamée : objet OpenAI avec en plus une clé de premier niveau **`sources`** (fusion des « events ») — `utils/middleware.py:2950-2951,3522-3535,4280`. Chaque élément : `{"source": <item files>, "document": [textes], "metadata": [{file_id, name, source, ...}], "distances"?: [...]}` — `retrieval/utils.py:1720-1730`.
- Réponse streamée (sans `chat_id`+`message_id`, donc sans émetteur d'événements) : le **premier** bloc SSE est `data: {"sources": [...]}` puis les blocs OpenAI — `utils/middleware.py:6611-6634`, `utils/middleware.py:3128-3143`.
- Paramètres modèle : `params` (ou champs de premier niveau) sont recopiés dans le corps envoyé au fournisseur OpenAI, sauf les paramètres propres à Open WebUI (`stream_response`, `function_calling`, `reasoning_tags`, `system`, …) — `utils/payload.py:105-153`. Donc `"chat_template_kwargs": {"enable_thinking": false}` (en premier niveau ou dans `params`/`params.custom_params`) passe jusqu'à llama.cpp/vLLM ; `reasoning_effort` et `max_tokens` sont mappés — `utils/payload.py:204-217`. `num_ctx` n'est mappé que pour Ollama (`utils/payload.py:240`) : pour une connexion OpenAI il serait transmis tel quel et ignoré ; le contexte de 16 384 jetons se règle côté LLM-Service.
- Le routeur OpenAI n'élague pas les champs inconnus (sauf Azure) — `routers/openai.py:1427-1580`.

## 4. Surface de l'interface

### Pages (`src/routes/(app)/…/+page.svelte`)

- `/` (nouvelle conversation), `/c/[id]`, `/home`, `/folders/[folderId]`, `/s/[id]` (partage), `/auth`, `/auth/sessions/[id]`, `/watch`, `/error`.
- `/workspace` → redirige vers `/workspace/models` (ou la première section permise) — `src/routes/(app)/workspace/+page.svelte:1-22`. Sections : `models` (+ `create`, `edit`), `knowledge` (+ `create`, `[id]`), `prompts` (+ `create`, `[id]`), `tools` (+ `create`, `edit`), `skills` (+ `create`, `edit`). Il existe `workspace/functions/create` mais pas de liste `workspace/functions` : les fonctions se gèrent dans `/admin/functions`.
- `/notes`, `/notes/new`, `/notes/[id]` ; `/channels/[id]`, `/channels/[id]/encrypted` ; `/automations`, `/automations/[id]` ; `/calendar` ; `/playground`, `/playground/completions`, `/playground/images`.
- `/admin` → `/admin/users` → `/admin/users/overview` ; onglets `overview` et `groups` — `src/lib/components/admin/Users.svelte:20`. `/admin/evaluations` → `leaderboard` / `feedback` — `src/lib/components/admin/Evaluations.svelte:17`. `/admin/functions` (+ `create`, `edit`), `/admin/analytics/[tab]`. Le menu latéral de l'admin : Users, Evaluations, Functions, Settings — `src/routes/(app)/admin/+layout.svelte`.
- **Changement notable** : `/admin/settings/[tab]` ne rend plus de page ; il redirige vers `/?settings=admin:<tab>` et ouvre la **fenêtre Réglages unifiée** (réglages personnels et d'administration dans la même fenêtre) — `src/routes/(app)/admin/settings/[tab]/+page.svelte:1-11`.

### Onglets de la fenêtre Réglages (`src/lib/components/chat/SettingsModal.svelte:191-374`)

| Groupe | id | Libellé fr-FR |
|---|---|---|
| Personnel | `general` | Général |
| | `interface` | Interface utilisateur |
| | `notifications` | Notifications |
| | `shortcuts` | Raccourcis |
| | `connections` (si `ENABLE_DIRECT_CONNECTIONS`) | Connexions |
| | `tools` (si intégrations directes) | Intégrations |
| | `personalization` | Personnalisation |
| | `audio` | Audio |
| | `data_controls` | Contrôles des données |
| | `usage` | Consommation de tokens |
| | `archived_chats` | Conversations archivées |
| | `account` | Compte |
| | `about` | À propos |
| Administration | `admin:general` | Général |
| | `admin:authentication` | Authentification |
| | `admin:interface` | Interface utilisateur |
| | `admin:connections` | Connexions |
| | `admin:models` | Modèles |
| | `admin:subagents` | Sous-agents |
| | `admin:integrations` | Intégrations |
| | `admin:apps` | Apps (non traduit) |
| | `admin:documents` | Documents |
| | `admin:audio` | Audio |
| | `admin:images` | Images |
| | `admin:web` | Recherche Web |
| | `admin:code-execution` | Exécution de code |
| | `admin:pipelines` | Pipelines |
| | `admin:analytics` | Analytique |
| | `admin:evaluations` | Évaluations |
| | `admin:db` | Base de données |

Libellés tirés de `src/lib/i18n/locales/fr-FR/translation.json:2821-4006` (clés `settings.admin.*.title`, `settings.personal.*.title`).

### Menu du compte (`src/lib/components/layout/Sidebar/UserMenu.svelte`)

Libellés : Settings (Réglages), Workspace (Espace de travail), Admin Panel (Panneau d'administration), Playground, Notes, Automations (Automatisations), Calendar (Calendrier), Documentation, Releases (Livraisons), Keyboard, Active Users (Utilisateurs connectés), Update your status (Mettre à jour votre statut), Sign Out (Déconnexion).

### Français

- `fr-FR` présent (`src/lib/i18n/locales/languages.json:83`) ; 4 695 clés dont **1 165 vides** (repli sur l'anglais), par exemple « Apps », « Audio » (clé simple), « Authentication », « Notifications » (clé simple), certains libellés Documents (`embeddingQueryPrefix`, `fullTextCharThreshold`, `knowledgeMax*`). Les captures montreront donc un mélange français/anglais.
- Traductions exactes (`translation.json`) : Workspace = « Espace de travail » ; Knowledge = « Connaissances » ; Knowledge Base = « Base de connaissances » ; Admin Panel = « Panneau d'administration » ; Settings = « Réglages » ; New Chat = « Nouvelle conversation » ; Notes = « Notes » ; Channels = « Canaux » ; Models = « Modèles » ; Tools = « Outils » ; Functions = « Fonctions » ; Prompts = « Prompts » ; Skills = « Skills » ; Web Search = « Recherche Web » ; Users = « Utilisateurs » ; Groups = « Groupes » ; Overview = « Aperçu » ; Leaderboard = « Classement » ; Feedback = « Avis » ; Evaluations = « Évaluations » ; API Key = « Clé API » ; Create Knowledge = « Créer une connaissance » ; Upload files = « Téléverser des fichiers » ; Add Content = « Ajouter du contenu » ; Attach Knowledge = « Joindre une connaissance » ; Memory = « Mémoire » ; Memories = « Souvenirs » ; Code Interpreter = « Interpréteur de code » ; Temporary Chat = « conversation temporaire » ; Sign in = « Connexion » ; Sign up = « Inscrivez-vous » ; Create Admin Account = « Créer un compte administrateur » ; Get started = « Démarrer » ; Email = « E-mail » ; Password = « Mot de passe » ; Name = « Nom d'utilisateur » ; Save = « Enregistrer » ; Select a model = « Sélectionnez un modèle » ; Send message = « Envoyer un message » ; Citations = « Citations » ; Valves = « Vannes » ; Filter = « Filtre » ; Pipe = « Pipeline » ; Action = « Action » ; New Function = « Nouvelle fonction » ; New Tool = « Nouvel outil » ; New Note = « Nouvelle note » ; Create Channel = « Créer un canal » ; Default (SentenceTransformers) = « Par défaut (Sentence Transformers) » ; External = « Externe ».
- Libellés de l'onglet Documents (admin) : sections « Extraction de contenu », « Embedding », « Récupération », « Fichiers », « Intégration », « Zone de danger » ; champs « Moteur d'extraction de contenu », « URL du serveur Docling », « Moteur de modèle d'embedding », « Modèle d'embedding », « Taille du lot d'embedding », « Taille des chunks », « Chevauchement des chunks », « Recherche hybride », « Top K », « Top K Reranker », « Seuil de pertinence », « Moteur de ré-ranking », « Modèle de ré-ranking », « Ignorer l'Embedding et le Retrieval », « Mode avec injection complète dans le contexte », « Modèle RAG », « Réindexer » — `translation.json:3044-3217`.
- Onglet Connexions (admin) : « API compatibles OpenAI », « API Ollama », « Gérer les connexions API OpenAI », « Ajouter une connexion », « Direct connexions » — `translation.json:3015-3029`. Compte : « Clé API », « Créer une nouvelle clé secrète », « Jeton JWT » — `translation.json:3680-3695`.

## 5. Fonctions

- **Outils Python** (Workspace > Outils) : routeur `/api/v1/tools` — `main.py:852`. Depuis 0.13.0, interrupteur marche/arrêt par outil et création d'outil depuis le chat — `CHANGELOG.md` (0.13.0 Added).
- **Fonctions** (Admin > Functions) : trois types `Pipe`, `Filter`, `Action` détectés par la classe du module — `backend/open_webui/utils/plugin.py:296-300` ; désactivables par `ENABLE_FUNCTIONS` — `env.py:1185`.
- **Serveurs d'outils** : type `openapi` (défaut) ou `mcp` — `utils/tools.py:176,485-496`, `utils/middleware.py:841` ; client MCP en **Streamable HTTP** (`mcp.client.streamable_http`) — `backend/open_webui/utils/mcp/client.py:12,120-140` ; configuration par `TOOL_SERVER_CONNECTIONS` (JSON) — `config.py:368-374`. MCP Apps affichées dans le chat (0.13.0).
- **Mémoire** : `/api/v1/memories`, `ENABLE_MEMORIES` — `main.py:855`, `config.py:408`.
- **Notes** : `/api/v1/notes` (création, pages, chat lié à une note, épinglage) — `routers/notes.py:111-661`.
- **Canaux** : `/api/v1/channels`, désactivés par défaut (`ENABLE_CHANNELS=False`) ; variante chiffrée — `main.py:841`, `config.py:2084`.
- **RBAC** : rôles `admin`/`user`/`pending`, groupes (`/api/v1/groups`), permissions par défaut `DEFAULT_USER_PERMISSIONS` (workspace, sharing, chat, features) — `config.py:1979-2050`, `main.py:857` ; partage des ressources par `access_grants`.
- **Évaluations** : arène (`ENABLE_EVALUATION_ARENA_MODELS=False`), classement Elo (K=32), avis — `routers/evaluations.py:40-70`, `config.py:2122`.
- **Automatisations** (présentes en 0.13) : tâches planifiées par règle RRULE (`data = {prompt, model_id, rrule}`), routeur `/api/v1/automations` (`list`, `create`, `{id}/update`, `toggle`, `run`, `runs`), exécutées par une boucle `scheduler_worker_loop` démarrée avec l'application ; résultat envoyé dans une conversation ou un canal ; 0.13.3 ajoute les agents de code dans les automatisations — `backend/open_webui/models/automations.py:19-38`, `routers/automations.py:159-409`, `main.py:449-451`, `utils/automations.py:69`, `CHANGELOG.md:12`. Page `/automations`. Permission utilisateur désactivée par défaut.
- **Calendrier** : `/api/v1/calendars`, page `/calendar` — `main.py:866`.
- **Terminal / exécution de code** : interpréteur et exécution de code en `pyodide` (navigateur) par défaut — `config.py:391-415` ; « Open Terminal » externe (`TERMINAL_SERVER_CONNECTIONS`, `/api/v1/terminals`), avec onglets Fichiers, Bureau, Navigateur, Git, et agents de code (Claude Code, Codex, Pi) exposés comme modèles depuis 0.13.1 — `config.py:380-382`, `main.py:864`, `CHANGELOG.md` (0.13.0–0.13.3).
- Autres : sous-agents (`ENABLE_SUBAGENTS`), Skills (Workspace), dossiers avec base et prompt système, compaction de contexte, recherche d'outils, Tether, commentaires, boîte de réception.

## 6. Licence

- `LICENSE` : « Open WebUI License » (© 2023- Open WebUI Inc.) = BSD 3 clauses + **clause 4 de marque** : interdiction de modifier, retirer, masquer ou remplacer la marque « Open WebUI » (nom, logo, identifiants visuels ou textuels), sauf (i) déploiements ou distributions dont le nombre d'utilisateurs finaux (personnes physiques ayant un accès direct) ne dépasse pas **50 sur toute période glissante de 30 jours**, (ii) autorisation écrite préalable, (iii) licence entreprise. Toute autre modification de la marque est une violation substantielle — `LICENSE:20-34`. Contributions sous CLA — `LICENSE:39-40`. Le code rappelle cette contrainte aux endroits de marque (favicon, nom) — `backend/open_webui/config.py:124-127,182-185`.
- `LICENSE_HISTORY` : code antérieur au commit `a76068d6…` sous **MIT** ; code entre `a76068d6…` et `60d84a3a…` sous **BSD 3 clauses** ; après `60d84a3a…`, Open WebUI License — `LICENSE_HISTORY:1-53`, `LICENSE_NOTICE:1-11`.
- Conséquence pour le banc : usage local mono-utilisateur, marque inchangée : aucune contrainte.

## 7. CHANGELOG (3 dernières versions)

- **0.13.3 (2026-11-08)** — `CHANGELOG.md:8-31` : agents de code dans les automatisations (choix du terminal et du dossier) ; changement de terminal ou de dossier en cours de conversation ; corrections : recherche dans les bases contenant de la ponctuation, mode « thinking » DeepSeek avec skills/knowledge/mémoires, copie en HTTP simple, build de l'image Ollama qui échoue désormais si Ollama manque.
- **0.13.2 (2026-11-08)** — `CHANGELOG.md:32-39` : correctifs seulement : conversations en HTTP simple (LAN, adresse Docker) qui ne se chargeaient plus, commentaires et édition Markdown en HTTP, interrupteur « Allow Side Chat ». Important : servir l'UI en `http://127.0.0.1` exige au moins 0.13.2.
- **0.13.1 (2026-11-03)** — `CHANGELOG.md:40-175` : correctifs de sécurité ; migrations de base ; agents de code comme modèles ; Tether ; mode d'autorisation d'outils « Auto » ; texte intégral pour petits fichiers (`RAG_FULL_TEXT_CHAR_THRESHOLD`, 50 000 caractères) ; écrans divisés, Git, éditeur Markdown, tableur. **Ruptures** : « Preload files » désactivé par défaut en appel de fonctions natif (les fichiers joints ne sont plus injectés, le modèle les lit par ses outils ; l'API hors interface garde l'ancien comportement) — `CHANGELOG.md:163` ; `RAG_TOP_K`/`RAG_TOP_K_RERANKER` passent de 3 à 10 et `CHUNK_SIZE` de 1000 à 1024 — `CHANGELOG.md:164` ; contexte (mémoire, skills, bases jointes) transmis en résultats d'outils cachés — `CHANGELOG.md:165` ; « Full Context Mode » renommé « Always Use Full Text » — `CHANGELOG.md:169`.
- Pour mémoire, **0.13.0 (2026-11-02)** — `CHANGELOG.md:176-238` : espace à onglets (fichiers, terminaux, bureau, navigateur), side chats, commentaires et boîte de réception, MCP Apps, sous-agents multi-modèles, limites de fichiers par base ; migrations de base ; contrôles déplacés dans le menu du modèle ; limite d'appels d'outils portée à 1024.

## 8. docker-compose officiel

`docker-compose.yaml:1-32` :

- Service `ollama` : `ollama/ollama:${OLLAMA_DOCKER_TAG-latest}`, volume `ollama:/root/.ollama`, `pull_policy: always`.
- Service `open-webui` : `build` local + `image: ghcr.io/open-webui/open-webui:${WEBUI_DOCKER_TAG-main}`, volume `open-webui:/app/backend/data`, `depends_on: ollama`, port `${OPEN_WEBUI_PORT-3000}:8080` (publié sur toutes les interfaces), `OLLAMA_BASE_URL=http://ollama:11434`, `WEBUI_SECRET_KEY=` (vide), `extra_hosts: host.docker.internal:host-gateway`, `restart: unless-stopped`.
- À retirer ou adapter pour le banc : le service `ollama`, son volume et `depends_on` ; `OLLAMA_BASE_URL` (remplacé par `ENABLE_OLLAMA_API=False`) ; le bloc `build` ; le tag `main` (mettre `v0.13.3` figé par empreinte) ; le port (publier `127.0.0.1:<port>:8080`) ; `WEBUI_SECRET_KEY` vide (fixer une valeur, sinon clé générée hors volume) ; `extra_hosts` inutile si le réseau Docker de LLM-Service est rejoint ; noms préfixés `rag-`.
- Autres fichiers compose du dépôt (non utilisés) : `docker-compose.api.yaml`, `.gpu.yaml`, `.amdgpu.yaml`, `.data.yaml`, `.otel.yaml`, `.playwright.yaml`, `.a1111-test.yaml`.

## Points d'attention pour le banc (synthèse)

1. Renseigner explicitement `RAG_OPENAI_API_BASE_URL`/`KEY` et `AUDIO_STT_OPENAI_API_BASE_URL`/`KEY` (leurs défauts pointent vers api.openai.com).
2. Variables d'environnement lues au premier démarrage seulement ; ensuite la base fait foi (ou `ENABLE_PERSISTENT_CONFIG=False`).
3. `ENABLE_API_KEYS=True` pour les clés `sk-…` ; sinon utiliser le JWT de `signin`.
4. Reranker externe : URL complète `.../v1/rerank`, et seulement avec `ENABLE_RAG_HYBRID_SEARCH=True`.
5. Chaque question avec base déclenche un appel LLM de réécriture de requêtes (`ENABLE_RETRIEVAL_QUERY_GENERATION=True` par défaut) ; titres, tags et suggestions de suite déclenchent d'autres appels dans l'UI.
6. Par l'API sans `session_id`, RAG classique et `sources` en premier niveau (ou premier bloc SSE) ; dans l'UI, les bases passent par les outils natifs.
7. Désactiver la réflexion : `chat_template_kwargs` transmis tel quel au fournisseur.
