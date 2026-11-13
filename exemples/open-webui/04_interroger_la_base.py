"""Exemple 04 : question posée à la base « Exemple API » (files: [{type: collection, id}]) ; réponse et sources.
Sans session_id, Open WebUI applique la recherche classique : passages trouvés, insérés dans la question, renvoyés
dans le champ « sources » de la réponse."""
import time
from owui import liste, requete, sources

base = next(b for b in liste(requete("GET", "/api/v1/knowledge/")) if b["name"] == "Exemple API")
question = "Quel a été le chiffre d'affaires du troisième trimestre 2025 ?"
corps = {
    "model": "chat",
    "stream": False,
    "messages": [{"role": "user", "content": question}],
    "files": [{"type": "collection", "id": base["id"]}],
    "chat_template_kwargs": {"enable_thinking": False},
}
t0 = time.time()
r = requete("POST", "/api/chat/completions", corps)
print(f"question : {question}  ({time.time() - t0:.1f} s)")
print("réponse :", r["choices"][0]["message"]["content"].strip())
print("sources :")
for doc, page, extrait in sources(r):
    print(f"  - {doc}, page {page} : {extrait}")
