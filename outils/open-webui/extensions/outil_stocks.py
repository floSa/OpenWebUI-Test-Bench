"""
title: Stocks Vélanor
author: banc d'essai (fictif)
description: Donne le stock d'une pièce de l'entreprise fictive Vélanor (données d'octobre 2025, figées dans le code).
version: 1.0.0
"""
# Outil écrit pour le manuel : aucune dépendance, aucun accès réseau ni disque.

STOCKS = {
    "batterie 500 wh": 412,
    "moteur central": 238,
    "cadre aluminium m": 156,
    "écran de commande": 590,
}


class Tools:
    def stock_piece(self, piece: str) -> str:
        """
        Donne le nombre d'unités en stock d'une pièce chez Vélanor.
        :param piece: nom de la pièce, par exemple « batterie 500 Wh » ou « moteur central ».
        """
        cle = piece.strip().lower()
        for nom, qte in STOCKS.items():
            if nom in cle or cle in nom:
                return f"Stock de « {nom} » au 31 octobre 2025 : {qte} unités (source : outil Stocks Vélanor)."
        return "Pièce inconnue. Pièces suivies : " + ", ".join(STOCKS)
