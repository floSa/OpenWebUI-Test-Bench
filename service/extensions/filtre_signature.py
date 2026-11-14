"""
title: Mention de source interne
author: banc d'essai (fictif)
description: Filtre qui ajoute une consigne de réponse en français et une mention en fin de réponse.
version: 1.0.0
"""
# Filtre écrit pour le manuel : aucune dépendance, aucun accès réseau ni disque.
from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        mention: str = Field(default="Réponse générée par l'assistant interne Vélanor.",
                             description="Texte ajouté à la fin de chaque réponse")

    def __init__(self):
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: dict = None) -> dict:
        # avant l'envoi au modèle : consigne de langue ajoutée en tête de conversation
        body.setdefault("messages", []).insert(0, {"role": "system", "content": "Réponds toujours en français."})
        return body

    def outlet(self, body: dict, __user__: dict = None) -> dict:
        # après la réponse : mention ajoutée au dernier message de l'assistant
        for m in reversed(body.get("messages", [])):
            if m.get("role") == "assistant":
                m["content"] = (m.get("content") or "") + f"\n\n_{self.valves.mention}_"
                break
        return body
