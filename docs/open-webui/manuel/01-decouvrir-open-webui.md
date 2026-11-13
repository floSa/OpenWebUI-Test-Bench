# 01. Découvrir Open WebUI

> Ce chapitre dit à quoi sert Open WebUI, pour qui il est fait, ce qu'il demande comme machine, et ce qu'il vaut d'après les essais. Il ne demande aucune manipulation.
> **Point de départ** : aucun ; ce chapitre se lit avant toute installation.
> **Durée** : environ 10 minutes. **Avant** : rien.

## Ce qu'il faut savoir

Open WebUI 0.13.3 a été essayé le 13 novembre 2026 sur Windows 11 (WSL2), avec des modèles d'IA installés sur la même machine. L'interface s'affiche en français.

## Ce que c'est

Open WebUI est une application web de **conversation avec des modèles d'IA**, qui s'installe sur un poste ou un serveur. Elle ressemble aux assistants conversationnels en ligne, mais tout reste sur la machine : les modèles, les documents et les conversations.

Ce manuel suit son usage principal pour une entreprise : **interroger ses propres documents**. Les documents sont rangés dans des **bases de connaissances** ; une question posée sur une base reçoit une réponse rédigée à partir des documents, avec le nom du document d'où vient chaque information (une **citation**).

Autour de cet usage, Open WebUI offre beaucoup d'autres fonctions : comptes et groupes avec des droits, assistants préréglés, notes, mémoire, prompts enregistrés, outils et extensions, dictée vocale, canaux de discussion, questions programmées.

Quelques mots reviennent dans tout le manuel :

| Mot | Sens |
|---|---|
| modèle | programme d'IA qui rédige les réponses ; ici, le modèle `chat` |
| base de connaissances | ensemble de documents rangés sous un nom |
| citation, source | document d'où vient une information de la réponse |
| assistant | modèle préréglé avec une consigne et une base (chapitre 07) |
| service de modèles | programme séparé qui fait tourner les modèles d'IA ; Open WebUI s'y connecte |

Les autres termes sont définis dans le [glossaire](18-glossaire.md).

## Pour qui

| Adapté | Peu adapté |
|---|---|
| Une équipe qui veut une interface commune, avec des comptes, des groupes et des droits séparés | Une personne qui veut seulement poser trois questions sur un document : l'outil est riche, donc long à régler |
| Des documents confidentiels qui ne doivent pas partir vers un service en ligne | Un poste sans carte graphique, si les réponses doivent arriver en quelques secondes avec les réglages par défaut |
| Des documents variés : PDF, Word, Excel, PowerPoint, pages web, notes, enregistrements audio, scans (avec le lecteur Docling) | Une marque blanche (logo et nom de l'entreprise à la place d'Open WebUI) au-delà de 50 utilisateurs : réservée à l'offre Enterprise payante |
| Des usages au-delà des documents : assistants par service, notes, outils, voix | Une recherche fine dans des milliers de documents sans réglage : il faut régler la lecture et la recherche (chapitre 08) |

## Le projet

| | |
|---|---|
| Dépôt | https://github.com/open-webui/open-webui |
| Site | https://openwebui.com |
| Licence | Open WebUI License : licence BSD à 3 clauses, plus une clause qui interdit de retirer la marque « Open WebUI » (sauf moins de 50 utilisateurs, ou offre Enterprise) |
| Popularité | 158 532 étoiles et 23 049 forks sur GitHub |
| Activité | très active : 2 565 modifications sur les 90 derniers jours, 893 contributeurs, plusieurs versions par mois (0.13.0 à 0.13.3 entre le 3 et le 8 novembre 2026) |
| Ancienneté | projet créé en octobre 2023 |
| Coût | gratuit ; une offre Enterprise payante existe |

Chiffres relevés sur GitHub le 13 novembre 2026.

## Fonctions

Réponses : **Oui**, **Non**, ou **Partiel** avec la limite en une phrase. Chaque « Oui » a été essayé pour ce manuel.

