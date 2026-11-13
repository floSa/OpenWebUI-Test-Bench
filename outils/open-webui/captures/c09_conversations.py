"""Chapitre 09 : converser au quotidien (menu d'une conversation, dossiers, recherche, partage, export, archive,
comparaison de deux modèles en écran partagé)."""
import re
from ui import Scenario, etapes

CH = "09-converser-au-quotidien"


def ouvrir_barre(p):
    b = p.locator("button[aria-label='Ouvrir la barre latérale']").filter(visible=True)
    if b.count():
        b.first.click(); p.wait_for_timeout(800)


def premier_item(p):
    """Première conversation de la barre latérale."""
    return p.locator("a[href^='/c/']").filter(has_text=re.compile(r"\S")).filter(visible=True).first


def menu_conv(p):
    """Bouton « Menu des conversations » de la conversation survolée."""
    return p.locator("button[aria-label='Menu des conversations']").filter(visible=True).first


def menus(p):
    return " | ".join(i.inner_text().strip() for i in p.get_by_role("menuitem").all())


def explorer(s):
    """Repérage : menu « … » d'une conversation (barre latérale) et boutons de l'en-tête d'une conversation ouverte."""
    p = s.page
    s.aller("/")
    ouvrir_barre(p)
    item = premier_item(p)
    item.hover(); p.wait_for_timeout(600)
    menu_conv(p).click(); p.wait_for_timeout(800)
    s.note("menu de la conversation : " + menus(p))
    p.keyboard.press("Escape")
    item.click(); p.wait_for_timeout(2500)
    s.note("en-tête : " + " | ".join(filter(None, ((b.get_attribute("aria-label") or b.inner_text().strip()[:30])
                                                   for b in p.locator("nav button, header button").filter(visible=True).all()))))
    for nom in ("Menu de la conversation", "Plus", "Menu"):
        b = p.locator(f"button[aria-label='{nom}']").filter(visible=True)
        if b.count():
            b.last.click(); p.wait_for_timeout(800)
            s.note(f"menu « {nom} » de l'en-tête : " + menus(p))
            p.keyboard.press("Escape"); p.wait_for_timeout(300)
    p.get_by_role("button", name="Recherche").first.click(); p.wait_for_timeout(1000)
    s.note("recherche : " + p.get_by_role("dialog").last.inner_text()[:400].replace("\n", " | "))
    p.keyboard.press("Escape")
    p.locator("button[aria-label='Nouveau dossier']").first.click(); p.wait_for_timeout(800)
    s.note("nouveau dossier : " + p.locator("body").inner_text()[:0] + menus(p) + " / " +
           " | ".join(i.get_attribute("placeholder") or "" for i in p.locator("input").filter(visible=True).all()))
    p.keyboard.press("Escape")


def survoler(s, titre=None):
    p = s.page
    ouvrir_barre(p)
    item = p.locator("a[href^='/c/']").filter(has_text=titre).filter(visible=True).last if titre else premier_item(p)
    item.hover(); p.wait_for_timeout(600)
    return item


def menu(s):
    p = s.page
    s.aller("/")
    item = survoler(s)
    b = menu_conv(p)
    b.click(); p.wait_for_timeout(800)
    it = lambda n: p.get_by_role("menuitem").filter(has_text=re.compile("^\\s*" + n)).first
    s.cap_souple("01-menu", [(item, "conversation"), (b, "Menu des conversations"), (it("Partager"), "Partager"),
                             (it("Télécharger"), "Télécharger"), (it("Renommer"), "Renommer"), (it("Épingler"), "Épingler"),
                             (it("Archiver"), "Archiver"), (it("Supprimer"), "Supprimer")])
    p.keyboard.press("Escape")


def renommer_epingler(s):
    p = s.page
    s.aller("/")
    survoler(s, "chiffre d")
    menu_conv(p).click(); p.wait_for_timeout(600)
    p.get_by_role("menuitem").filter(has_text="Renommer").first.click(); p.wait_for_timeout(600)
    champ = p.locator("input").filter(visible=True).last
    champ.fill("Chiffre d'affaires 2025"); p.wait_for_timeout(300)
    s.cap_souple("02-renommer", [(champ, "nouveau titre")])
    champ.press("Enter"); p.wait_for_timeout(1200)
    survoler(s, "Chiffre d'affaires 2025")
    menu_conv(p).click(); p.wait_for_timeout(600)
    p.get_by_role("menuitem").filter(has_text="Épingler").first.click(); p.wait_for_timeout(1200)
    s.note("barre après épingle : " + p.locator("nav, aside").first.inner_text()[:500].replace("\n", " | "))
    epingle = p.get_by_text(re.compile("^Épinglé")).filter(visible=True).first
    s.cap_souple("03-epinglee", [(epingle, "Épinglé"), (p.locator("a[href^='/c/']").filter(has_text="Chiffre d'affaires 2025").filter(visible=True).first, "conversation épinglée")])


