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


GROUPE = "Équipe production"


def ouvrir_chat_admin(s, nom="chat"):
    p = s.page
    s.reglages("admin:models")
    i = p.evaluate("""(nom) => [...document.querySelectorAll('button[aria-label=Modifier]')].filter(b => b.offsetParent)
        .findIndex(b => b.parentElement.parentElement.innerText.trim().split(/\\s/)[0] === nom)""", nom)
    p.locator("button[aria-label='Modifier']").filter(visible=True).nth(i).click()
    p.wait_for_timeout(2000)
    s.note("fiche ouverte : " + p.url)


def partage_chat_14(s):
    """14/09 et 14/10 : partage montré sur `chat` (les premières captures montraient `bge-m3`). Aucun accès ajouté."""
    s.chapitre = "14-comptes-groupes-permissions"
    p = s.page
    ouvrir_chat_admin(s)
    p.locator("button").filter(has_text=re.compile(r"^\s*Accès\s*$")).filter(visible=True).last.click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    if GROUPE in dlg.inner_text():  # accès déjà donné : le retirer pour refaire le parcours complet (enregistré aussitôt)
        ligne = dlg.locator("div").filter(has_text=GROUPE).filter(has=p.locator("button")).last
        ligne.locator("button").last.click(); p.wait_for_timeout(1500)
        s.note("accès du groupe retiré avant reprise : " + dlg.inner_text()[:200].replace("\n", " | "))
    dlg.get_by_role("button", name=re.compile("Ajouter un accès")).first.click(); p.wait_for_timeout(1200)
    choix = p.get_by_role("dialog").last
    case = choix.locator("div, label, li").filter(has_text=GROUPE).locator("input[type=checkbox], button[role=checkbox]").first
    if case.count():
        case.click(); p.wait_for_timeout(400)
    s.cap_souple("09-partage-modele-a", [(choix.get_by_text(GROUPE).first, GROUPE),
                                         (choix.locator("input[type=checkbox], button[role=checkbox]").first, "case à cocher"),
                                         (choix.get_by_role("button", name="Ajouter"), "Ajouter")])
    choix.get_by_role("button", name="Ajouter").click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog").filter(has_text="Contrôle d'accès").last
    if not dlg.count():
        p.locator("button").filter(has_text=re.compile(r"^\s*Accès\s*$")).filter(visible=True).last.click(); p.wait_for_timeout(1200)
        dlg = p.get_by_role("dialog").last
    s.cap_souple("09-partage-modele-b", [(dlg.get_by_role("button", name=re.compile("^Visibilité")).first, "Visibilité"),
                                         (dlg.get_by_text(GROUPE).first, GROUPE)])
    s.note("contrôle d'accès de chat : " + dlg.inner_text()[:300].replace("\n", " | "))
    s.reglages("admin:models")
    s.cap_souple("10-modele-partage", [(p.locator("button").filter(has_text=re.compile(r"^\s*chat\s+Partagé")).filter(visible=True).first, "chat Partagé"),
                                       (p.locator("button").filter(has_text=re.compile(r"^\s*gemma-4-e4b\s+Privé")).filter(visible=True).first, "gemma-4-e4b Privé")])


def admin_15(s):
    s.chapitre = "15-administrer"
    p = s.page
    s.reglages("admin:analytics")
    d = p.get_by_role("dialog").last
    s.cap_souple("05-analytique", [(s.onglet("Analytique", admin=True), "Analytique"),
                                   (d.get_by_text("Tokens", exact=True).first, "Tokens"), (d.get_by_text("Messages", exact=True).first, "Messages")])
    s.reglages("admin:interface")
    s.cap_souple("10-interface-taches", [(s.onglet("Interface utilisateur", admin=True), "Interface utilisateur"),
                                         (p.get_by_text("Modèle de tâche local", exact=True).locator("xpath=following::select[1]"), "Modèle de tâche local"),
                                         (p.get_by_text("Modèle de tâche externe", exact=True).locator("xpath=following::select[1]"), "Modèle de tâche externe"),
                                         (p.get_by_role("button", name=re.compile("Configurer")).filter(visible=True).first, "Configurer"),
                                         (s.champ("Génération du Titre"), "Génération du Titre")])


def pause_13(s):
    s.chapitre = "13-automatisations-canaux-calendrier"
    p = s.page
    s.aller("/automations")
    p.get_by_role("link", name=re.compile("Point qualité du lundi")).first.click(); p.wait_for_timeout(2000)
    inter = p.locator("main [role=switch], main button[aria-label='En pause'], main button[aria-label='Actif']").first
    s.note("interrupteur : " + str(inter.get_attribute("aria-label")) + " / " + str(inter.get_attribute("aria-checked")))
    s.cap_souple("13-pause", [(inter, "interrupteur"), (p.get_by_text("En pause", exact=True).first, "statut")])


