# Rapport de mission — Open WebUI

Mission `kit/PROMPT.md`, fiche `kit/fiches/05-open-webui.md`, essais du 13 novembre 2026 sur la machine du profil B (Ryzen 5 9600X, 32 Go dans WSL2, RTX 4060 Ti 16 Go, Docker 29.9.3).

## Ce qui a été installé

| Élément | Version |
|---|---|
| Open WebUI | 0.13.3 (8 novembre 2026, dernière stable) ; image `ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158e6558eeb980bc828e0f1b30238ad24d82ed84d5e5eda1dab2a082f14` (4,59 Go) |
| Conteneur | `rag-open-webui`, projet compose `rag-open-webui`, port `127.0.0.1:3000` seulement ; réseaux `llm-net` et `rag-local` |
| Lecteur de documents (facultatif) | docling-serve 1.38.2, image `quay.io/docling-project/docling-serve-cpu:v1.38.2@sha256:7a480a1604fa3b42efeddc7db9527690d9f9bc903226136013e2bfe6b1a4dfb0` (5,06 Go), conteneur `rag-docling-serve`, sans port publié |
| Serveur MCP d'essai | `rag-mcp-velanor`, lancé depuis l'image Open WebUI (paquet `mcp` 2.3.0 déjà présent), sans port publié |
| Captures | `mcr.microsoft.com/playwright/python:v1.65.1-noble` (éphémère) |
| Modèles (service LLM central, profil `gpu`) | `chat` = Qwen3.5-4B, `embed` = bge-m3, `rerank` = bge-reranker-v2-m3, `transcribe` = faster-whisper-small ; `gemma-4-e4b` à la demande ; contexte 16 384 jetons |
| Versions relevées | `banc-essai/resultats/open-webui/versions-2026-11-13.json` |

Aucun modèle n'a été téléchargé par Open WebUI (embeddings, tri et transcription fournis par le service central).

## Où l'ouvrir

`http://127.0.0.1:3000`, depuis WSL comme depuis le navigateur Windows. Comptes fictifs (administrateur « Claire Admin », utilisateur « Julien Moreau ») : `donnees/IDENTIFIANTS-LOCAUX.txt`. L'instance est laissée en marche, avec Docling et le serveur MCP d'essai.

## Manuels écrits

- Page d'accueil : [documentations/README.md](README.md).
- Partie 1, manuel utilisateur, 18 chapitres : [documentations/manuel/](manuel/), 153 captures annotées propres (02 : 1 reprise du 03 ; 03 : 12 ; 04 : 5 ; 05 : 11 ; 06 : 8 ; 07 : 13 ; 08 : 8 ; 09 : 11 ; 10 : 10 ; 11 : 22 ; 12 : 6 ; 13 : 12 ; 14 : 15 ; 15 : 13 ; 16 : 3 ; 17 : 4 plus 2 reprises des chapitres 05 et 14), et 45 captures de la carte de l'interface.
- Partie 2, annexes A1 à A6 et carte de l'interface : [documentations/annexes/](annexes/).
- Exemples d'API exécutés : [banc-essai/exemples/](../banc-essai/exemples/), sorties dans `sorties_verifiees.txt`.
- Index de la série et comparatif : [documentations/index-serie.md](index-serie.md) ; glossaire : [documentations/glossaire.md](glossaire.md).

## Résultats du banc en cinq lignes

1. Lecture par défaut : 28/34 avec ou sans tri `rerank` ; les 6 échecs viennent du contrat scanné, refusé (« The content provided is empty »).
2. Docling, recherche hybride et `rerank` : 34/34, chaque réponse cite le bon document ; 4 questions pièges sur 4 refusées dans tous les bancs.
3. Temps médian : 58 s par défaut, 24 s avec « Génération de requête de RAG » coupée, 1,3 s avec en plus la réflexion de `chat` coupée (`chat_template_kwargs`), toujours 34/34.
4. Réglage serré (3 passages au lieu de 10) : 32/34, médiane 17 s.
5. Mémoire au plus fort : Open WebUI et Docling 4,0 Go, service central 7,5 Go ; carte graphique 9,4 à 9,9 Go sur 16.

Détail : [annexe A1](annexes/A1-evaluation-qualite-et-performances.md).

## Vérifié, non vérifié

Relectures : lecteur novice (partie 1) en cinq passages, 43, 23, 4, 5 puis **0 remarque** ; relecture adversariale (partie 2), 25 points appliqués.

