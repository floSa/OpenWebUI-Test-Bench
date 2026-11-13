"""Serveur MCP local (Streamable HTTP) pour le manuel : deux fonctions sur l'entreprise fictive Vélanor.

Lancé dans un conteneur de l'image Open WebUI (le paquet Python « mcp » 2.3.0 y est déjà installé), sur le réseau rag-local,
sans port publié : Open WebUI le joint à http://rag-mcp-velanor:8000/mcp. Aucun accès réseau sortant ni disque.
"""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("velanor")

SITES = {"nantes": "12 quai de la Fosse, 44000 Nantes (siège, assemblage)",
         "saint-nazaire": "seconde usine d'assemblage, ouverture prévue en septembre 2026"}


@mcp.tool()
def site_velanor(ville: str) -> str:
    """Adresse ou description d'un site de Vélanor (nantes, saint-nazaire)."""
    return SITES.get(ville.strip().lower(), "Site inconnu. Sites : " + ", ".join(SITES))


@mcp.tool()
def jours_ouvres(debut: str, fin: str) -> int:
    """Nombre de jours ouvrés (lundi à vendredi) entre deux dates AAAA-MM-JJ incluses."""
    import datetime as dt
    d, f = dt.date.fromisoformat(debut), dt.date.fromisoformat(fin)
    return sum(1 for i in range((f - d).days + 1) if (d + dt.timedelta(i)).weekday() < 5)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
