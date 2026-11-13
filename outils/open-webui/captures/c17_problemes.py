"""Chapitre 17 : erreurs réellement provoquées (mot de passe faux, Docling arrêté, serveur MCP arrêté).
Docling et le serveur MCP sont arrêtés puis relancés depuis l'hôte (docling.sh, mcp.sh) autour des étapes ; jamais LLM-Service."""
import re
from ui import Scenario, identifiants, etapes

CH = "17-en-cas-de-probleme"
FICHIER = "/depot/corpus/documents/procedure-batteries.docx"


def mot_de_passe(s):
    u = s.autre_session()  # session vierge, non connectée
    p = u.page
    try:
        d = identifiants()
        u.aller("/auth")
        p.locator("input[type=email], input[name=email]").first.fill(d["open-webui.admin.email"])
        p.locator("input[type=password]").first.fill("mot-de-passe-faux")
        p.locator("form button[type=submit]").first.click(); p.wait_for_timeout(1500)
        toast = p.locator("[data-sonner-toast]").first
        s.note("connexion refusée : " + (toast.inner_text() if toast.count() else "aucun message"))
        u.cap_souple("01-mot-de-passe", [(toast, "message d'erreur"), (p.locator("input[type=password]").first, "Mot de passe")])
    finally:
        u.fermer()


def docling_arrete(s):
    """À lancer quand Docling est arrêté : l'ajout d'un fichier à une base temporaire échoue."""
    p = s.page
    s.aller("/workspace/knowledge")
    p.get_by_role("button", name="Créer", exact=True).first.click()
    p.get_by_placeholder("Nommez votre base de connaissances").fill("Essai erreurs")
    p.get_by_placeholder("Décrivez votre base de connaissances et vos objectifs").fill("Base temporaire du chapitre 17.")
    p.get_by_role("button", name="Créer une connaissance").click()
    p.get_by_placeholder("Nom de la connaissance").wait_for(); s.sans_toasts()
    p.get_by_role("button", name="Ajouter du contenu").click(); p.wait_for_timeout(800)
    with p.expect_file_chooser() as fc:
        p.get_by_role("menuitem").filter(has_text=re.compile("Téléverser des fichiers")).first.click()
    fc.value.set_files(FICHIER)
    toast = p.locator("[data-sonner-toast]").filter(has_text=re.compile("rror|chec|impossible|Docling|connect", re.I)).first
    try:
        toast.wait_for(timeout=120000)
    except Exception:
        pass
    s.note("ajout sans Docling : " + " || ".join(t.inner_text() for t in p.locator("[data-sonner-toast]").all())[:600])
    s.cap_souple("02-docling-arrete", [(toast, "message d'erreur")])
    kid = p.url.rstrip("/").split("/")[-1]
    r = p.evaluate("""async (id) => { const r = await fetch('/api/v1/knowledge/' + id + '/delete',
        {method: 'DELETE', headers: {Authorization: 'Bearer ' + localStorage.token}}); return r.status }""", kid)
    s.note(f"base temporaire supprimée : HTTP {r}")


def mcp_arrete(s):
    """À lancer quand le serveur MCP est arrêté : la liste des outils ou l'appel échoue (sollicite le modèle)."""
    p = s.page
    s.aller("/")
    plus = p.locator("button[aria-label='Plus']").filter(visible=True).last
    plus.click(); p.wait_for_timeout(800)
    p.get_by_role("menuitem").filter(has_text="Outils").filter(visible=True).first.click(); p.wait_for_timeout(1000)
    mcpb = p.get_by_text("Vélanor MCP", exact=True).filter(visible=True)
    menu = p.get_by_text("Rechercher des outils").locator("xpath=ancestor::*[3]")
    s.note("outils proposés, serveur MCP arrêté : " + p.locator("body").inner_text().split("Rechercher des outils")[-1][:200].replace("\n", " | "))
    s.cap_souple("03-mcp-menu", [(p.get_by_text("Stocks Vélanor", exact=True).first, "Stocks Vélanor"), (mcpb.first, "Vélanor MCP")])
    if mcpb.count():
        mcpb.first.click(); p.wait_for_timeout(500)
    p.keyboard.press("Escape")
    p.locator("#chat-input").click(); p.keyboard.type("Quelle est l'adresse du site de Nantes de Vélanor ?")
    p.locator("#send-message-button").click()
    rep = s.attendre_reponse(maxi=240000)
    toasts = " || ".join(t.inner_text() for t in p.locator("[data-sonner-toast]").all())
    s.note(f"MCP arrêté : réponse {rep[:500]!r} ; messages : {toasts[:400]}")
    msg = p.locator(".chat-assistant").last
    err = p.locator("[data-sonner-toast]").first if toasts else msg.get_by_text(re.compile("rror|chec|indisponible|connect|impossible", re.I)).first
    s.cap_souple("04-mcp-arrete", [(err, "message"), (msg, "réponse")])


def mcp_reprise(s):
    """Capture reprise depuis la conversation existante (sans solliciter le modèle)."""
    p = s.page
    s.aller("/")
    cid = p.evaluate("""async () => { const r = await fetch('/api/v1/chats/?page=1', {headers: {Authorization: 'Bearer ' + localStorage.token}});
        const d = await r.json(); return d.find(c => /adresse/i.test(c.title)).id }""")
    s.aller(f"/c/{cid}"); p.locator(".chat-assistant").last.wait_for(); p.wait_for_timeout(2000)
    msg = p.locator(".chat-assistant").last
    s.cap_souple("04-mcp-arrete", [(msg.get_by_text(re.compile("Failed to connect to MCP")).first, "Failed to connect to MCP server"),
                                   (msg.get_by_text(re.compile("Je ne trouve pas")).first, "réponse sans l'outil")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([mot_de_passe, docling_arrete, mcp_arrete, mcp_reprise], s)
    finally:
        s.fermer()
