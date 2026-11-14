# Carte de l'interface d'Open WebUI 0.13.3

> **Objet** : liste de contrôle de la couverture de l'interface : chaque page, menu, onglet et réglage visible, avec le chapitre du manuel qui le couvre.
> **Prérequis** : instance installée (chapitre 02), compte administrateur, interface en français.
> **Version décrite** : Open WebUI 0.13.3, parcours du 13 novembre 2026.
> **Statut des informations** : [Vérifié] relevé par le scénario `banc-essai/open-webui/captures/carte.py` (texte et éléments de chaque page dans `banc-essai/resultats/open-webui/captures/carte/`) ; [Source] non vu à l'écran, tiré du code ; [Estimation] sans objet ; [À tester] sans objet.
> **Précautions** : aucune ; parcours en lecture seule.

## Sommaire

1. [Pages principales](#1-pages-principales)
2. [Fenêtre Réglages, groupe Personnel](#2-fenêtre-réglages-groupe-personnel)
3. [Fenêtre Réglages, groupe Administrateur](#3-fenêtre-réglages-groupe-administrateur)
4. [Panneau d'administration](#4-panneau-dadministration)
5. [Menus](#5-menus)
6. [Captures de repérage](#6-captures-de-repérage)

Toutes les lignes sont [Vérifié] sauf mention contraire.

## 1. Pages principales

| Page ou menu | Chemin d'accès | Éléments (boutons, onglets, réglages) | Manuel qui le couvre |
|---|---|---|---|
| Accueil, nouvelle conversation | barre latérale › « Nouvelle conversation » (`/`) | barre latérale (Nouvelle conversation, Recherche, Notes, Espace de travail, Dossiers, Conversations, menu du compte), onglets de conversation (« + », Split screen, conversation temporaire), sélecteur de modèle, « Model controls », zone de saisie, « + » (Téléverser des fichiers, Prise de vue, Add Context, Interpréteur de code), Saisie vocale, Mode vocal, « Suggéré » | [03](../manuel/03-premiers-pas.md), [04](../manuel/04-premiere-question.md), [09](../manuel/09-converser-au-quotidien.md), [12](../manuel/12-voix-et-recherche-web.md) |
| Conversation | liste « Conversations » (`/c/<id>`) | réponse, raisonnement replié, sources, actions sous la réponse (copier, modifier, lire à voix haute, informations, bon, mauvais, continuer, régénérer), menu de la conversation | [06](../manuel/06-interroger-ses-documents.md), [09](../manuel/09-converser-au-quotidien.md) |
| Recherche | barre latérale › « Recherche » (Ctrl+K) | champ de recherche, résultats | [09](../manuel/09-converser-au-quotidien.md) |
| Espace de travail › Modèles | « Espace de travail » (`/workspace/models`) | onglets Modèles, Connaissances, Prompts, Skills, Outils ; « Créer », « Ouvrir le menu de création », « Rechercher des modèles », filtre « Tout », « Actions » | [07](../manuel/07-assistant-lie-a-une-base.md) |
| Espace de travail › Connaissances | onglet « Connaissances » (`/workspace/knowledge`) | « Créer », « Rechercher des connaissances », filtres « Tout » et « Toutes Les Sources », liste (nom, auteur, date), « Plus d'options » | [05](../manuel/05-bases-de-connaissances.md) |
| Espace de travail › Prompts | onglet « Prompts » (`/workspace/prompts`) | « Créer », « Ouvrir le menu de création » (importer), « Rechercher des prompts », « Tout » | [11](../manuel/11-prompts-outils-fonctions.md) |
| Espace de travail › Skills | onglet « Skills » (`/workspace/skills`) | « Créer », « Ouvrir le menu de création », « Rechercher des skills », « Tout » | Non couvert : fonction avancée non essayée |
| Espace de travail › Outils | onglet « Outils » (`/workspace/tools`) | « Créer », « Ouvrir le menu de création » (importer, depuis une URL), « Rechercher des outils », « Tout » | [11](../manuel/11-prompts-outils-fonctions.md) |
| Notes | barre latérale › « Notes » (`/notes`) | « Créer », « Ouvrir le menu de création », « Rechercher des notes », « Tout », affichage « Écrire » ou « Liste » | [10](../manuel/10-notes-et-memoire.md) |
| Automatisations | menu du compte › « Automatisations » (`/automations`) | « Créer », « Ouvrir le menu de création », « Rechercher des automatisations », « Tout », « Actions » | [13](../manuel/13-automatisations-canaux-calendrier.md) |
| Calendrier | menu du compte › « Calendrier » (`/calendar`) | « Précédent », « Suivant », « Aujourd'hui », « Mois », « Créer », grille du mois, calendriers « Personal » et « Scheduled Tasks » | [13](../manuel/13-automatisations-canaux-calendrier.md) |
| Canaux | barre latérale › « Canaux » après activation (`/channels/<id>`) | absent tant que « Canaux » n'est pas activé dans Réglages › Administrateur › Général | [13](../manuel/13-automatisations-canaux-calendrier.md) |
| Playground › Conversation | menu du compte › « Playground » (`/playground`) | onglets « Conversation », « Complétions », « Images » ; « Instructions système », message, « Switch to Assistant role », « Contrôles », « Ajouter », « Exécuter » | [15](../manuel/15-administrer.md) |
| Playground › Complétions | onglet « Complétions » (`/playground/completions`) | zone de texte, « Exécuter » | [15](../manuel/15-administrer.md) |
| Playground › Images | onglet « Images » | génération d'images | Non couvert : génération d'images hors périmètre (aucun modèle d'image dans le service central) |

## 2. Fenêtre Réglages, groupe Personnel

Ouverte par menu du compte › « Réglages » (Ctrl+.) ou l'adresse `/?settings=<onglet>`.

| Page ou menu | Chemin d'accès | Éléments (boutons, onglets, réglages) | Manuel qui le couvre |
|---|---|---|---|
| Général | Réglages › « Général » | « Thème », « Langue », « Prompt système », « Paramètres du modèle » (Afficher), « Enregistrer » | [03](../manuel/03-premiers-pas.md), [09](../manuel/09-converser-au-quotidien.md) |
| Interface utilisateur | Réglages › « Interface utilisateur » | zoom, police, mode accessibilité, titre dans l'onglet, localisation, copie formatée, notifications de mise à jour, fenêtre « Quoi de neuf », file d'attente des messages, direction, mode de la page d'accueil, « Taper entrer pour envoyer », « Utilisation de la récupération ciblée », fond d'écran | Non couvert : réglage d'affichage personnel, sans effet sur l'usage des documents |
| Notifications | Réglages › « Notifications » | « Notifications du navigateur », « Son de notification », style du son | Non couvert : réglage d'affichage personnel, sans effet sur l'usage des documents |
| Raccourcis | Réglages › « Raccourcis » | liste des raccourcis clavier, « Réinitialiser les valeurs par défaut » | Non couvert : réglage personnel, sans effet sur l'usage des documents (seul Ctrl+K est cité aux chapitres 03 et 09) |
| Personnalisation | Réglages › « Personnalisation » | « Mémoire » (interrupteur), « Mémoires enregistrées », « Actions » (gérer) | [10](../manuel/10-notes-et-memoire.md) |
| Audio | Réglages › « Audio » | « Moteur de reconnaissance vocale », « Langue », « Envoi automatique après la transcription », « Moteur de Text-to-Speech » (Par défaut, Kokoro.js), « Lire automatiquement la réponse », « Vitesse de lecture de la parole », « Voix », « Autoriser les voix non locales » | [12](../manuel/12-voix-et-recherche-web.md) |
| Contrôles des données | Réglages › « Contrôles des données » | importer, exporter, conversations partagées, « Tout archiver », « Tout supprimer », « Gérer les fichiers » | [09](../manuel/09-converser-au-quotidien.md) |
| Consommation de tokens | Réglages › « Consommation de tokens » | aperçu (jetons, séries), activité « Journalier », « Hebdomadaire », « Cumulatif » | [15](../manuel/15-administrer.md) |
| Conversations archivées | Réglages › « Conversations archivées » | recherche, « Actions », liste | [09](../manuel/09-converser-au-quotidien.md) |
| Compte | Réglages › « Compte » | photo, nom, bio, genre, date de naissance, « Variables utilisateur », « Changer le mot de passe », clés d'API (si autorisées) | [15](../manuel/15-administrer.md) |
| À propos | Réglages › « À propos » | version, « Vérifier les mises à jour disponibles », liens communautaires | [15](../manuel/15-administrer.md) |
| Connexions (personnel) | Réglages › « Connexions » | Non couvert : onglet absent tant que « Direct connexions » est désactivé (choix de cette installation, chapitre 03) | Non couvert : désactivé volontairement, un seul service de modèles partagé |
| Intégrations (personnel) | Réglages › « Intégrations » | Non couvert : onglet absent tant que « Intégrations directes » est désactivé | Non couvert : désactivé volontairement |

## 3. Fenêtre Réglages, groupe Administrateur

| Page ou menu | Chemin d'accès | Éléments (boutons, onglets, réglages) | Manuel qui le couvre |
|---|---|---|---|
| Général | Réglages › Administrateur › « Général » | version, mises à jour, aide, licence ; fonctionnalités : partage communautaire, évaluation des messages, dossiers, souvenirs, skills, notes, commentaires, notifications, « Canaux », Apps, « Calendrier », « Automatisations », webhooks utilisateur, statut utilisateur, filigrane, URL de l'instance, traductions, bannières | [13](../manuel/13-automatisations-canaux-calendrier.md), [15](../manuel/15-administrer.md) |
| Authentification | Réglages › Administrateur › « Authentification » | « Rôle utilisateur par défaut », « Groupe par défaut », « Formulaire de connexion », « Nouveaux comptes », « Clés API », « Expiration du jeton JWT », authentification à plusieurs facteurs, comptes en attente, SSO et LDAP | [14](../manuel/14-comptes-groupes-permissions.md), [15](../manuel/15-administrer.md) ; SSO et LDAP : Non couvert : hors périmètre (fiche) |
| Interface utilisateur | Réglages › Administrateur › « Interface utilisateur » | visibilité des contrôles, « Modèle pour les tâches » (local, externe, paramètres), compaction du contexte, permissions et recherche d'outils, génération du titre, des tags, des suites, des requêtes de recherche, autocomplétion, prompts | [08](../manuel/08-regler-la-lecture-des-documents.md), [15](../manuel/15-administrer.md) |
| Connexions | Réglages › Administrateur › « Connexions » | « API compatibles OpenAI », connexions (roue dentée, interrupteur), « + », « API Ollama », « Direct connexions », cache de la liste des modèles | [03](../manuel/03-premiers-pas.md) |
| Modèles | Réglages › Administrateur › « Modèles » | « Valeurs par défaut du modèle », recherche, filtre « Available », « Actions », liste (crayon, « Plus d'options », interrupteur) | [03](../manuel/03-premiers-pas.md), [07](../manuel/07-assistant-lie-a-une-base.md) |
| Sous-agents | Réglages › Administrateur › « Sous-agents » | « Activer les sous-agents » | Non couvert : fonction avancée non essayée |
| Intégrations | Réglages › Administrateur › « Intégrations » | « Serveurs d'outils externes » (« + »), « Terminal », « Connaissances externes », « Intégrations directes » | [11](../manuel/11-prompts-outils-fonctions.md) ; Terminal : Non couvert : nécessite un serveur « Open Terminal » externe, hors périmètre |
| Documents | Réglages › Administrateur › « Documents » | « Moteur d'extraction de contenu » (Par défaut, Externe, Tika, Docling…), extraction d'images PDF, mode de chargement, « Ignorer l'Embedding et le Retrieval », découpage, taille et chevauchement des chunks, moteur et modèle d'embedding, taille du lot, « Recherche hybride », « Top K », reranking, seuil, texte intégral, modèle RAG, fichiers (taille, nombre, extensions), « Réinitialiser », « Réindexer » | [08](../manuel/08-regler-la-lecture-des-documents.md) |
| Audio | Réglages › Administrateur › « Audio » | appels vocaux (Standard, Realtime), moteur de reconnaissance vocale, URL, clé, modèle, moteur et voix de synthèse, division de la réponse | [12](../manuel/12-voix-et-recherche-web.md) |
| Images | Réglages › Administrateur › « Images » | « Génération d'image » | Non couvert : génération d'images hors périmètre |
| Recherche Web | Réglages › Administrateur › « Recherche Web » | « Recherche Web », moteur, « Ignorer l'Embedding et le Retrieval », proxy, chargeur web, délai, certificat SSL, requêtes simultanées, YouTube | [12](../manuel/12-voix-et-recherche-web.md) |
| Exécution de code | Réglages › Administrateur › « Exécution de code » | « Autoriser l'exécution de code », moteur (pyodide, jupyter), interpréteur de code et son prompt | [11](../manuel/11-prompts-outils-fonctions.md) |
| Pipelines | Réglages › Administrateur › « Pipelines » | « Source », « Aucun pipelines détecté » | Non couvert : nécessite un serveur Pipelines séparé, remplacé par les fonctions (chapitre 11) |
| Analytique | Réglages › Administrateur › « Analytique » | période, aperçu (sessions, jetons, messages, conversations, utilisateurs), activité, modèles, utilisateurs | [15](../manuel/15-administrer.md) |
| Évaluations | Réglages › Administrateur › « Évaluations » | « Modèles d'arène » | [15](../manuel/15-administrer.md) |
| Base de données | Réglages › Administrateur › « Base de données » | importer et exporter la configuration, « Base de données » (télécharger), exporter toutes les conversations, exporter les utilisateurs | [15](../manuel/15-administrer.md) |
| Apps | Réglages › Administrateur › « Apps » | Non couvert : onglet absent tant que « Apps » n'est pas activé dans Général | Non couvert : connexion d'applications externes, hors périmètre |

## 4. Panneau d'administration

| Page ou menu | Chemin d'accès | Éléments (boutons, onglets, réglages) | Manuel qui le couvre |
|---|---|---|---|
| Utilisateurs › Aperçu | menu du compte › « Panneau d'administration » (`/admin/users/overview`) | onglets « Utilisateurs », « Évaluations », « Fonctions », « Réglages » ; « Aperçu », « Groupes » ; recherche, « Ajouter un utilisateur », liste (rôle, e-mail, dernière activité), changement de rôle, « Modifier l'utilisateur » | [14](../manuel/14-comptes-groupes-permissions.md) |
| Utilisateurs › Groupes | « Groupes » (`/admin/users/groups`) | « Rechercher des groupes », « Nouveau groupe », liste | [14](../manuel/14-comptes-groupes-permissions.md) |
| Évaluations › Classement | « Évaluations » (`/admin/evaluations/leaderboard`) | recherche, tableau RK, MODÈLE, NOTE, VICTOIRES, PERDU | [15](../manuel/15-administrer.md) |
| Évaluations › Avis | « Avis » (`/admin/evaluations/feedback`) | liste des avis donnés sur les réponses | [15](../manuel/15-administrer.md) |
| Fonctions | « Fonctions » (`/admin/functions`) | « Créer », « Ouvrir le menu de création », « Rechercher des fonctions », « Tout », « Tag » | [11](../manuel/11-prompts-outils-fonctions.md) |
| Réglages | « Réglages » | ouvre la fenêtre Réglages, groupe Administrateur (section 3) | [03](../manuel/03-premiers-pas.md) |

## 5. Menus

| Page ou menu | Chemin d'accès | Éléments (boutons, onglets, réglages) | Manuel qui le couvre |
|---|---|---|---|
| Menu du compte | barre latérale › nom du compte | « Mettre à jour votre statut », « Espace de travail », « Notes », « Calendrier », « Automatisations », « Playground », « Panneau d'administration », « Réglages » (Ctrl+.), « Déconnexion » | [03](../manuel/03-premiers-pas.md) |
| Menu « + » de la zone de saisie | zone de saisie › « + » | « Téléverser des fichiers », « Prise de vue », « Add Context », « Interpréteur de code » | [04](../manuel/04-premiere-question.md), [06](../manuel/06-interroger-ses-documents.md), [11](../manuel/11-prompts-outils-fonctions.md) |
| Sélecteur de modèle | zone de saisie › nom du modèle | recherche, liste des modèles, « Définir comme valeur par défaut » | [03](../manuel/03-premiers-pas.md), [09](../manuel/09-converser-au-quotidien.md) ; « Définir comme valeur par défaut » relevé à la [capture 03/12](../../banc-essai/resultats/open-webui/captures/03-premiers-pas/12-selecteur-modeles.txt) |

## 6. Captures de repérage

Une capture brute par page (sans annotation), prise par le scénario de la carte.

| Page | Capture |
|---|---|
| Accueil | ![Accueil](../img/carte/accueil.png) |
| Modèles (espace de travail) | ![Modèles](../img/carte/modeles.png) |
| Connaissances | ![Connaissances](../img/carte/connaissances.png) |
| Prompts | ![Prompts](../img/carte/prompts.png) |
| Skills | ![Skills](../img/carte/skills.png) |
| Outils | ![Outils](../img/carte/outils.png) |
| Notes | ![Notes](../img/carte/notes.png) |
| Automatisations | ![Automatisations](../img/carte/automatisations.png) |
| Calendrier | ![Calendrier](../img/carte/calendrier.png) |
| Playground | ![Playground](../img/carte/playground.png) |
| Playground, Complétions | ![Complétions](../img/carte/playground-completions.png) |
| Utilisateurs | ![Utilisateurs](../img/carte/admin-utilisateurs.png) |
| Groupes | ![Groupes](../img/carte/admin-groupes.png) |
| Classement | ![Classement](../img/carte/admin-classement.png) |
| Avis | ![Avis](../img/carte/admin-avis.png) |
| Fonctions | ![Fonctions](../img/carte/admin-fonctions.png) |
| Analytique (panneau) | ![Analytique](../img/carte/admin-analytique.png) |
| Menu du compte | ![Menu du compte](../img/carte/menu-compte.png) |
| Réglages › Général | ![Général](../img/carte/reglages-general.png) |
| Réglages › Interface utilisateur | ![Interface](../img/carte/reglages-interface.png) |
| Réglages › Notifications | ![Notifications](../img/carte/reglages-notifications.png) |
| Réglages › Raccourcis | ![Raccourcis](../img/carte/reglages-shortcuts.png) |
| Réglages › Personnalisation | ![Personnalisation](../img/carte/reglages-personalization.png) |
| Réglages › Audio | ![Audio](../img/carte/reglages-audio.png) |
| Réglages › Contrôles des données | ![Données](../img/carte/reglages-data-controls.png) |
| Réglages › Consommation de tokens | ![Consommation](../img/carte/reglages-usage.png) |
| Réglages › Conversations archivées | ![Archives](../img/carte/reglages-archived-chats.png) |
| Réglages › Compte | ![Compte](../img/carte/reglages-account.png) |
| Réglages › À propos | ![À propos](../img/carte/reglages-about.png) |
| Administrateur › Général | ![Général admin](../img/carte/reglages-admin-general.png) |
| Administrateur › Authentification | ![Authentification](../img/carte/reglages-admin-authentication.png) |
| Administrateur › Interface utilisateur | ![Interface admin](../img/carte/reglages-admin-interface.png) |
| Administrateur › Connexions | ![Connexions](../img/carte/reglages-admin-connections.png) |
| Administrateur › Modèles | ![Modèles admin](../img/carte/reglages-admin-models.png) |
| Administrateur › Sous-agents | ![Sous-agents](../img/carte/reglages-admin-subagents.png) |
| Administrateur › Intégrations | ![Intégrations](../img/carte/reglages-admin-integrations.png) |
| Administrateur › Documents | ![Documents](../img/carte/reglages-admin-documents.png) |
| Administrateur › Audio | ![Audio admin](../img/carte/reglages-admin-audio.png) |
| Administrateur › Images | ![Images](../img/carte/reglages-admin-images.png) |
| Administrateur › Recherche Web | ![Recherche Web](../img/carte/reglages-admin-web.png) |
| Administrateur › Exécution de code | ![Exécution de code](../img/carte/reglages-admin-code-execution.png) |
| Administrateur › Pipelines | ![Pipelines](../img/carte/reglages-admin-pipelines.png) |
| Administrateur › Analytique | ![Analytique admin](../img/carte/reglages-admin-analytics.png) |
| Administrateur › Évaluations | ![Évaluations](../img/carte/reglages-admin-evaluations.png) |
| Administrateur › Base de données | ![Base de données](../img/carte/reglages-admin-db.png) |

## Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| Un onglet de Réglages ouvre « Général » | onglet masqué par la configuration (Connexions et Intégrations personnelles, Apps) | activer la fonction correspondante dans le groupe Administrateur |
| Le groupe « Administrateur » est absent | compte sans rôle administrateur | se connecter avec le compte administrateur |

## Sources

- Scénario : `banc-essai/open-webui/captures/carte.py` ; relevés : `banc-essai/resultats/open-webui/captures/carte/*.txt` et `*.json`.
- Code au tag v0.13.3 : `banc-essai/resultats/open-webui/cadrage-source-v0.13.3.md` (section 4).
