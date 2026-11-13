"""Chapitre 11 : prompts, outils, fonctions et serveurs MCP (code relu dans outils/open-webui/extensions/)."""
import re
from pathlib import Path
from ui import Scenario, etapes, RACINE

CH = "11-prompts-outils-fonctions"
EXT = RACINE / "outils/open-webui/extensions"


def editeur(p, code):
    """Remplace le contenu de l'éditeur de code (CodeMirror) par `code`."""
    ed = p.locator(".cm-content").first
    ed.click(); p.keyboard.press("Control+A"); p.keyboard.press("Delete")
    p.keyboard.insert_text(code)
    p.wait_for_timeout(500)
    return ed


def prompt(s):
    p = s.page
    s.aller("/workspace/prompts")
    creer = p.get_by_role("button", name="Créer", exact=True).first
    s.cap("01-prompts", [(s.el("Prompts", debut=True), "Prompts"), (creer, "Créer")])
    creer.click()
    nom = p.get_by_placeholder("Nom du prompt"); nom.wait_for()
    nom.fill("Fiche de synthèse")
    p.get_by_placeholder("commande").fill("synthese")
    p.get_by_placeholder(re.compile("Rédigez un résumé")).fill(
        "Rédige une fiche de synthèse de {{sujet}} pour un responsable d'atelier : contexte, chiffres clés, actions à mener. "
        "Cite le document source de chaque chiffre.")
    s.cap("02-nouveau-prompt", [(nom, "Nom du prompt"), (p.get_by_placeholder("commande"), "Commande"),
                                (p.get_by_placeholder(re.compile("Rédigez un résumé")), "Contenu du prompt"),
                                (p.get_by_role("button", name="Enregistrer & Créer"), "Enregistrer & Créer")])
    p.get_by_role("button", name="Enregistrer & Créer").click(); p.wait_for_timeout(2000)
    s.sans_toasts()
    s.aller("/")
    p.locator("#chat-input").click(); p.keyboard.type("/syn"); p.wait_for_timeout(1500)
    s.cap_souple("03-appel-prompt", [(p.get_by_text("Fiche de synthèse").last, "Fiche de synthèse"),
                                     (p.locator("#chat-input"), "/syn")])
    p.keyboard.press("Escape")


def outil(s):
    p = s.page
    s.aller("/workspace/tools")
    creer = p.get_by_role("button", name="Créer", exact=True).first
    creer.click()
    p.get_by_placeholder("Nom de l'outil").wait_for()
    p.get_by_placeholder("Nom de l'outil").fill("Stocks Vélanor")
    idf = p.get_by_placeholder("ID de l'outil")
    if not idf.input_value():
        idf.fill("stocks_velanor")
    p.get_by_placeholder("Description de l'outil").fill("Stock d'une pièce chez Vélanor (fictif)")
    ed = editeur(p, (EXT / "outil_stocks.py").read_text())
    s.cap("04-nouvel-outil", [(p.get_by_placeholder("Nom de l'outil"), "Nom de l'outil"),
                              (idf, "ID de l'outil"), (p.get_by_placeholder("Description de l'outil"), "Description"),
                              (ed, "code de l'outil"), (p.get_by_role("button", name="Enregistrer & Créer"), "Enregistrer & Créer")])
    p.get_by_role("button", name="Enregistrer & Créer").click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog")
    if dlg.count() and dlg.last.is_visible():
        s.note("avertissement : " + dlg.last.inner_text().replace("\n", " | ")[:500])
        s.cap_souple("05-avertissement", [(dlg.last.get_by_role("button", name="Confirmer"), "Confirmer")])
        dlg.last.get_by_role("button", name="Confirmer").click(); p.wait_for_timeout(2000)
    s.sans_toasts()
    s.aller("/workspace/tools")
    s.cap_souple("06-liste-outils", [(p.get_by_text("Stocks Vélanor").first, "Stocks Vélanor")])


