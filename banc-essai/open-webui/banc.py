#!/usr/bin/env python3
"""Adaptateur du banc commun pour Open WebUI (API de l'instance).

Indexation (kit/fiches/05-open-webui.md, « Adaptateur du banc ») : base Knowledge « <base> » créée par l'API, chaque
fichier du corpus téléversé (POST /api/v1/files/, lecture, découpage et vecteurs calculés par `embed` du service central),
attente de la fin du traitement, puis rattachement à la base. Questions : POST /api/chat/completions, modèle `chat`,
base attachée (files: [{type: collection, id}]), sans flux, une conversation neuve par question (pas d'historique).
Sources : champ « sources » de la réponse (document, page_label, extrait, distance ou score du reranker).
Le raisonnement du modèle arrive à part (reasoning_content) : il est gardé dans reponse_brute, pas noté.

Les réglages de recherche d'Open WebUI sont globaux (Paramètres d'administration › Documents) : l'option --reglages
les écrit par POST /api/v1/retrieval/config/update avant le banc ; la configuration effective est relue et gardée dans le JSON.

Usage :
  banc-essai/open-webui/banc.py --etiquette defaut-sans-rerank [--base Banc] [--reindexer]
       [--reglages '{"ENABLE_RAG_HYBRID_SEARCH": true, ...}'] [--limite N] [--ids Q01,Q02] [--sans-juge]
"""
import argparse, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "communs/banc"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import commun  # noqa: E402
from client import API, BASE, sans_pensee  # noqa: E402

APP = ["rag-open-webui", "rag-docling-serve"]
MODELES = ["llm-central", "llm-swap", "llm-speaches"]
CLES = ("TOP_K", "TOP_K_RERANKER", "RELEVANCE_THRESHOLD", "ENABLE_RAG_HYBRID_SEARCH", "HYBRID_BM25_WEIGHT",
        "RAG_FULL_CONTEXT", "BYPASS_EMBEDDING_AND_RETRIEVAL", "CONTENT_EXTRACTION_ENGINE", "DOCLING_SERVER_URL",
        "PDF_EXTRACT_IMAGES", "PDF_LOADER_MODE", "RAG_RERANKING_ENGINE", "RAG_RERANKING_MODEL",
        "RAG_EXTERNAL_RERANKER_URL", "TEXT_SPLITTER", "CHUNK_SIZE", "CHUNK_OVERLAP")


