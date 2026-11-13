"""Chapitre 13 : automatisations, canaux et calendrier."""
import re
from ui import Scenario, etapes

CH = "13-automatisations-canaux-calendrier"
TITRE = "Point qualité du lundi"


def automatisation(s):
    p = s.page
    s.aller("/automations")
    creer = p.get_by_role("button", name="Créer", exact=True).first
    s.cap("01-automatisations", [(creer, "Créer"), (p.get_by_placeholder("Rechercher des automatisations"), "Rechercher des automatisations")])
    creer.click(); p.wait_for_timeout(1200)
    p.get_by_placeholder("Titre de l'automatisation").fill(TITRE)
    p.get_by_placeholder("Entrez le prompt ici.").fill(
        "Rappelle en cinq lignes les contrôles de sécurité des batteries à faire cette semaine dans le local B2 "
        "(inspection, extincteurs, formation), en français.")
    freq = p.get_by_role("button", name="Daily")
    freq.click(); p.wait_for_timeout(800)
    s.note("fréquences : " + " | ".join(i.inner_text().strip() for i in p.get_by_role("menuitem").all() + p.get_by_role("option").all()))
    s.cap_souple("02-frequence", [(freq, "Daily"), (p.get_by_role("menuitem").first, "première fréquence")])
    hebdo = p.get_by_role("menuitem").filter(has_text=re.compile("Weekly|Hebdo", re.I))
    if hebdo.count():
        hebdo.first.click()
    else:
        p.keyboard.press("Escape")
    p.wait_for_timeout(800)
    s.note("après fréquence : " + p.get_by_role("dialog").last.inner_text().replace("\n", " | ")[:400])
    mod = p.get_by_role("button", name=re.compile("Sélectionnez un mod"))
    mod.click(); p.wait_for_timeout(800)
    p.get_by_text("chat", exact=True).last.click(); p.wait_for_timeout(600)
    dest = p.get_by_role("button", name=re.compile("Nouvelle conversat"))
    dlg = p.get_by_role("dialog").last
    s.cap_souple("03-nouvelle-automatisation", [(p.get_by_placeholder("Titre de l'automatisation"), "Titre"),
                                                (p.get_by_placeholder("Entrez le prompt ici."), "Instructions"),
                                                (dlg.locator("button").filter(has_text=re.compile("Weekly|Daily|Hebdo|Quotid|Mon|Lun", re.I)).first, "fréquence"),
                                                (dlg.locator("button").filter(has_text=re.compile("^\\s*chat")).first, "modèle"),
                                                (dest, "destination"),
                                                (dlg.get_by_role("button", name="Créer", exact=True), "Créer")])
    dlg.get_by_role("button", name="Créer", exact=True).click(); p.wait_for_timeout(2000)
    s.sans_toasts()
    s.note("après création : " + p.url + " | " + p.locator("main").inner_text().replace("\n", " | ")[:600])
    s.aller("/automations")
    ligne = p.get_by_text(TITRE).first
    s.cap_souple("04-liste", [(ligne, TITRE), (p.get_by_role("switch").first, "interrupteur")])


def canaux(s):
    p = s.page
    s.reglages("admin:general")
    inter = s.champ("Canaux")
    if (inter.get_attribute("aria-checked") or inter.get_attribute("data-state")) not in ("true", "checked"):
        inter.click(); p.wait_for_timeout(400)
    s.cap("05-activer-canaux", [(s.champ("Canaux"), "Canaux"), (s.bouton("Enregistrer", exact=True), "Enregistrer")])
    s.bouton("Enregistrer", exact=True).click(); p.wait_for_timeout(1500)
    s.aller("/")
    p.get_by_role("button", name="Ouvrir la barre latérale").first.click(); p.wait_for_timeout(1000)
    s.note("barre latérale : " + p.locator("nav, aside").first.inner_text().replace("\n", " | ")[:400])
    plus = p.get_by_role("button", name=re.compile("Créer un canal|Nouveau canal|Add Channel", re.I)).first
    s.cap_souple("06-barre-canaux", [(p.get_by_text("Canaux", exact=True).first, "Canaux"), (plus, "Créer un canal")])
    plus.click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    s.note("fenêtre canal : " + dlg.inner_text().replace("\n", " | ")[:500])
    nom = dlg.locator("input").first
    nom.fill("atelier-nantes")
    s.cap_souple("07-nouveau-canal", [(nom, "nom du canal"), (dlg.get_by_role("button", name=re.compile("Créer|Enregistrer")).last, "Créer")])
    dlg.get_by_role("button", name=re.compile("Créer|Enregistrer")).last.click(); p.wait_for_timeout(2000)
    s.sans_toasts()
    saisie = p.locator("#chat-input, [contenteditable=true]").last
    saisie.click(); p.keyboard.type("Rappel : inspection du local B2 lundi matin.")
    p.keyboard.press("Enter"); p.wait_for_timeout(2000)
    s.cap_souple("08-canal", [(p.get_by_text("atelier-nantes").first, "atelier-nantes"),
                              (p.get_by_text("Rappel : inspection du local B2").last, "message publié"), (saisie, "zone de saisie")])


def calendrier(s):
    p = s.page
    s.aller("/calendar")
    s.cap_souple("09-calendrier", [(p.get_by_role("button", name="Aujourd'hui"), "Aujourd'hui"),
                                   (p.get_by_role("button", name="Créer", exact=True).first, "Créer"),
                                   (p.get_by_text("Scheduled Tasks").first, "Scheduled Tasks")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([automatisation, canaux, calendrier], s)
    finally:
        s.fermer()
