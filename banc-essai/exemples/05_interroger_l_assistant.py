"""Exemple 05 : question à l'assistant personnalisé existant « Assistant qualité Vélanor » (id assistant-qualit-vlanor),
en lecture seule. Ses consignes s'appliquent toujours ; sa base (« Démo Vélanor ») n'est consultée par l'API que si
la requête demande l'appel de fonctions « legacy » (params.function_calling). Les deux appels sont faits pour comparer."""
import time
from owui import requete, sources

question = "Quel taux de cellules défectueuses a été mesuré chez Batterix lors de l'audit ?"
for params in ({}, {"function_calling": "legacy"}):
    corps = {
        "model": "assistant-qualit-vlanor",
        "stream": False,
        "messages": [{"role": "user", "content": question}],
        "params": params,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    t0 = time.time()
    r = requete("POST", "/api/chat/completions", corps)
    print(f"--- params = {params}  ({time.time() - t0:.1f} s)")
    print("question :", question)
    print("réponse :", r["choices"][0]["message"]["content"].strip())
    print("sources :", "aucune" if not sources(r) else "")
    for doc, page, extrait in sources(r):
        print(f"  - {doc}, page {page} : {extrait}")