class Adaptateur:
    nom = "Open WebUI"

    def __init__(self, a):
        self.a, self.api = a, API()
        self.kid = None
        reglages = json.loads(a.reglages) if a.reglages else {}
        if a.rerank:  # reranker externe du service central (actif seulement avec la recherche hybride)
            reglages.update({"ENABLE_RAG_HYBRID_SEARCH": True, "RAG_RERANKING_ENGINE": "external",
                             "RAG_EXTERNAL_RERANKER_URL": "http://llm-central:8080/v1/rerank",
                             "RAG_EXTERNAL_RERANKER_API_KEY": commun._env()["LLM_CENTRAL_KEY"],
                             "RAG_RERANKING_MODEL": "rerank"})
        if a.taches:  # tâches de fond (réécriture des requêtes de recherche, titres…) : Réglages › Interface utilisateur
            t = self.api.get("/api/v1/tasks/config"); t.update(json.loads(a.taches))
            r = self.api.post("/api/v1/tasks/config/update", t)
            print("tâches :", {k: r.get(k) for k in json.loads(a.taches)}, flush=True)
        if reglages:
            r = self.api.post("/api/v1/retrieval/config/update", reglages)
            print("réglages appliqués :", {k: r.get(k) for k in reglages if k in r and "KEY" not in k}, flush=True)

    def _base(self):
        if not self.kid:
            bases = self.api.get("/api/v1/knowledge/")
            bases = bases.get("items", bases) if isinstance(bases, dict) else bases
            ex = [b for b in bases if b["name"] == self.a.base]
            if ex:
                self.kid = ex[0]["id"]
            else:
                self.kid = self.api.post("/api/v1/knowledge/create",
                                         {"name": self.a.base, "description": "Corpus du banc (Vélanor, fictif)"})["id"]
        return self.kid

    def _fichiers_base(self):
        k = self.api.get(f"/api/v1/knowledge/{self._base()}/files")
        return k.get("items", k) if isinstance(k, dict) else k

    def indexer(self, fichiers):
        kid = self._base()
        deja = self._fichiers_base()
        if deja and not self.a.reindexer:
            return {"base": kid, "documents": len(deja), "reprise": "base déjà indexée, réutilisée"}
        detail = []
        for f in fichiers:
            t0 = time.time()
            try:
                fo = self.api.televerser(f)
                st = fo.get("_statut", {})
                ajout = self.api.post(f"/api/v1/knowledge/{kid}/file/add", {"file_id": fo["id"]})
                detail.append({"fichier": f.name, "statut": st.get("status"), "erreur": st.get("error"),
                               "caracteres": len(((fo.get("data") or {}).get("content")) or ""),
                               "duree_s": round(time.time() - t0, 1)})
            except Exception as e:  # un format refusé ne bloque pas le banc : consigné tel quel
                detail.append({"fichier": f.name, "statut": "échec", "erreur": str(e)[:300],
                               "duree_s": round(time.time() - t0, 1)})
            print(f"  {f.name}: {detail[-1]}", flush=True)
        return {"base": kid, "fichiers": detail}

    def demander(self, question):
        corps = {"model": "chat", "stream": False, "messages": [{"role": "user", "content": question}],
                 "files": [{"type": "collection", "id": self._base()}]}
        if self.a.corps:  # champs ajoutés à chaque requête (ex. réflexion de `chat` coupée)
            corps.update(json.loads(self.a.corps))
        r = self.api.post("/api/chat/completions", corps)
        m = r["choices"][0]["message"]
        cits = []
        for s in r.get("sources") or []:
            dist = s.get("distances") or []
            for i, (doc, meta) in enumerate(zip(s.get("document") or [], s.get("metadata") or [])):
                page = meta.get("page_label") or (meta.get("page") + 1 if isinstance(meta.get("page"), int) else None)
                try:
                    page = int(page) if page is not None else None
                except (TypeError, ValueError):
                    page = None
                cits.append({"document": meta.get("name") or meta.get("source") or "", "page": page,
                             "extrait": (doc or "")[:300], "score": dist[i] if i < len(dist) else None})
        brute = (m.get("content") or "")
        return {"reponse": sans_pensee(brute), "citations": cits,
                "reponse_brute": {"content": brute, "reasoning_len": len(m.get("reasoning_content") or ""),
                                  "usage": r.get("usage")}}

    def config(self):
        c = self.api.get("/api/v1/retrieval/config")
        e = self.api.get("/api/v1/retrieval/embedding")
        tc = self.api.get("/api/v1/tasks/config")
        return {"url": BASE, "base": self.a.base, "modele": "chat", "corps": self.a.corps,
                "taches": {k: tc.get(k) for k in ("TASK_MODEL", "TASK_MODEL_PARAMS", "ENABLE_RETRIEVAL_QUERY_GENERATION")},
                "recherche": {k: c.get(k) for k in CLES},
                "embedding": {k: e.get(k) for k in ("RAG_EMBEDDING_ENGINE", "RAG_EMBEDDING_MODEL", "RAG_EMBEDDING_BATCH_SIZE")}}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--etiquette", required=True)
    p.add_argument("--base", default="Banc")
    p.add_argument("--reindexer", action="store_true")
    p.add_argument("--reglages", help="JSON écrit par /api/v1/retrieval/config/update avant le banc")
    p.add_argument("--rerank", action="store_true", help="recherche hybride et reranker externe `rerank` du service central")
    p.add_argument("--taches", help="JSON fusionné dans /api/v1/tasks/config (ex. génération des requêtes de recherche)")
    p.add_argument("--corps", help='JSON fusionné dans chaque requête (ex. {"chat_template_kwargs": {"enable_thinking": false}})')
    p.add_argument("--limite", type=int)
    p.add_argument("--ids")
    p.add_argument("--sans-juge", action="store_true")
    a = p.parse_args()
    ad = Adaptateur(a)
    res = commun.lancer(ad, a.etiquette, APP, MODELES, indexer=True, juge=not a.sans_juge, limite=a.limite,
                        ids=a.ids.split(",") if a.ids else None)
    commun.ecrire(res, commun.RACINE / "banc-essai/resultats/open-webui")


if __name__ == "__main__":
    main()
