"""Exemple 02 : question simple au modèle `chat`, sans document (POST /api/chat/completions, sans flux).
La réflexion du modèle est coupée (chat_template_kwargs.enable_thinking = false) pour répondre en quelques secondes."""
import time
from owui import requete

corps = {
    "model": "chat",
    "stream": False,
    "messages": [{"role": "user", "content": "En une phrase : à quoi sert une base de connaissances dans un assistant ?"}],
    "chat_template_kwargs": {"enable_thinking": False},  # transmis tel quel au service de modèles
}
t0 = time.time()
r = requete("POST", "/api/chat/completions", corps)
print(f"durée : {time.time() - t0:.1f} s")
print("modèle :", r.get("model"))
print("réponse :", r["choices"][0]["message"]["content"].strip())
print("jetons :", r.get("usage", {}).get("prompt_tokens"), "en entrée,", r.get("usage", {}).get("completion_tokens"), "en sortie")