def outils_11(s):
    """11/15 et 11/17 : question saisie (non envoyée) ; détail des deux appels d'outils dans la conversation existante."""
    s.chapitre = "11-prompts-outils-fonctions"
    p = s.page
    s.aller("/")
    plus = p.locator("button[aria-label='Plus']").filter(visible=True).last
    p.locator("#chat-input").click()
    p.keyboard.type("Combien de moteurs centraux reste-t-il en stock, et combien de jours ouvrés y a-t-il entre le 16 et le 27 novembre 2026 ?")
    s.cap_souple("15-outils-actifs", [(p.locator("#chat-input"), "question"), (plus, "+")])
    p.keyboard.press("Control+A"); p.keyboard.press("Delete")
    cid = p.evaluate("""async () => { const r = await fetch('/api/v1/chats/?page=1', {headers: {Authorization: 'Bearer ' + localStorage.token}});
        const d = await r.json(); return d.find(c => c.id.startsWith('d09059c9')).id }""")  # essai d'outils réussi (essai-outils-filtre-2026-11-13.json)
    s.aller(f"/c/{cid}"); p.locator(".chat-assistant").last.wait_for(); p.wait_for_timeout(1500)
    msg = p.locator(".chat-assistant").last
    s.note("conversation ouverte : " + p.url + " | " + msg.inner_text()[:200].replace("\n", " | "))
    msg.get_by_text("Exploré", exact=False).first.click(); p.wait_for_timeout(1200)
    s.note("après clic : " + msg.inner_text()[:400].replace("\n", " | "))
    s.cap_souple("17-detail-appel", [(msg.get_by_text(re.compile("Voir le résultat de stock_piece")).first, "stock_piece"),
                                     (msg.get_by_text(re.compile("Voir le résultat de velanor-mcp_jours_ouvres")).first, "jours_ouvres")])


def consigne_16(s):
    s.chapitre = "16-cas-pratiques"
    p = s.page
    cid = p.evaluate("""async () => { const r = await fetch('/api/v1/chats/?page=1', {headers: {Authorization: 'Bearer ' + localStorage.token}});
        const d = await r.json(); return d.find(c => /Sécurité batterie/.test(c.title)).id }""") if False else None
    s.aller("/")
    cid = p.evaluate("""async () => { const r = await fetch('/api/v1/chats/?page=1', {headers: {Authorization: 'Bearer ' + localStorage.token}});
        const d = await r.json(); return d.find(c => /Sécurité batterie/.test(c.title)).id }""")
    s.aller(f"/c/{cid}"); p.locator(".chat-assistant").last.wait_for(); p.wait_for_timeout(1500)
    msg = p.locator(".chat-assistant").last
    src = msg.locator("button").filter(has_text=re.compile("Source")).last
    src.click(); p.wait_for_timeout(800)
    s.cap_souple("01-consigne", [(msg.get_by_text(re.compile("^\\s*Exploré")).first, "Exploré"),
                                 (msg.locator("ol, ul").first, "réponse"), (src, "1 Source")])


def retirer_bge(s):
    """Retire l'accès du groupe au modèle technique `bge-m3`, partagé par erreur (sans capture)."""
    p = s.page
    ouvrir_chat_admin(s, "bge-m3")
    p.locator("button").filter(has_text=re.compile(r"^\s*Accès\s*$")).filter(visible=True).last.click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    if GROUPE in dlg.inner_text():
        dlg.locator("div").filter(has_text=GROUPE).filter(has=p.locator("button")).last.locator("button").last.click(); p.wait_for_timeout(1500)
    s.note("accès de bge-m3 : " + dlg.inner_text()[:200].replace("\n", " | "))


def liste_modeles_14(s):
    """14/10 reprise après le retrait de l'accès de `bge-m3` : seul `chat` est partagé."""
    s.chapitre = "14-comptes-groupes-permissions"
    p = s.page
    s.reglages("admin:models")
    s.cap_souple("10-modele-partage", [(p.locator("button").filter(has_text=re.compile(r"^\s*chat\s+Partagé")).filter(visible=True).first, "chat Partagé"),
                                       (p.locator("button").filter(has_text=re.compile(r"^\s*gemma-4-e4b\s+Privé")).filter(visible=True).first, "gemma-4-e4b Privé")])


if __name__ == "__main__":
    s = Scenario("_retouches")
    try:
        etapes([general_15, notes_10, comptes_14, base_vide_05, partage_chat_14, admin_15, pause_13, outils_11, consigne_16, retirer_bge, liste_modeles_14], s)
    finally:
        s.fermer()
