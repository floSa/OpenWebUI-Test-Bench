# A3. Automatiser par l'API

> **Objet** : piloter Open WebUI depuis un script ou une autre application, sans l'interface : s'authentifier, lister les modèles, poser une question, créer une base et y verser un document, interroger cette base puis un assistant personnalisé, faire le ménage.
> **Prérequis** : installation du [chapitre 02](../manuel/02-installer-open-webui.md), compte administrateur du [chapitre 03](../manuel/03-premiers-pas.md), assistant « Assistant qualité Vélanor » du [chapitre 07](../manuel/07-assistant-lie-a-une-base.md) ; terminal Ubuntu à la racine du dépôt, `python3` et `curl` (aucune bibliothèque à installer).
> **Version décrite** : Open WebUI 0.13.3 (`ghcr.io/open-webui/open-webui:v0.13.3`), docling-serve 1.38.2, service LLM central (modèles `chat`, `embed`, `rerank`), essais du 13 novembre 2026.
> **Statut des informations** : [Vérifié] exécuté, sortie dans [`exemples/open-webui/sorties_verifiees.txt`](../../../exemples/open-webui/sorties_verifiees.txt) ; [Source] lu dans le code au tag v0.13.3 (`outils/resultats/open-webui/cadrage-source-v0.13.3.md`, section 3) ; [Estimation] calcul expliqué ; [À tester] non essayé.
> **Précautions** : les exemples 03 et 06 écrivent dans l'instance (base « Exemple API » créée puis supprimée) ; les autres sont en lecture seule. Les secrets (identifiants, clé d'API) passent par des variables d'environnement, jamais par les fichiers ; une clé d'API donne les droits du compte qui l'a créée.

## Sommaire

