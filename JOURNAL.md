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
