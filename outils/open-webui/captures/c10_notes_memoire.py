"""Chapitre 10 : notes et mémoire."""
import re
from ui import Scenario, etapes

CH = "10-notes-et-memoire"
TITRE = "Réunion qualité du 13 novembre"
SOUVENIR = "Je travaille au service qualité de Vélanor, à Nantes ; je préfère des réponses courtes, en listes."


def menage_notes(s):
    """Supprime les notes vides créées par les explorations (titre = date du jour, sans contenu)."""
    p = s.page
    for _ in range(5):
        s.aller("/notes")
        vides = p.locator("a[href^='/notes/']").filter(has_text=re.compile(r"2026-11-13|" + re.escape(TITRE)))
        if not vides.count():
            break
        vides.first.click(); p.wait_for_timeout(1500)
        p.get_by_role("button", name="Menu des notes").click(); p.wait_for_timeout(600)
        p.get_by_role("menuitem").filter(has_text="Supprimer").first.click(); p.wait_for_timeout(800)
        d = p.get_by_role("dialog").last
        if d.count():
            d.get_by_role("button", name="Confirmer").click(); p.wait_for_timeout(1200)
        s.note("note vide supprimée")


def notes(s):
    p = s.page
    s.aller("/notes")
    creer = p.get_by_role("button", name="Créer", exact=True).first
    s.cap("01-notes", [(s.el("Notes"), "Notes"), (creer, "Créer"), (p.get_by_placeholder("Rechercher des notes"), "Rechercher des notes")])
    creer.click(); p.wait_for_timeout(2500)
    titre = p.locator("input").filter(visible=True).first
    titre.fill(TITRE)
    ed = p.locator("[contenteditable=true]").filter(visible=True).first
    ed.click()
    p.keyboard.type("Participants : Karim Benali (HSE), Julien Moreau (production).")
    p.keyboard.press("Enter")
    p.keyboard.type("Décision : inspection du local B2 avancée au lundi 16 novembre.")
    p.keyboard.press("Enter")
    p.keyboard.type("À faire : vérifier les extincteurs de classe D avant fin novembre.")
    p.wait_for_timeout(2500)
    s.cap_souple("02-nouvelle-note", [(titre, "titre"), (p.get_by_role("button", name="H1").first, "barre de mise en forme"),
                               (ed, "texte de la note"), (p.get_by_role("button", name="Menu des notes"), "Menu des notes"),
                               (p.get_by_role("button", name="Accès"), "Accès")])
    p.get_by_role("button", name="Menu des notes").click(); p.wait_for_timeout(800)
    s.note("menu des notes : " + " | ".join(i.inner_text().strip() for i in p.get_by_role("menuitem").all()))
    s.cap_souple("03-menu-note", [(p.get_by_role("menuitem").first, "première action")])
    p.keyboard.press("Escape")
    # outils d'IA de la note (boutons en bas de page)
    s.note("boutons visibles : " + " | ".join(filter(None, (b.get_attribute("aria-label") or b.inner_text().strip()
                                                             for b in p.locator("button").filter(visible=True).all()[-12:]))))
    s.aller("/notes")
    s.cap_souple("04-liste-notes", [(p.get_by_text(TITRE).first, TITRE)])


def memoire(s):
    p = s.page
    s.reglages("personalization")
    inter = p.get_by_role("dialog").last.locator("button[role=switch], [role=switch]").filter(visible=True).first
    if (inter.get_attribute("aria-checked") or inter.get_attribute("data-state")) not in ("true", "checked"):
        inter.click(); p.wait_for_timeout(500)
    actions = p.get_by_role("dialog").last.get_by_role("button", name="Actions").last
    s.cap("05-memoire", [(s.onglet("Personnalisation"), "Personnalisation"), (inter, "Mémoire"),
                         (actions, "Actions")])
    actions.click(); p.wait_for_timeout(800)
    s.note("menu Actions : " + " | ".join(i.inner_text().strip() for i in p.get_by_role("menuitem").all()))
    ajout = p.get_by_role("menuitem").filter(has_text=re.compile("Ajouter|Add", re.I)).first
    ajout.click(); p.wait_for_timeout(1000)
    dlg = p.get_by_role("dialog").last
    zone = dlg.locator("textarea").first
    zone.fill(SOUVENIR)
    s.cap_souple("06-ajouter-souvenir", [(zone, "souvenir"), (dlg.get_by_role("button", name=re.compile("Ajouter|Enregistrer")).last, "Ajouter")])
    dlg.get_by_role("button", name=re.compile("Ajouter|Enregistrer")).last.click(); p.wait_for_timeout(1500)
    s.sans_toasts()
    s.reglages("personalization")
    s.cap_souple("07-souvenirs", [(p.get_by_text(re.compile("Mémoires enregistrées")).first, "Mémoires enregistrées"),
                                  (p.get_by_text("Je travaille au service qualité").first, "souvenir enregistré")])
    enr = s.bouton("Enregistrer", exact=True).filter(visible=True).last
    enr.click(); p.wait_for_timeout(1000)


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([menage_notes, notes, memoire], s)
    finally:
        s.fermer()
