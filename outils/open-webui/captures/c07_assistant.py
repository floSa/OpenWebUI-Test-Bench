"""Chapitre 07 : créer un assistant (modèle personnalisé) lié à une base, le partager, l'utiliser."""
import re
from ui import Scenario, etapes

CH = "07-assistant-lie-a-une-base"
NOM = "Assistant qualité Vélanor"
DESCRIPTION = "Répond aux questions sur les documents de Vélanor, en citant ses sources."
CONSIGNE = ("Tu es l'assistant qualité de Vélanor. Réponds en français, en trois phrases au plus, "
            "uniquement à partir des documents de la base. Si l'information n'y figure pas, dis-le.")
BASE = "Démo Vélanor"
QUESTION = "Quelle est la température de stockage des batteries ?"


def ligne(p, libelle):
    """Valeur cliquable d'une ligne de l'éditeur de modèle (« Connaissances », « Outils »...)."""
    return p.get_by_text(libelle, exact=True).filter(visible=True).last


def creer(s):
    p = s.page
    s.aller("/workspace/models")
    creer_ = p.get_by_role("button", name="Créer", exact=True).first
    s.cap("01-modeles", [(p.get_by_role("link", name=re.compile(r"^Modèles")).first, "Modèles"), (creer_, "Créer")])
    creer_.click(); p.wait_for_timeout(2000)
    nom = p.get_by_placeholder("Nom du modèle"); nom.fill(NOM)
    p.get_by_placeholder("Ajoutez une brève description de ce que fait ce modèle.").fill(DESCRIPTION)
    base = p.get_by_text("Chosir un modèle de base", exact=True).filter(visible=True).first
    base.click(); p.wait_for_timeout(1000)
    p.locator("button[aria-label='Sélectionner le modèle chat']").click(); p.wait_for_timeout(800)
    consigne = p.locator("textarea").filter(visible=True).nth(1)
    consigne.fill(CONSIGNE); p.wait_for_timeout(500)
    s.note("après identité : " + p.locator("main").inner_text()[:700].replace("\n", " | "))
    s.cap_souple("02-identite", [(nom, "Nom du modèle"), (p.get_by_placeholder("ID du modèle"), "ID du modèle"),
                                 (p.get_by_placeholder("Ajoutez une brève description de ce que fait ce modèle."), "Description"),
                                 (p.get_by_text("Modèle de base (à partir de)").first.locator("xpath=following::button[1]"), "Modèle de base"),
                                 (consigne, "Prompt système")])
    ligne(p, "Connaissances").click(); p.wait_for_timeout(1200)
    choix = p.get_by_text(BASE, exact=True).filter(visible=True).first
    s.cap_souple("03-choisir-base", [(p.get_by_placeholder("Search knowledge"), "Search knowledge"), (choix, BASE),
                                     (p.get_by_text("Terminé", exact=True).filter(visible=True).first, "Terminé")])
    choix.click(); p.wait_for_timeout(600)
    p.get_by_text("Terminé", exact=True).filter(visible=True).first.click(); p.wait_for_timeout(800)
    s.note("lignes : " + p.locator("main").inner_text().split("Connaissances")[-1][:500].replace("\n", " | "))
    enr = p.get_by_role("button", name=re.compile("Enregistrer & Créer"))
    enr.scroll_into_view_if_needed()
    s.cap_souple("04-pret", [(p.get_by_text("Connaissances", exact=True).filter(visible=True).last, "Connaissances"),
                             (p.get_by_text(BASE).filter(visible=True).last, BASE),
                             (p.get_by_text("Outils intégrés", exact=True).filter(visible=True).first, "Outils intégrés"),
                             (enr, "Enregistrer & Créer")])
    enr.click(); p.wait_for_timeout(2500)
    s.note("après création : " + p.url + " | " + p.locator("main").inner_text()[:400].replace("\n", " | "))
    s.sans_toasts()
    s.aller("/workspace/models")
    carte = p.get_by_text(NOM).first
    s.cap_souple("05-liste", [(carte, NOM)])