| Fonction | Réponse | Chapitre |
|---|---|---|
| Interface en français | Oui | 03 |
| Modèles installés sur la machine (service compatible OpenAI) | Oui | 02, 03 |
| Bases de connaissances, réponses avec citations | Oui | 05, 06 |
| PDF scannés | Partiel : seulement avec le lecteur Docling, à installer en plus | 08 |
| Fichiers audio dans une base (transcription) | Oui, avec des erreurs de transcription sur les chiffres et les noms rares | 05, 16 |
| Recherche hybride et tri des passages | Oui | 08 |
| Assistants préréglés liés à une base | Oui | 07 |
| Comptes, groupes, droits par fonction | Oui | 14 |
| Notes et mémoire | Oui ; mémoire marquée expérimentale | 10 |
| Outils, filtres, serveurs MCP | Partiel : le modèle n'appelle pas toujours l'outil ; l'ajout d'un filtre en fin de réponse ne s'affiche pas | 11 |
| Dictée vocale | Oui, sur une adresse sûre (`127.0.0.1`) | 12 |
| Recherche sur le web | Non essayée : demande un moteur de recherche à installer, et fait sortir les questions du poste | 12 |
| Questions programmées (automatisations) | Oui | 13 |
| Canaux de discussion entre comptes | Oui | 13 |
| API pour automatiser | Oui | annexe A3 |

## Matériel nécessaire

Open WebUI ne fait tourner aucun modèle : il les demande à un **service de modèles** installé à part (LLM-Service). Le matériel se calcule donc pour l'ensemble.

**Configuration minimale sans carte graphique** (service de modèles en mode processeur) :

- un processeur récent de 8 cœurs ;
- 16 Go de mémoire vive : environ 4,3 Go pour le service de modèles, 1 à 1,6 Go pour Open WebUI, et jusqu'à 2,4 Go de plus pour Docling pendant la lecture d'un document ;
- 10 Go de disque pour les deux programmes (Open WebUI 4,6 Go, Docling 5,1 Go), plus la place des modèles du service et des documents ;
- temps d'attente estimé, d'après la vitesse du modèle sur processeur (environ cinq fois plus lente) : quelques secondes par question avec la réflexion du modèle coupée (chapitre 07, étape 12), deux minutes environ avec la réflexion, près de cinq minutes avec tous les réglages par défaut. Cette configuration n'a pas été mesurée avec Open WebUI : ce sont des estimations.

**Configuration minimale avec carte graphique NVIDIA** (configuration essayée) :

- une carte graphique de 12 Go de mémoire (16 Go sur la machine d'essai) : 7 Go pour les trois modèles permanents, plus l'affichage de Windows ;
- 16 Go de mémoire vive dans WSL au minimum, 32 Go confortables : 7,5 Go pour le service de modèles et 2,3 à 4 Go pour Open WebUI et Docling, mesurés au plus fort ;
- le même disque que ci-dessus ;
- temps d'attente mesuré : environ une minute par question avec les réglages par défaut, 24 secondes avec la réécriture des questions coupée (chapitre 08, étape 9), 1,3 seconde en médiane avec en plus la réflexion coupée ; lecture des 9 documents d'essai par Docling en 51 secondes.

Le détail, les calculs et les mesures sont dans l'[annexe A2](../annexes/A2-choisir-son-materiel-et-ses-modeles.md).

## Résultats mesurés

Sur un jeu d'essai de 9 documents d'une entreprise fictive et 38 questions dont les réponses sont connues :

- avec la lecture par défaut, 28 bonnes réponses sur 34 : les 6 échecs viennent d'un contrat scanné, que la lecture par défaut refuse ;
- avec le lecteur Docling, la recherche hybride et le tri par `rerank` : **34 bonnes réponses sur 34**, chaque réponse citant le bon document ;
- les 4 questions sans réponse dans les documents ont été refusées par l'outil dans tous les essais, au lieu d'une réponse inventée ;
- temps de réponse médian : 58 secondes avec les réglages par défaut, 24 secondes avec la réécriture des questions coupée, 1,3 seconde avec en plus la réflexion du modèle coupée, sans perte de qualité ;
- un réglage plus serré (3 passages au lieu de 10) fait perdre 2 réponses sur 34.

Le détail est dans l'[annexe A1](../annexes/A1-evaluation-qualite-et-performances.md).

## Pour aller plus loin

- Installer : [chapitre 02](02-installer-open-webui.md).
- Le parcours le plus court jusqu'à une première réponse citée : chapitres 02 à 04, en une heure environ.
- Le sommaire complet : [page d'accueil du manuel](../README.md).

---
*Version décrite : Open WebUI 0.13.3, essais du 13 novembre 2026. Détails et preuves : [rapport d'essais](../annexes/A6-rapport-d-essais.md).*
