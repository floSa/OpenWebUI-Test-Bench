# Manuel d'Open WebUI

Ce manuel apprend à installer et à utiliser Open WebUI 0.13.3 sur un poste Windows 11 avec WSL2, branché sur un service de modèles d'IA local, avec un usage central : interroger ses propres documents. Il s'adresse à une personne à l'aise avec un terminal, sans être forcément développeur. Chaque étape a été faite dans l'interface, à la souris, et montrée par une capture d'écran annotée.

Le manuel se lit en deux parties : la **partie 1** est le manuel utilisateur, à lire dans l'ordre ; la **partie 2** évalue l'outil (qualité des réponses, matériel, automatisation, exploitation) et n'est pas nécessaire pour suivre la partie 1.

## Par où commencer

Lire les chapitres 01 à 04 dans l'ordre : en une heure environ, l'application est installée, configurée, et une première réponse citant un document est obtenue.

## Partie 1 — Manuel utilisateur

| N° | Chapitre | Ce qu'on saura faire |
|---|---|---|
| 01 | [Découvrir Open WebUI](manuel/01-decouvrir-open-webui.md) | dire à quoi sert l'outil, pour qui, sur quelle machine, et ce qu'il vaut d'après les essais |
| 02 | [Installer Open WebUI](manuel/02-installer-open-webui.md) | installer, ouvrir, arrêter, redémarrer et supprimer l'application |
| 03 | [Premiers pas](manuel/03-premiers-pas.md) | créer le compte administrateur, se repérer dans l'écran, régler la langue, vérifier la connexion aux modèles et ne garder que les modèles de conversation |
| 04 | [Première question en dix minutes](manuel/04-premiere-question.md) | joindre un document à une conversation, poser une question et lire la source citée |
| 05 | [Créer et alimenter une base de connaissances](manuel/05-bases-de-connaissances.md) | créer une base, y déposer des fichiers, les consulter, les retirer |
| 06 | [Interroger ses documents et lire les sources](manuel/06-interroger-ses-documents.md) | appeler une base avec « # », lire les citations et le raisonnement, poursuivre, régénérer, noter une réponse |
| 07 | [Créer un assistant lié à une base](manuel/07-assistant-lie-a-une-base.md) | créer un modèle personnalisé avec sa consigne et sa base, le partager |
| 08 | [Régler la lecture des documents](manuel/08-regler-la-lecture-des-documents.md) | choisir le lecteur de documents (Docling pour les scans), le découpage, la recherche hybride, le tri par le reranker, le texte intégral |
| 09 | [Converser au quotidien](manuel/09-converser-au-quotidien.md) | gérer les conversations (dossiers, recherche, épingle, archive, partage, export), comparer plusieurs modèles |
| 10 | [Notes et mémoire](manuel/10-notes-et-memoire.md) | écrire des notes, les enrichir avec le modèle, faire retenir des informations durables |
| 11 | [Prompts, outils, fonctions et serveurs MCP](manuel/11-prompts-outils-fonctions.md) | enregistrer des prompts réutilisables, ajouter un outil, un filtre et un serveur MCP |
| 12 | [Voix et recherche web](manuel/12-voix-et-recherche-web.md) | dicter une question, faire lire une réponse, brancher une recherche web locale |
| 13 | [Automatisations, canaux et calendrier](manuel/13-automatisations-canaux-calendrier.md) | programmer une question récurrente, ouvrir un canal d'équipe, consulter le calendrier |
| 14 | [Comptes, groupes et permissions](manuel/14-comptes-groupes-permissions.md) | créer des comptes, des groupes, régler les droits et le partage des bases |
| 15 | [Administrer l'instance](manuel/15-administrer.md) | régler l'instance (fonctions, inscriptions, interface), créer une clé d'API, suivre l'usage et les évaluations, sauvegarder la base |
| 16 | [Cas pratiques](manuel/16-cas-pratiques.md) | mettre en place trois usages complets, de bout en bout |
| 17 | [En cas de problème](manuel/17-en-cas-de-probleme.md) | reconnaître les erreurs réellement rencontrées et les corriger |
| 18 | [Glossaire](manuel/18-glossaire.md) | retrouver le sens des mots employés |

## Partie 2 — Évaluation et compléments

| N° | Annexe | Contenu |
|---|---|---|
| A1 | [Évaluation : qualité et performances](annexes/A1-evaluation-qualite-et-performances.md) | résultats du banc de 38 questions, sans puis avec le reranker, effet du lecteur Docling et du nombre de passages |
| A2 | [Choisir son matériel et ses modèles](annexes/A2-choisir-son-materiel-et-ses-modeles.md) | configurations minimales sans et avec carte graphique, budget de contexte, temps d'attente |
| A3 | [Automatiser par l'API](annexes/A3-automatiser-par-l-api.md) | API de l'instance, clés, exemples exécutés |
| A4 | [Exploitation](annexes/A4-exploitation.md) | sauvegarde, restauration, mise à jour, journaux, sécurité, licence et marque, connexions sortantes |
| A5 | [Fonctionnement interne](annexes/A5-fonctionnement-interne.md) | architecture, conteneurs, ports, découpage, budget de contexte |
| A6 | [Rapport d'essais](annexes/A6-rapport-d-essais.md) | méthode, preuves, ce qui a été vérifié et ce qui ne l'a pas été |
| — | [Carte de l'interface](annexes/carte-interface.md) | chaque page et menu de l'interface, avec le chapitre qui le couvre |

## Parcours conseillés

| Besoin | Chapitres |
|---|---|
| Interroger ses documents, seul | 01 à 08, puis 16 |
| Mettre l'outil à disposition d'une équipe | 01 à 07, 14, 15, puis annexe A4 |
| Automatiser (scripts, autre application) | 01 à 04, 15, puis annexe A3 |
| Choisir l'outil ou le matériel | 01, puis annexes A1 et A2 |

## Ce qui reste ouvert

- Recherche web (SearXNG) non installée : la page de réglage est montrée au chapitre 12, la fonction n'a pas été essayée.
- Configuration sans carte graphique non mesurée : ses temps d'attente sont estimés (chapitre 01, annexe A2).
- Fonctions vues sans être essayées : « Mode vocal », conversation temporaire, Playground, Skills, sous-agents, génération d'images (voir la carte de l'interface, annexe).
- Dans cette version, la mention ajoutée par un filtre en fin de réponse n'est pas affichée (chapitre 11) et un modèle peut oublier d'appeler un outil (chapitres 11 et 17).

## Conventions des captures

Chaque capture porte des rectangles rouges numérotés (pastilles), repris dans le tableau N° | Élément | Rôle qui la suit. Un rectangle noir bordé de rouge, **sans numéro**, n'est pas une annotation : il masque une clé ou un mot de passe.

## Décisions en attente

Réservé aux responsables de l'installation : les choix qui dépassent ce manuel (réglages du service de modèles) sont listés dans le [journal du projet](../../JOURNAL.md#décisions-en-attente).
