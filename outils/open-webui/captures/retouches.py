"""Reprise de captures dont l'annotation était fautive (revue visuelle du 13 novembre), sans refaire tout un chapitre.
Chaque étape écrit l'image au même nom que l'originale, dans le dossier du chapitre concerné."""
import re
from ui import Scenario, identifiants, etapes


def general_15(s):
    """15/01 : la pastille « Vérifier les mises à jour » sortait du cadre ; seuls les éléments visibles ensemble."""
    s.chapitre = "15-administrer"
    p = s.page
    s.reglages("admin:general")
    canaux = s.champ("Canaux")
    canaux.evaluate("e => e.scrollIntoView({block: 'center'})"); p.wait_for_timeout(600)
    s.cap_souple("01-general", [(s.onglet("Général", admin=True), "Général"), (canaux, "Canaux"),
                                (s.champ("Notes"), "Notes"), (s.champ("Automatisations"), "Automatisations")])
    p.keyboard.press("Escape")


def notes_10(s):
    """10/01 : le lien « Notes » de la barre latérale repliée n'était pas visible ; on désigne le titre de la page."""
    s.chapitre = "10-notes-et-memoire"
    p = s.page
    s.aller("/notes")
    titre = p.locator("main").get_by_text("Notes", exact=True).first
    s.cap("01-notes", [(titre, "Notes"), (p.get_by_role("button", name="Créer", exact=True).first, "Créer"),
                       (p.get_by_placeholder("Rechercher des notes"), "Rechercher des notes")])


def comptes_14(s):
    """14/03 : pastilles 1 et 2 superposées ; la pastille 1 désigne maintenant le nom du compte."""
    s.chapitre = "14-comptes-groupes-permissions"
    p = s.page
    d = identifiants()
    s.aller("/admin/users/overview")
    ligne = p.locator("tr").filter(has_text=d["open-webui.utilisateur.email"]).first
    ligne.wait_for()
    s.cap_souple("03-liste-comptes", [(ligne.get_by_text(d["open-webui.utilisateur.nom"]).first, "nouveau compte"),
                                      (ligne.locator("td").nth(1), "rôle"),
                                      (ligne.get_by_role("button", name="Modifier l'utilisateur"), "Modifier l'utilisateur")])


def base_vide_05(s):
    """05/03 : le message de création cachait « Accès ». Base temporaire du même nom, supprimée ensuite."""
    s.chapitre = "05-bases-de-connaissances"
    p = s.page
    s.aller("/workspace/knowledge")
    p.get_by_role("button", name="Créer", exact=True).first.click()
    p.get_by_placeholder("Nommez votre base de connaissances").fill("Démo Vélanor")
    p.get_by_placeholder("Décrivez votre base de connaissances et vos objectifs").fill(
        "Documents fictifs de l'entreprise Vélanor : rapport annuel, procédures, stocks, stratégie, audit, SAV.")
    p.get_by_role("button", name="Créer une connaissance").click()
    p.get_by_placeholder("Nom de la connaissance").wait_for()
    s.sans_toasts(); p.wait_for_timeout(800)
    s.cap("03-base-vide", [(p.get_by_placeholder("Nom de la connaissance"), "nom de la base"),
                           (p.get_by_role("button", name="Ajouter du contenu"), "Ajouter du contenu"),
                           (p.get_by_role("button", name="Accès"), "Accès")])
    kid = p.url.rstrip("/").split("/")[-1]
    r = p.evaluate("""async (id) => { const r = await fetch('/api/v1/knowledge/' + id + '/delete',
        {method: 'DELETE', headers: {Authorization: 'Bearer ' + localStorage.token}}); return r.status }""", kid)
    s.note(f"base temporaire {kid} supprimée : HTTP {r}")


if __name__ == "__main__":
    s = Scenario("_retouches")
    try:
        etapes([general_15, notes_10, comptes_14, base_vide_05], s)
    finally:
        s.fermer()
