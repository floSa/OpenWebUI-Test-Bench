"""Exemple 03 : créer la base « Exemple API », y téléverser un document du corpus, attendre sa lecture, l'ajouter.
Routes : POST /api/v1/knowledge/create, POST /api/v1/files/?process=true, GET /api/v1/files/{id}/process/status,
POST /api/v1/knowledge/{id}/file/add. L'exemple 06 supprime ce qui est créé ici."""
from pathlib import Path
from owui import attendre_traitement, liste, requete, televerser

NOM = "Exemple API"
DOCUMENT = Path(__file__).resolve().parents[2] / "banc-essai/corpus/documents/rapport-annuel-2025.pdf"

if any(b["name"] == NOM for b in liste(requete("GET", "/api/v1/knowledge/"))):
    raise SystemExit(f"la base « {NOM} » existe déjà : lancer d'abord l'exemple 06 (ménage)")
base = requete("POST", "/api/v1/knowledge/create", {"name": NOM, "description": "Base créée par les exemples de l'annexe A3"})
print("base créée :", base["name"], "| id", base["id"])

f = televerser(DOCUMENT)
print("fichier téléversé :", f["filename"], "| id", f["id"], "| statut initial", (f.get("data") or {}).get("status"))
statut, duree = attendre_traitement(f["id"])
print(f"traitement : {statut['status']} en {duree} s" + (f" ({statut.get('error')})" if statut.get("error") else ""))

k = requete("POST", f"/api/v1/knowledge/{base['id']}/file/add", {"file_id": f["id"]})
fichiers = liste(requete("GET", f"/api/v1/knowledge/{base['id']}/files"))
print("fichiers de la base :", [x.get("filename") or x.get("meta", {}).get("name") for x in fichiers])