def dossier(s):
    p = s.page
    s.aller("/")
    ouvrir_barre(p)
    nb = p.locator("button[aria-label='Nouveau dossier']").filter(visible=True).first
    nb.click(); p.wait_for_timeout(800)
    champ = p.get_by_placeholder("Entrez le nom du dossier").filter(visible=True).first
    champ.fill("Questions rapport annuel")
    s.cap_souple("04-nouveau-dossier", [(nb, "Nouveau dossier"), (champ, "Entrez le nom du dossier")])
    champ.press("Enter"); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog")
    if dlg.count():
        s.note("fenêtre dossier : " + dlg.last.inner_text()[:500].replace("\n", " | "))
        b = dlg.last.get_by_role("button", name=re.compile("Créer|Enregistrer")).last
        s.cap_souple("04b-dossier-fenetre", [(b, "Créer")])
        b.click(); p.wait_for_timeout(1500)
    s.aller("/"); ouvrir_barre(p)
    doss = p.get_by_text("Questions rapport annuel").filter(visible=True).first
    conv = p.locator("a[href^='/c/']").filter(has_text="chiffre d").filter(visible=True).first
    try:
        conv.drag_to(doss); p.wait_for_timeout(1500)
    except Exception as e:
        s.note(f"glisser-déposer : {e}")
    s.note("barre après dossier : " + p.locator("nav, aside").first.inner_text()[:600].replace("\n", " | "))
    doss.click(); p.wait_for_timeout(1000)
    s.cap_souple("05-dossier", [(doss, "Questions rapport annuel"),
                                (p.locator("a[href^='/c/']").filter(has_text="chiffre d").filter(visible=True).first, "conversation rangée")])


def ranger(s):
    """Glisse la conversation « Quel est le chiffre... » dans le dossier (souris pas à pas : glisser-déposer HTML5)."""
    p = s.page
    s.aller("/"); ouvrir_barre(p)
    doss = p.get_by_text("Questions rapport annuel", exact=True).first
    if not doss.is_visible():
        p.get_by_role("button", name="Dossiers", exact=True).first.click(); p.wait_for_timeout(800)
    s.note(f"dossier visible : {doss.is_visible()} ; barre : " + p.locator("#sidebar, nav").first.inner_text()[:400].replace("\n", " | "))
    conv = p.locator("a[href^='/c/']").filter(has_text="Quel est le chiffre").filter(visible=True).first
    a, b = conv.bounding_box(), doss.bounding_box()
    p.mouse.move(a["x"] + 30, a["y"] + a["height"] / 2); p.mouse.down()
    for i in range(1, 16):
        p.mouse.move(a["x"] + 30, a["y"] + (b["y"] - a["y"]) * i / 15 + a["height"] / 2); p.wait_for_timeout(40)
    p.mouse.up(); p.wait_for_timeout(1500)
    if not p.locator("a[href^='/c/']").filter(has_text="Quel est le chiffre").filter(visible=True).count():
        doss.click(); p.wait_for_timeout(1000)
    s.note("barre après rangement : " + p.locator("#sidebar, nav").first.inner_text()[:400].replace("\n", " | "))
    s.cap_souple("05-dossier", [(doss, "Questions rapport annuel"),
                                (p.locator("a[href^='/c/']").filter(has_text="Quel est le chiffre").filter(visible=True).first, "conversation rangée")])


def partager(s):
    p = s.page
    s.aller("/")
    survoler(s, "Chiffre d'affaires 2025")
    menu_conv(p).click(); p.wait_for_timeout(600)
    p.get_by_role("menuitem").filter(has_text="Partager").first.click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog").last
    s.note("fenêtre partage : " + dlg.inner_text()[:600].replace("\n", " | "))
    s.note("boutons partage : " + " | ".join(b.inner_text().strip() or (b.get_attribute("aria-label") or "") for b in dlg.locator("button").all()))
    s.cap_souple("06-partager", [(dlg.get_by_role("button", name=re.compile("Copier le lien|Copy Link|Copier")).last, "Copier le lien")])
    p.keyboard.press("Escape")


