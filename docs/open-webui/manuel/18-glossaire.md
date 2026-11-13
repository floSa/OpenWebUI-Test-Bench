# 18. Glossaire

> Ce chapitre rassemble les mots employés dans le manuel, avec leur sens simple.
> **Point de départ** : n'importe quel chapitre, quand un mot n'est pas clair.
> **Durée** : à la demande. **Avant** : aucun.

## Ce qu'il faut savoir

Les termes communs à toute la série de manuels (RAG, embedding, jeton, reranker…) sont définis dans le [glossaire de la série](../../glossaire.md). Le tableau ci-dessous reprend ceux qui reviennent le plus dans ce manuel, avec le libellé affiché par Open WebUI quand il existe. L'interface est en français, mais certains libellés restent en anglais : ils sont cités tels quels.

## Mots du manuel

| Mot | Libellé dans l'interface | Sens |
|---|---|---|
| Administrateur | « Administrateur », « admin » | compte qui règle l'instance pour tout le monde ; le premier compte créé l'est d'office |
| Base de connaissances | « Connaissances », « Base de connaissances » | ensemble de documents rangés sous un nom, que les conversations peuvent interroger |
| Barre latérale | « Ouvrir la barre latérale » | colonne de gauche : nouvelle conversation, recherche, notes, espace de travail, liste des conversations |
| Citation, source | « Sources », numéros « [1] » | renvoi, dans une réponse, vers le passage de document qui la justifie |
| Clé d'API | « Clé API » | mot de passe technique qui permet à un programme d'utiliser l'instance à la place d'une personne |
| Connexion | « Connexions », « API compatibles OpenAI » | adresse et clé d'un service de modèles déclaré dans l'instance |
| Conteneur | — | petite machine isolée lancée par Docker, qui contient l'application |
| Conversation temporaire | « conversation temporaire » | conversation qui n'est pas enregistrée dans la liste |
| Découpage | « Taille des chunks », « Chevauchement des chunks » | coupure d'un document en passages de taille fixe avant le calcul des embeddings |
| Docling | « Docling » (moteur d'extraction) | lecteur de documents qui reconnaît aussi le texte des pages scannées ; fourni ici par un conteneur à part |
| Embedding | « Embedding », « Modèle d'embedding » | suite de nombres qui représente le sens d'un passage ; deux passages proches ont des embeddings proches |
| Espace de travail | « Espace de travail » | page qui réunit les modèles personnalisés, les bases de connaissances, les prompts, les outils et les skills |
| Fonction | « Fonctions » | extension écrite en Python et installée par l'administrateur : filtre, pipeline ou action |
| Groupe | « Groupes » | ensemble de comptes qui reçoit les mêmes droits et les mêmes partages |
| Instance | — | une installation d'Open WebUI, avec ses comptes et ses données |
| Jeton | « tokens » | unité de texte traitée par un modèle, environ trois quarts de mot en français |
| MCP | « MCP » | protocole qui permet au modèle d'appeler les fonctions d'un programme externe (serveur MCP) |
| Mémoire | « Mémoire », « Souvenirs » | informations durables sur l'utilisateur, ajoutées à chaque conversation |
| Modèle | « Modèle sélectionné » | programme d'IA qui écrit les réponses ; ici `chat`, servi par le service de modèles |
| Modèle personnalisé | « Modèles » (espace de travail) | assistant construit sur un modèle, avec un nom, une consigne et, au besoin, des bases de connaissances |
| Note | « Notes » | page de texte libre, enregistrée dans l'instance, que le modèle peut aider à rédiger |
| Outil | « Outils » | fonction écrite en Python que le modèle peut appeler pendant une conversation |
| Passage | « chunk » | morceau de document retrouvé pour répondre |
| Prompt | « Prompts » | texte réutilisable, appelé dans la zone de saisie par une commande commençant par « / » |
| Raisonnement | « Pensé pendant … » | réflexion que le modèle écrit avant sa réponse ; repliée au-dessus de la réponse |
| Recherche hybride | « Recherche hybride » | recherche qui combine les mots exacts et le sens des passages |
| Reranker | « Moteur de ré-ranking », « Modèle de ré-ranking » | modèle qui reclasse les passages retrouvés pour mettre les plus utiles en tête ; ici `rerank` |
| Réglages | « Réglages » | fenêtre unique qui réunit les réglages personnels et, pour un administrateur, ceux de l'instance |
| Service de modèles | — | service LLM central (projet LLM-Service) qui fournit `chat`, `embed`, `rerank` et `transcribe` |
| Transcription | « Speech-to-Text », « Saisie vocale » | conversion de la parole en texte ; ici par `transcribe` |

---
*Version décrite : Open WebUI 0.13.3, essais du 13 novembre 2026. Détails et preuves : [rapport d'essais](../annexes/A6-rapport-d-essais.md).*