def partager(s):
    p = s.page
    s.aller("/workspace/models")
    p.get_by_text(NOM).first.click(); p.wait_for_timeout(2000)
    acces = p.get_by_role("button", name="Accès").first
    acces.click(); p.wait_for_timeout(1000)
    dlg = p.get_by_role("dialog").last
    s.note("fenêtre accès : " + dlg.inner_text()[:500].replace("\n", " | "))
    ajout = dlg.get_by_role("button", name=re.compile("Ajouter un accès")).first
    ajout.click(); p.wait_for_timeout(1000)
    d2 = p.get_by_role("dialog").last
    grp = d2.get_by_text("Équipe production").first
    grp.click(); p.wait_for_timeout(400)
    btn = d2.get_by_role("button", name="Ajouter", exact=True).first
    s.cap_souple("06-partage", [(grp, "Équipe production"), (btn, "Ajouter")])
    btn.click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog").last
    s.cap_souple("07-acces", [(dlg.get_by_text("Équipe production").first, "Équipe production")])
    s.note("après partage : " + dlg.inner_text()[:400].replace("\n", " | "))
    p.keyboard.press("Escape")


def utiliser(s):
    """Sollicite le modèle : à lancer hors banc."""
    p = s.page
    s.aller("/")
    sel = p.locator("button[aria-label^='Modèle sélectionné']").first
    sel.click(); p.wait_for_timeout(1000)
    item = p.get_by_role("button", name=re.compile(re.escape(NOM))).filter(visible=True).first
    if not item.count():
        item = p.get_by_text(NOM).filter(visible=True).first
    s.cap_souple("08-choisir", [(sel, "modèle"), (item, NOM)])
    item.click(); p.wait_for_timeout(800)
    p.locator("#chat-input").click(); p.keyboard.type(QUESTION)
    p.locator("#send-message-button").click()
    rep = s.attendre_reponse()
    s.note(f"réponse : {rep[:600]!r}")
    msg = p.locator(".chat-assistant").last
    s.cap_souple("09-reponse", [(p.locator("button[aria-label^='Modèle sélectionné']").first, NOM),
                                (msg.get_by_text(re.compile("Exploré|Recherché|Pensé")).first, "étapes"),
                                (msg.locator("button").filter(has_text=re.compile("Source")).last, "Sources")])


def utiliser_julien(s):
    """Sollicite le modèle : le compte « utilisateur » (groupe Équipe production) voit et utilise l'assistant partagé."""
    u = s.autre_session("utilisateur")
    p = u.page
    try:
        u.aller("/")
        sel = p.locator("button[aria-label^='Modèle sélectionné']").first
        sel.click(); p.wait_for_timeout(1000)
        s.note("modèles visibles pour l'utilisateur : " + " | ".join(b.inner_text().strip() for b in p.locator("button[aria-label^='Sélectionner le modèle']").all()))
        item = p.get_by_text(NOM).filter(visible=True).first
        u.cap_souple("10-utilisateur-choisit", [(item, NOM)])
        item.click(); p.wait_for_timeout(800)
        p.locator("#chat-input").click(); p.keyboard.type("Quel est le délai de livraison prévu par le contrat avec Batterix ?")
        p.locator("#send-message-button").click()
        rep = u.attendre_reponse()
        s.note(f"réponse à l'utilisateur : {rep[:600]!r}")
        msg = p.locator(".chat-assistant").last
        u.cap_souple("11-utilisateur-reponse", [(p.locator("button[aria-label^='Modèle sélectionné']").first, NOM),
                                                (msg.locator("button").filter(has_text=re.compile("Source")).last, "Sources")])
    finally:
        u.fermer()


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([creer, partager, utiliser, utiliser_julien], s)
    finally:
        s.fermer()
