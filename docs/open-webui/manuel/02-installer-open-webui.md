# 02. Installer Open WebUI

> Ce chapitre apprend à installer Open WebUI sous Windows 11 avec WSL2, à l'ouvrir dans le navigateur, puis à l'arrêter, le redémarrer et le supprimer.
> **Point de départ** : un terminal Ubuntu (WSL2) ouvert sur le poste, Docker Desktop démarré, et le service de modèles LLM-Service installé et démarré sur le même poste (voir « Ce qu'il faut savoir »).
> **Durée** : environ 15 minutes, dont 2 à 10 de téléchargement selon la connexion. **Avant** : chapitre 01.

**Attention** : l'application n'est ouverte qu'au poste lui-même (adresse `127.0.0.1`). Ne pas modifier les ports dans les fichiers fournis : une adresse ouverte sur le réseau exposerait les documents, les conversations et la clé du service de modèles.

## Ce qu'il faut savoir

Open WebUI tient dans **un seul conteneur Docker** (un « conteneur » est une petite machine isolée qui contient l'application et tout ce dont elle a besoin). Ce conteneur ne fait tourner aucun modèle d'IA : les réponses, la représentation des textes (les « embeddings », voir le [glossaire](18-glossaire.md)) et la transcription de la voix sont demandées à un **service de modèles** installé à part sur le même poste : le service LLM central, projet LLM-Service (https://github.com/floSa/llm-service). Il s'installe en suivant son propre README, avant ce chapitre, et se démarre par son script `scripts/demarrer.sh` (dans le dossier où il a été installé ; ajouter `cpu` sans carte graphique NVIDIA). Il est protégé par une clé : la valeur de `LITELLM_MASTER_KEY` dans le fichier `.env` de LLM-Service (ou celle que fournit la personne qui gère ce service).

Ce service a deux adresses : depuis le terminal du poste, `http://127.0.0.1:8080/v1` ; depuis Open WebUI, qui tourne dans un conteneur Docker relié au service par un réseau Docker nommé `llm-net`, `http://llm-central:8080/v1`.

L'installation se fait avec un script fourni dans ce dépôt. Il télécharge l'image officielle d'Open WebUI à une version précise, crée un dossier de données, génère un secret de session propre au poste et démarre l'application **déjà branchée** au service de modèles : l'adresse et la clé sont lues dans le fichier `.env` du dépôt au premier démarrage, puis gardées dans les réglages de l'application (modifiables ensuite dans l'interface, chapitre 03). Le compte administrateur se crée dans le navigateur.

Les données (documents, conversations, comptes, réglages) sont rangées dans le dossier `donnees/open-webui/` du dépôt. Les supprimer efface tout.

## Vérifier les prérequis

**Étape 1. Vérifier Docker**
*Où* : terminal Ubuntu.

```bash
docker version --format '{{.Server.Version}}'
docker compose version
```

*Résultat* : deux numéros de version s'affichent (par exemple `29.9.3` et `Docker Compose version v5.7.0`). Une erreur signifie que Docker Desktop n'est pas démarré, ou que l'intégration WSL n'est pas activée dans ses réglages (Docker Desktop › Settings › Resources › WSL integration).

**Étape 2. Récupérer le dépôt**
*Où* : terminal Ubuntu, dans le dossier où ranger le projet.

```bash
git clone https://github.com/floSa/OpenWebUI-Test-Bench.git
cd OpenWebUI-Test-Bench
```

*Résultat* : le dossier `OpenWebUI-Test-Bench` existe ; toutes les commandes suivantes se lancent depuis ce dossier.

**Étape 3. Créer la clé du banc pour le service de modèles**
*Où* : terminal Ubuntu, dossier du dépôt.

```bash
cp .env.example .env
~/mes_projets/Projet-IA/LLM-Service/scripts/cle.sh creer openwebui-test-bench --dans "$PWD/.env" --noms LLM_CENTRAL_URL,LLM_CENTRAL_KEY
```

Le script de LLM-Service crée une clé propre à ce banc (nom `openwebui-test-bench`) et l'écrit, sans l'afficher, sur les lignes `LLM_CENTRAL_URL` et `LLM_CENTRAL_KEY` du fichier `.env`. La clé maîtresse de LLM-Service (`LITELLM_MASTER_KEY`) ne se recopie jamais ici. Si une clé existe déjà pour ce nom, le script refuse : la révoquer d'abord avec `~/mes_projets/Projet-IA/LLM-Service/scripts/cle.sh revoquer openwebui-test-bench`, puis relancer la commande. Procédure complète : `docs/brancher-une-application.md` du dépôt LLM-Service. Ce fichier `.env` n'est jamais envoyé sur GitHub.

*Résultat* : le fichier `.env` contient la clé ; il n'est lisible que sur le poste.

**Étape 4. Vérifier que le service de modèles répond**
*Où* : terminal Ubuntu, dossier du dépôt.

```bash
outils/communs/llm_central_sante.sh --essai
```

*Résultat* : la liste des modèles s'affiche (`chat`, `embed`, `rerank`, `transcribe` et quelques autres), puis une ligne par essai : un mot de réponse, `dimensions : 1024`, deux scores de tri, le début de la transcription d'un message vocal. Si la commande répond « service injoignable », démarrer le service avec le script `scripts/demarrer.sh` du dossier de LLM-Service (sur le poste d'essai : `~/mes_projets/Projet-IA/LLM-Service/scripts/demarrer.sh` ; ajouter `cpu` sans carte graphique NVIDIA), puis relancer la vérification.

## Installer et ouvrir l'application

**Étape 5. Lancer l'installation**
*Où* : terminal Ubuntu, dossier du dépôt.

```bash
outils/open-webui/installer.sh
```

Le script télécharge l'image (4,6 Go, une seule fois), écrit le secret de session dans `donnees/open-webui/options.env`, démarre le conteneur `rag-open-webui` et attend qu'il réponde.

*Résultat* : les dernières lignes affichent `Open WebUI prêt : http://127.0.0.1:3000`, la ligne `rag-open-webui 127.0.0.1:3000->8080/tcp` (l'application n'écoute que sur le poste), `ports : tous liés à 127.0.0.1`, la version (`"version":"0.13.3"`), la durée et la mémoire prise au repos (environ 1 Go). Sans téléchargement, l'installation prend moins d'une minute.

**Étape 6. Ouvrir Open WebUI dans le navigateur**
*Où* : navigateur de Windows (Edge, Firefox, Chrome), barre d'adresse.

Taper `http://127.0.0.1:3000` puis Entrée.

![Écran d'accueil au premier lancement](../img/03-premiers-pas/01-accueil.png)
*Écran : accueil d'une instance neuve, « Bienvenue dans votre espace IA. ».*

| N° | Élément | Rôle |
|---|---|---|
| 1 | « Démarrer » | ouvre le formulaire de création du premier compte (chapitre 03) |

*Résultat* : la page d'accueil s'affiche, en français si le navigateur est en français. L'installation est terminée ; la suite se passe au chapitre 03.

## Arrêter, redémarrer, supprimer

**Étape 7. Voir l'état de l'application**
*Où* : terminal Ubuntu, dossier du dépôt.

```bash
outils/open-webui/etat.sh
```

*Résultat* : l'état du conteneur (`Up … (healthy)`), la réponse `{"status":true}`, la version, la mémoire utilisée, la place occupée par les données, une ligne vide sous « ports publiés hors de 127.0.0.1 » (aucun port ouvert au réseau) et la liste des modèles du service central.

**Étape 8. Arrêter Open WebUI**
*Où* : terminal Ubuntu, dossier du dépôt.

```bash
outils/open-webui/arreter.sh
```

*Résultat* : `Open WebUI arrêté.` Les documents, conversations et réglages sont conservés. Le service de modèles, partagé avec d'autres applications, continue de tourner.

**Étape 9. Redémarrer Open WebUI**
*Où* : terminal Ubuntu, dossier du dépôt.

```bash
outils/open-webui/demarrer.sh
```

*Résultat* : `Open WebUI prêt : http://127.0.0.1:3000` après une vingtaine de secondes. Dans le navigateur, l'écran de connexion demande l'adresse e-mail et le mot de passe choisis au chapitre 03.

**Étape 10. Tout supprimer**
*Où* : terminal Ubuntu, dossier du dépôt.

```bash
outils/communs/nettoyer.sh open-webui
```

Le script annonce ce qu'il va supprimer et demande de taper `oui`. Il supprime les conteneurs de l'application et le dossier `donnees/open-webui/` (documents, conversations, comptes, réglages, clés d'API). Il ne touche pas au service de modèles. L'image téléchargée reste dans Docker ; pour la retirer aussi : `docker image rm ghcr.io/open-webui/open-webui:v0.13.3`.

*Résultat* : `Terminé.` ; l'adresse `http://127.0.0.1:3000` ne répond plus.

## Bon à savoir

- Le script d'installation peut être relancé sans risque : il garde le secret de session, les réglages et les données existants.
- L'adresse et la clé du service de modèles ne sont lues dans `.env` qu'au **premier** démarrage. Pour les changer ensuite, passer par l'interface (chapitre 03, « Vérifier la connexion aux modèles »).
- L'image installée est l'image standard. Les variantes `:ollama` (avec un serveur de modèles intégré) et `:cuda` (calculs sur carte graphique dans l'application) ne servent pas ici : les modèles viennent du service central.
- Le secret de session est fixé par le script : sans lui, Open WebUI en génère un à chaque recréation du conteneur et toutes les sessions ouvertes sont perdues.

## En cas de problème

| Symptôme | Cause | Que faire |
|---|---|---|
| `clé absente : copier .env.example en .env…` | le fichier `.env` manque ou sa clé est vide | refaire l'étape 3 |
| `réseau llm-net absent` | le service de modèles n'est pas démarré (`llm-net` est le réseau Docker qu'il crée) | démarrer LLM-Service (`scripts/demarrer.sh` de son dossier), puis relancer l'installation |
| `Open WebUI ne répond pas après 300 s` | démarrage en échec | `docker logs rag-open-webui` ; voir le [chapitre 17](17-en-cas-de-probleme.md) |
| La page affiche l'écran de connexion au lieu de « Bienvenue » | un compte existe déjà dans `donnees/open-webui/` | se connecter avec le compte existant, ou tout supprimer (étape 10) puis réinstaller |

---
*Version décrite : Open WebUI 0.13.3, essais du 13 novembre 2026. Détails et preuves : [rapport d'essais](../annexes/A6-rapport-d-essais.md).*