1. [L'API de l'instance](#1-lapi-de-linstance)
2. [S'authentifier](#2-sauthentifier)
3. [Lancer un exemple](#3-lancer-un-exemple)
4. [Exemples](#4-exemples)
5. [Points d'attention](#5-points-dattention)
6. [Outils du banc](#6-outils-du-banc)
7. [Dépannage](#dépannage)
8. [Sources](#sources)

## 1. L'API de l'instance

[Source] Open WebUI expose une API REST sur la même adresse que l'interface (ici `http://127.0.0.1:3000`). La partie « conversation » suit le format d'OpenAI (`POST /api/chat/completions`, `GET /api/models`) : un programme écrit pour OpenAI peut s'y brancher en changeant l'adresse et la clé. Le reste (bases, fichiers, comptes, réglages) est propre à Open WebUI, sous `/api/v1/`. La documentation interactive de l'API (`/docs`) n'est servie qu'en mode développement : `docs_url` n'est défini que si `ENV` vaut `dev` [Source] (`main.py:558`) ; ce que renvoie `/docs` sur l'instance installée n'a pas été relevé dans un résultat brut [À tester]. La liste des routes utiles est dans le relevé de cadrage.

| Action | Route | Exemple |
|---|---|---|
| Se connecter | `POST /api/v1/auths/signin` `{"email", "password"}` → `token` | 01, `owui.py` |
| Lister les modèles et assistants | `GET /api/models` | 01 |
| Poser une question | `POST /api/chat/completions` `{"model", "messages", "stream": false}` | 02, 04, 05 |
| Créer une base | `POST /api/v1/knowledge/create` `{"name", "description"}` | 03 |
| Téléverser un fichier | `POST /api/v1/files/?process=true` (formulaire, champ `file`) | 03 |
| Suivre la lecture du fichier | `GET /api/v1/files/{id}/process/status` → `pending`, `completed` ou `failed` | 03 |
| Ajouter le fichier à la base | `POST /api/v1/knowledge/{id}/file/add` `{"file_id"}` | 03 |
| Lister les bases, leurs fichiers | `GET /api/v1/knowledge/`, `GET /api/v1/knowledge/{id}/files` | 03, 04, 06 |
| Supprimer une base, un fichier | `DELETE /api/v1/knowledge/{id}/delete`, `DELETE /api/v1/files/{id}` | 06 |

## 2. S'authentifier

Chaque requête porte l'en-tête `Authorization: Bearer <secret>`. Deux secrets sont acceptés [Source] :

- **jeton de session** : renvoyé par `POST /api/v1/auths/signin` avec l'adresse et le mot de passe d'un compte ; c'est la voie suivie par les exemples [Vérifié] (exemple 01, « authentification : connexion (jeton de session) ») ;
- **clé d'API** (`sk-…`) : créée dans l'interface (chapitre [15](../manuel/15-administrer.md#créer-une-clé-dapi)) ou par `POST /api/v1/auths/api_key`, une seule par compte ; l'administrateur doit d'abord autoriser les clés (« Clés API »).

Les exemples lisent `OWUI_CLE` si elle est définie, sinon `OWUI_EMAIL` et `OWUI_MOT_DE_PASSE`. Aucune clé n'a été créée pour ces essais : le compte administrateur en possède déjà une (chapitre 15) et en créer une autre la remplacerait. La voie par clé a été essayée avec cette clé existante, passée par `OWUI_CLE` sans être affichée [Vérifié] (exemple 01, seconde sortie).

## 3. Lancer un exemple

```bash
exemples/open-webui/lancer.sh exemples/open-webui/02_question_simple.py
```

[Vérifié] `lancer.sh` lit les identifiants fictifs du compte administrateur dans `donnees/IDENTIFIANTS-LOCAUX.txt` (lignes `open-webui.admin.email` et `open-webui.admin.mot_de_passe`), les passe aux exemples par `OWUI_EMAIL` et `OWUI_MOT_DE_PASSE`, affiche l'heure, masque dans la sortie tout ce qui ressemble à une clé (`sk-…`) ou à un jeton (`eyJ…`) et termine par le code de sortie. Pour une autre instance ou un autre compte, définir soi-même ces variables (ou `OWUI_CLE`, et `OWUI_URL` pour l'adresse) et lancer `python3 exemples/open-webui/<exemple>.py` depuis la racine.

Les exemples Python n'utilisent que la bibliothèque standard ; les fonctions communes (requête, connexion, téléversement en formulaire, attente du traitement, lecture des sources) tiennent dans `exemples/open-webui/owui.py`. L'ordre compte pour 03, 04 et 06 : 04 interroge la base créée par 03, 06 la supprime.

## 4. Exemples

Toutes les questions sont posées avec `"chat_template_kwargs": {"enable_thinking": false}` : ce champ, inconnu d'Open WebUI, est transmis tel quel au service de modèles [Source] et coupe la phase de réflexion de `chat`. Les réponses arrivent alors en 1 à 2 secondes [Vérifié] ; avec la réflexion, compter jusqu'à deux minutes : 95 % des questions sous 71,1 à 119,5 s selon les bancs avec réflexion [Vérifié] (annexe [A1](A1-evaluation-qualite-et-performances.md), `latence_p95_s` des bancs `defaut-sans-rerank` à `serre`).

### 01. Lister les modèles (curl)

**But** : vérifier que l'instance répond, se connecter et lister les modèles et assistants proposés.

```bash
exemples/open-webui/lancer.sh exemples/open-webui/01_lister_modeles.sh
```

```text
santé : HTTP 200
authentification : connexion (jeton de session)
- chat : « chat »
- gemma-4-e4b : « gemma-4-e4b »
- assistant-qualit-vlanor : « Assistant qualité Vélanor », assistant fondé sur chat
code 0
```

[Vérifié] ([sortie](../../../exemples/open-webui/sorties_verifiees.txt)). Les assistants personnalisés apparaissent comme des modèles ; `info.base_model_id` donne le modèle sur lequel ils reposent. Le jeton est extrait avec `python3`, `jq` n'étant pas installé.

### 02. Question simple au modèle `chat`

**But** : poser une question sans document et lire la réponse et le nombre de jetons.

```bash
exemples/open-webui/lancer.sh exemples/open-webui/02_question_simple.py
```

```text
durée : 1.0 s
modèle : chat
réponse : Une base de connaissances sert d'élément central qui enrichit les réponses de l'assistant en lui fournissant des informations précises, factuelles et contextuelles sur la thématique traitée.
jetons : 27 en entrée, 42 en sortie
code 0
```

[Vérifié] ([sortie](../../../exemples/open-webui/sorties_verifiees.txt)). Corps envoyé : `{"model": "chat", "stream": false, "messages": [{"role": "user", "content": "…"}], "chat_template_kwargs": {"enable_thinking": false}}`. La réponse a la forme d'OpenAI (`choices[0].message.content`, `usage`).

### 03. Créer une base et y verser un document

**But** : créer la base « Exemple API », téléverser `corpus/documents/rapport-annuel-2025.pdf`, attendre la fin de sa lecture, puis l'ajouter à la base.

```bash
exemples/open-webui/lancer.sh exemples/open-webui/03_creer_une_base.py
```

```text
base créée : Exemple API | id 2528d0f0-64b7-493e-85eb-748462e0950a
fichier téléversé : rapport-annuel-2025.pdf | id d7e46a9f-8d61-4706-b264-c32db628e521 | statut initial pending
traitement : completed en 10.6 s
fichiers de la base : ['rapport-annuel-2025.pdf']
code 0
```

[Vérifié] ([sortie](../../../exemples/open-webui/sorties_verifiees.txt)). Le téléversement rend la main tout de suite (statut `pending`) : la lecture (ici par Docling, réglage du [chapitre 08](../manuel/08-regler-la-lecture-des-documents.md)) et le calcul des vecteurs par `embed` se font en tâche de fond. L'ajout à la base est refusé tant que le fichier n'est pas lu [Source] : il faut attendre `completed`. L'exemple s'arrête si une base « Exemple API » existe déjà.

### 04. Interroger la base

**But** : poser une question à la base créée en 03 et afficher la réponse et les passages utilisés (document, page).

```bash
exemples/open-webui/lancer.sh exemples/open-webui/04_interroger_la_base.py
```

```text
question : Quel a été le chiffre d'affaires du troisième trimestre 2025 ?  (1.3 s)
réponse : Le chiffre d'affaires du troisième trimestre (T3) 2025 s'élève à **14,2 M€** [1].
sources :
  - rapport-annuel-2025.pdf, page 4 : ## 3. Chiffre d'affaires trimestriel | Trimestre | Chiffre d'affaires (M€) | Par
  - rapport-annuel-2025.pdf, page 3 : ## 2. Chiffres clés 2025 | Indicateur | 2025 | Évolution | |--------------------
  …
code 0
```

[Vérifié] ([sortie](../../../exemples/open-webui/sorties_verifiees.txt) : 10 passages, pages 4, 3, 6, 1, 2, 10, 8, 5, 7, 9). La base est désignée par `"files": [{"type": "collection", "id": "<id de la base>"}]`. La réponse non streamée contient, en plus du format d'OpenAI, un champ `sources` : pour chaque base, la liste des passages (`document`) et de leurs métadonnées (`metadata` : `name`, `page_label`…). Le renvoi `[1]` de la réponse désigne le premier passage. Le nombre de passages (10) et leur ordre suivent les réglages de recherche de l'instance (chapitre 08 : 10 passages, recherche hybride et reranker `rerank`).

### 05. Interroger l'assistant personnalisé

**But** : poser une question à l'assistant existant « Assistant qualité Vélanor » (id `assistant-qualit-vlanor`, base « Démo Vélanor »), en lecture seule. L'exemple fait deux appels, sans puis avec `"params": {"function_calling": "legacy"}`.

```bash
exemples/open-webui/lancer.sh exemples/open-webui/05_interroger_l_assistant.py
```

```text
--- params = {}  (2.0 s)
réponse : Il est impossible de répondre à cette question car le document ne mentionne ni la firme Batterix ni des résultats d'audit spécifiques liés à elle. […] (par exemple autour de 40% selon le rapport d'audit interne du 25 août 2017) […]
sources : aucune
--- params = {'function_calling': 'legacy'}  (1.7 s)
réponse : Le taux de défaut des cellules mesuré chez Batterix lors de l'audit effectué le 18 juin 2025 était de 0,3 %. […]
sources :
  - supplier-audit-batterix-en.pdf, page 1 : Vélanor SAS — document fictif — page 1 Supplier Quality Audit — Batterix GmbH, B
  - contrat-batterix-scan.pdf, page 1 : ## CONTRAT D'APPROVISIONNEMENT N° BX-2025-117 Entre : Vélanor SAS, 12 quai de la
  …
code 0
```

[Vérifié] ([sortie](../../../exemples/open-webui/sorties_verifiees.txt)). Sans `function_calling: "legacy"`, la base de l'assistant n'est pas consultée et le modèle invente une réponse (taux de 40 %, audit de 2017, absents du corpus) ; avec, les passages de « Démo Vélanor » sont fournis et la réponse est juste (0,3 %, audit du 18 juin 2025). Voir le [point d'attention 1](#5-points-dattention).

### 06. Ménage

**But** : supprimer la base « Exemple API » et les fichiers qu'elle contient, puis lister les bases restantes.

```bash
exemples/open-webui/lancer.sh exemples/open-webui/06_menage.py
```

```text
suppression de la base : Exemple API -> True
suppression du fichier : rapport-annuel-2025.pdf -> {'message': 'File deleted successfully'}
bases restantes : ['Banc-docling', 'Démo Vélanor', 'Banc']
code 0
```

[Vérifié] ([sortie](../../../exemples/open-webui/sorties_verifiees.txt)). La liste des fichiers de la base est lue **avant** de la supprimer, pour pouvoir ensuite supprimer chaque fichier. La base et le fichier supprimés ne sont plus trouvés ensuite (réponse 404). Les bases existantes (« Démo Vélanor », « Banc », « Banc-docling ») ne sont pas touchées : seules les bases nommées exactement « Exemple API » sont supprimées.

## 5. Points d'attention

1. **Bases d'un assistant et appel de fonctions.** [Source] [Vérifié] Depuis la version 0.13, l'appel de fonctions « natif » est le défaut : dans l'interface, les bases attachées sont proposées au modèle comme **outils** qu'il décide d'appeler, au lieu d'être cherchées et insérées d'office. Par l'API, sans conversation de l'interface (`session_id` absent), ces outils ne sont pas fournis. Conséquences constatées :
   - une base passée dans `files` (exemple 04) est cherchée et insérée d'office (recherche « classique ») : la réponse et le champ `sources` sont corrects ;
   - la base **attachée à un assistant** (exemple 05) n'est consultée que si la requête contient `"params": {"function_calling": "legacy"}` ; sinon l'assistant répond sans document, et peut inventer. Autre solution : passer la base de l'assistant dans `files`, comme en 04.
2. **Réflexion du modèle.** `chat_template_kwargs.enable_thinking: false` divise le temps de réponse (1 à 2 s ici) [Vérifié] ; le champ est transmis au service de modèles sans contrôle [Source]. Avec un autre modèle que `chat`, ce champ peut être sans effet ou refusé. [À tester]
3. **Limite de connexions.** [Vérifié] [Source] Au-delà de 15 connexions en 3 minutes pour une même adresse, `POST /api/v1/auths/signin` répond `429 {"detail":"API rate limit exceeded"}` (`routers/auths.py:99` ; constaté pendant ces essais, [sortie](../../../exemples/open-webui/sorties_verifiees.txt), « constats hors exemples »). Un script qui enchaîne les appels doit se connecter une fois et réutiliser le jeton (ce que fait `owui.py`), ou utiliser une clé d'API.
4. **Lecture en tâche de fond.** [Vérifié] Un fichier téléversé n'est pas utilisable tout de suite : attendre `completed` sur `/process/status` avant de l'ajouter à une base (exemple 03). Un fichier en échec (`failed`) porte la raison dans `error`.
5. **Conversations.** [Vérifié] Un appel à `/api/chat/completions` sans `chat_id` ne crée aucune conversation dans l'interface : nombre de conversations du compte identique avant et après les exemples (11 et 11, [sortie](../../../exemples/open-webui/sorties_verifiees.txt), « constats hors exemples »).
6. **Réglages globaux.** [Source] Le nombre de passages, la recherche hybride et le reranker se règlent pour toute l'instance (chapitre 08, ou `POST /api/v1/retrieval/config/update` en administrateur) ; ils ne se passent pas question par question dans `/api/chat/completions`.
7. **Flux.** [Source] Avec `"stream": true`, la réponse arrive en blocs `data: …` ; le premier bloc contient `sources`, les suivants le texte. Non utilisé dans les exemples. [À tester]

[Estimation] Pour 1 000 questions par jour à 1,5 s chacune sans réflexion (exemples 04 et 05), le modèle est occupé environ 25 minutes (1 000 × 1,5 s = 1 500 s) ; le service central traite plusieurs questions en même temps : 4 requêtes simultanées à 46 jetons/s chacune, 174 jetons/s cumulés, contre 68 jetons/s pour une requête seule [Source] (`~/mes_projets/Projet-IA/LLM-Service/README.md`, tableau des temps de réponse) ; plusieurs scripts en parallèle ralentissent donc chaque réponse sans la bloquer.

## 6. Outils du banc

`outils/open-webui/client.py` [Vérifié] est le client du banc (mêmes routes, connexion par les identifiants fictifs) ; `outils/open-webui/banc.py` crée la base « Banc », y verse le corpus, pose les 38 questions par `/api/chat/completions` et en tire les mesures de l'annexe A1. Ils lisent les identifiants directement dans `donnees/` et ne sont pas destinés à être recopiés : les exemples de cette annexe en sont la version lisible.

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `KeyError: 'OWUI_EMAIL'` | exemple lancé sans `lancer.sh` ni variables | passer par `exemples/open-webui/lancer.sh`, ou définir `OWUI_CLE` (ou `OWUI_EMAIL` et `OWUI_MOT_DE_PASSE`) |
| `HTTP 429 … API rate limit exceeded` | plus de 15 connexions en 3 minutes | attendre 3 minutes ; réutiliser le jeton ou passer à une clé d'API |
| `HTTP 401` | jeton expiré ou clé supprimée | se reconnecter ; recréer la clé (chapitre 15) |
| `HTTP 403` avec une clé d'API | clés non autorisées par l'administrateur, ou permission absente pour un compte non administrateur | « Clés API » activé (chapitre 15), permission du groupe (chapitre 14) |
| `la base « Exemple API » existe déjà` | exemple 03 relancé sans ménage | lancer l'exemple 06, puis 03 |
| `StopIteration` à l'exemple 04 | base « Exemple API » absente | lancer l'exemple 03 avant |
| assistant qui répond sans source | base de l'assistant non consultée par l'API | ajouter `"params": {"function_calling": "legacy"}` (exemple 05) |
| ajout à la base refusé (fichier non traité) | lecture du fichier pas finie | attendre `completed` sur `/api/v1/files/{id}/process/status` |

## Sources

- Exemples : `exemples/open-webui/*.py`, `*.sh`, sorties dans `exemples/open-webui/sorties_verifiees.txt`.
- Client et banc : `outils/open-webui/client.py`, `outils/open-webui/banc.py`.
- Relevé du code source v0.13.3 : `outils/resultats/open-webui/cadrage-source-v0.13.3.md` (section 3, « API utile pour un banc ») ; `backend/open_webui/utils/middleware.py` (bases d'un modèle en mode `legacy`, lignes 2282-2320), `backend/open_webui/utils/tools.py:588-593`, `backend/open_webui/routers/auths.py:99` (limite de connexions).
- Code source d'Open WebUI : https://github.com/open-webui/open-webui/tree/v0.13.3 ; documentation de l'API : https://docs.openwebui.com/getting-started/api-endpoints