def telecharger(s):
    p = s.page
    s.aller("/")
    survoler(s, "Chiffre d'affaires 2025")
    menu_conv(p).click(); p.wait_for_timeout(600)
    t = p.get_by_role("menuitem").filter(has_text="Télécharger").first
    t.hover(); p.wait_for_timeout(800)
    t.click(); p.wait_for_timeout(800)
    s.note("sous-menu Télécharger : " + menus(p))
    sm = p.get_by_role("menuitem").filter(has_text=re.compile("json", re.I)).first.locator("xpath=..")
    s.cap_souple("07-telecharger", [(t, "Télécharger"), (sm, "formats")])
    sous = p.get_by_role("menuitem").filter(has_text=re.compile("PDF")).first
    if sous.count():
        with p.expect_download(timeout=60000) as dl:
            sous.click()
        d = dl.value
        chemin = "/depot/outils/resultats/open-webui/captures/09-converser-au-quotidien/" + d.suggested_filename
        d.save_as(chemin)
        s.note(f"téléchargé : {d.suggested_filename}")


def rechercher(s):
    p = s.page
    s.aller("/")
    p.get_by_role("button", name="Recherche").first.click(); p.wait_for_timeout(800)
    dlg = p.get_by_role("dialog").last
    champ = dlg.locator("input").first
    champ.fill("chiffre"); p.wait_for_timeout(1500)
    s.note("recherche « chiffre » : " + dlg.inner_text()[:500].replace("\n", " | "))
    s.cap_souple("08-rechercher", [(champ, "recherche"), (dlg.get_by_text(re.compile("Chiffre d'affaires 2025")).first, "résultat")])
    p.keyboard.press("Escape")


QUESTION_COMP = "En une phrase : pourquoi stocker les batteries entre 10 et 25 °C ?"


def comparer(s):
    """Sollicite le modèle (deux fois) : écran partagé, `chat` à gauche, `gemma-4-e4b` à droite, même question."""
    p = s.page
    s.aller("/")
    p.locator("button[aria-label='Split screen']").first.click(); p.wait_for_timeout(1500)
    sels = p.locator("button[aria-label^='Modèle sélectionné']").filter(visible=True)
    s.note(f"sélecteurs visibles : {sels.count()}")
    sels.last.click(); p.wait_for_timeout(800)
    p.locator("button[aria-label='Sélectionner le modèle gemma-4-e4b']").filter(visible=True).first.click(); p.wait_for_timeout(800)
    zones = p.locator("#chat-input, [contenteditable=true]").filter(visible=True)
    s.note(f"zones de saisie : {zones.count()}")
    s.cap_souple("10-ecran-partage", [(p.locator("button[aria-label='Split screen']").first, "Split screen"),
                                      (sels.first, "chat"), (sels.last, "gemma-4-e4b")])
    for i in range(zones.count()):
        z = p.locator("#chat-input, [contenteditable=true]").filter(visible=True).nth(i)
        z.click(); p.keyboard.type(QUESTION_COMP); p.keyboard.press("Enter"); p.wait_for_timeout(1500)
    import time
    debut, dernier = time.time(), ""
    while time.time() - debut < 300:
        txt = " ".join(m.inner_text() for m in p.locator(".chat-assistant").all())
        if txt and txt == dernier and not p.locator("button[aria-label='Stop']").count():
            break
        dernier = txt; p.wait_for_timeout(4000)
    msgs = p.locator(".chat-assistant")
    s.note("réponses : " + " ||| ".join(m.inner_text()[:300].replace("\n", " ") for m in msgs.all()))
    s.cap_souple("11-comparaison", [(msgs.first, "réponse de chat"), (msgs.last, "réponse de gemma-4-e4b")])


def archiver(s):
    """Archive une conversation de la comparaison (étape comparer)."""
    p = s.page
    s.aller("/")
    if not p.evaluate("""async () => { const r = await fetch('/api/v1/chats/archived', {headers: {Authorization: 'Bearer ' + localStorage.token}});
            return (await r.json()).some(c => c.title === 'Stock Trends') }"""):
        item = survoler(s, "Stock Trends")
        item.locator("xpath=../../..").locator("button[aria-label='Menu des conversations']").first.click(); p.wait_for_timeout(600)
        p.get_by_role("menuitem").filter(has_text="Archiver").first.click(); p.wait_for_timeout(1500)
        s.sans_toasts()
    s.reglages("general")
    s.onglet("Conversations archivées").click(); p.wait_for_timeout(1500)
    p.get_by_text("Stock Trends").last.wait_for(timeout=15000)
    dlg = p.get_by_role("dialog").filter(has_text="Stock Trends").last
    s.note("archives : " + dlg.inner_text()[-600:].replace("\n", " | "))
    s.cap_souple("09-archives", [(s.onglet("Conversations archivées"), "Conversations archivées"),
                                 (dlg.get_by_text("Stock Trends").first, "conversation archivée")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([explorer, menu, renommer_epingler, dossier, ranger, partager, telecharger, rechercher, comparer, archiver], s)
    finally:
        s.fermer()
