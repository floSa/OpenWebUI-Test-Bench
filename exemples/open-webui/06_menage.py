"""Exemple 06 : ménage. Supprime chaque base nommée « Exemple API » et les fichiers qu'elle contient
(DELETE /api/v1/knowledge/{id}/delete, DELETE /api/v1/files/{id}), puis liste les bases restantes."""
from owui import liste, requete

for b in liste(requete("GET", "/api/v1/knowledge/")):
    if b["name"] != "Exemple API":
        continue
    fichiers = liste(requete("GET", f"/api/v1/knowledge/{b['id']}/files"))
    print("suppression de la base :", b["name"], "->", requete("DELETE", f"/api/v1/knowledge/{b['id']}/delete"))
    for f in fichiers:
        print("suppression du fichier :", f.get("filename"), "->", requete("DELETE", f"/api/v1/files/{f['id']}"))
print("bases restantes :", [b["name"] for b in liste(requete("GET", "/api/v1/knowledge/"))])