Vérifié : installation et branchement (`installation-2026-11-13.log`), chaque action de la partie 1 faite à la souris par Playwright, six bancs complets, sauvegarde à froid et restauration sur une instance à part (`essai-restauration-2026-11-13.log`), exemples d'API, ports publiés (`etat-final-2026-11-13.log`).

Non vérifié, et pourquoi :
- recherche web (SearXNG) : facultative dans la fiche, elle ferait sortir les questions du poste ; page de réglage montrée seulement ;
- profil A (sans carte graphique) : machine non disponible ; temps estimés dans l'annexe A2 à partir des débits mesurés de LLM-Service ;
- restauration en place de l'instance principale : faite sur une instance à part pour ne pas risquer l'instance d'essai ;
- mise à jour de version : aucune version plus récente que 0.13.3 au moment des essais ;
- lecture à haute voix : lancée, son non écouté (navigateur automatisé) ; « Mode vocal », conversation temporaire, Playground : non essayés.

## Incidents

- Le premier essai d'outils : `chat` a prévu d'appeler les outils puis a répondu sans les appeler, avec des chiffres inventés ; réussi au second essai (`essai-outils-filtre-2026-11-13.json`). Documenté aux chapitres 11 et 17.
- La mention ajoutée par un filtre (`outlet`) est enregistrée mais pas affichée dans l'interface.
- Par l'API, un assistant ne consulte sa base qu'avec `"params": {"function_calling": "legacy"}` (annexe A3).
- Serveur MCP arrêté : panne silencieuse, une seule ligne « Failed to connect to MCP server ».
- Le conteneur MCP héritait du contrôle de santé de l'image Open WebUI (état « unhealthy ») : corrigé par `--no-healthcheck` dans `service/mcp.sh`.
- Micro refusé par le navigateur hors contexte sûr : captures faites par une adresse `*.localhost` ; sans effet pour l'utilisateur sur `127.0.0.1`.
- Masques des secrets décalés sur certaines captures (défilement) : outil commun `annoter.py` corrigé, captures reprises ; revue des 131 captures d'alors sans aucun secret visible.
- Titres automatiques de conversations parfois en anglais ou vides (« Stock Trends », « your concise title here »).
- Limite de 15 connexions en 3 minutes sur `/api/v1/auths/signin` (réponse 429) rencontrée par les exemples.

## Décisions en attente

1. LLM-Service : modèle de réponse plus léger pour situer un plancher de qualité. Hors mission (modification de LLM-Service). Le levier essayé à la place, la réflexion coupée, a gardé 34/34 en 1,3 s.

## Disque, mémoire, carte graphique

| Élément | Valeur |
|---|---|
| Images | Open WebUI 4,59 Go, docling-serve-cpu 5,06 Go |
| Données d'Open WebUI (`donnees/open-webui/`) | 26 Mo |
| Sauvegarde d'essai (`donnees/sauvegardes/`) | 6,1 Mo |
| Mémoire au repos (fin de mission) | Open WebUI 960 Mio, Docling 775 Mio, serveur MCP 59 Mio |
| Service central, mémoire vive | LiteLLM 717 Mio, llama-swap 9,1 Gio (modèles chargés), speaches 1,4 Gio |
| Carte graphique (service central, bureau compris) | 9 988 Mio sur 16 380 |

Source : `banc-essai/resultats/open-webui/etat-final-2026-11-13.log` et `docker stats` au moment du rapport.

## Tout arrêter ou tout supprimer

```bash
service/arreter.sh            # arrêt d'Open WebUI et de Docling, données conservées
service/mcp.sh stop           # arrêt du serveur MCP d'essai
service/sauvegarder.sh        # sauvegarde à froid avant toute suppression
service/compose.sh --profile docling down && docker rm -f rag-mcp-velanor
rm -rf donnees/open-webui               # irréversible
docker image rm ghcr.io/open-webui/open-webui:v0.13.3 quay.io/docling-project/docling-serve-cpu:v1.38.2
```

LLM-Service n'est jamais arrêté ni modifié par ces scripts.

## Proposition pour la solution suivante

Reprendre de ce banc : le passage systématique d'un banc « sans réflexion » (`--corps '{"chat_template_kwargs": {"enable_thinking": false}}'` dans `banc-essai/open-webui/banc.py`), qui a divisé le temps de réponse par plus de 40 sans perte de qualité ; la recherche des étapes cachées qui sollicitent le modèle (ici la réécriture des requêtes) ; la revue visuelle des captures par un sous-agent avant rédaction ; et, pour les scénarios Playwright, la vérification des horloges (bancs en heure locale, conteneur de captures en temps universel) avant de conclure à un chevauchement.