def fonction(s):
    p = s.page
    s.aller("/admin/functions")
    creer = p.get_by_role("button", name="Créer", exact=True).first
    s.cap("07-fonctions", [(s.el("Fonctions"), "Fonctions"), (creer, "Créer")])
    creer.click()
    p.get_by_placeholder("Nom de la fonction").wait_for()
    p.get_by_placeholder("Nom de la fonction").fill("Mention de source interne")
    idf = p.get_by_placeholder("ID de la fonction")
    if not idf.input_value():
        idf.fill("mention_source_interne")
    p.get_by_placeholder("Description de la fonction").fill("Réponse en français et mention en fin de réponse")
    ed = editeur(p, (EXT / "filtre_signature.py").read_text())
    s.cap("08-nouvelle-fonction", [(p.get_by_placeholder("Nom de la fonction"), "Nom de la fonction"),
                                   (p.get_by_label("Démarreur de fonction"), "modèle de départ"),
                                   (ed, "code du filtre"), (p.get_by_role("button", name="Enregistrer & Créer"), "Enregistrer & Créer")])
    p.get_by_role("button", name="Enregistrer & Créer").click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog")
    if dlg.count() and dlg.last.is_visible():
        dlg.last.get_by_role("button", name="Confirmer").click(); p.wait_for_timeout(2000)
    s.sans_toasts()
    s.aller("/admin/functions")
    ligne = p.locator("div").filter(has_text=re.compile("^\\s*Mention de source interne")).last
    s.note("liste des fonctions : " + p.locator("main").inner_text().replace("\n", " | ")[:600])
    inter = p.get_by_role("switch").first
    s.cap_souple("09-liste-fonctions", [(p.get_by_text("Mention de source interne").first, "Mention de source interne"),
                                        (inter, "interrupteur (désactivée)")])


def mcp(s):
    p = s.page
    s.reglages("admin:integrations")
    plus = p.get_by_text("Serveurs d'outils externes", exact=True).locator("xpath=following::button[1]")
    s.cap_souple("10-integrations", [(s.onglet("Intégrations", admin=True), "Intégrations"),
                                     (p.get_by_text("Serveurs d'outils externes", exact=True), "Serveurs d'outils externes"),
                                     (plus, "+")])
    plus.click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    s.note("fenêtre serveur d'outils : " + dlg.inner_text().replace("\n", " | ")[:900])
    s.note("éléments : " + str(dlg.evaluate("n => [...n.querySelectorAll('button,input,select,textarea')].map(e=>[e.tagName,(e.innerText||'').trim().slice(0,30),e.placeholder||'',e.getAttribute('aria-label')])")))
    typ = dlg.get_by_role("button", name="OpenAPI")
    typ.click(); p.wait_for_timeout(800)
    s.note("type après clic : " + dlg.inner_text().replace("\n", " | ")[:200])
    dlg.get_by_placeholder("Entrez votre nom").fill("Vélanor MCP")
    dlg.get_by_placeholder("Entrez la description").fill("Sites et jours ouvrés (serveur MCP d'essai)")
    url = dlg.get_by_placeholder(re.compile("URL"))
    url.fill("http://rag-mcp-velanor:8000/mcp")
    ver = dlg.get_by_role("button", name="Vérifier la connexion")
    s.cap("11-serveur-mcp", [(dlg.locator("button").filter(has_text=re.compile("MCP|OpenAPI")).first, "Type"),
                             (dlg.get_by_placeholder("Entrez votre nom"), "Nom"), (url, "URL"),
                             (dlg.locator("select").first, "Auth"), (ver, "Vérifier la connexion"),
                             (dlg.get_by_role("button", name="Enregistrer"), "Enregistrer")])
    ver.click(); p.wait_for_timeout(3000)
    toast = p.locator("[data-sonner-toast]").first
    s.note("vérification : " + (toast.inner_text() if toast.count() else "aucun message"))
    s.cap_souple("12-mcp-verifie", [(toast, "message")])
    dlg.get_by_role("button", name="Enregistrer").click(); p.wait_for_timeout(1500)
    s.sans_toasts()
    enr = s.bouton("Enregistrer", exact=True).filter(visible=True).last
    enr.click(); p.wait_for_timeout(1500)
    s.sans_toasts()
    s.cap_souple("13-mcp-liste", [(p.get_by_text("Vélanor MCP").first, "Vélanor MCP")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([prompt, outil, fonction, mcp], s)
    finally:
        s.fermer()
