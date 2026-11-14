"""Chapitre 15 : administrer l'instance (réglages généraux, clés d'API, analytique, évaluations, base de données)."""
import re
from ui import Scenario, identifiants, etapes, CLE_RE
CLE_SANS = lambda x: CLE_RE.sub("[clé masquée]", x).replace("\n", " | ")

CH = "15-administrer"


def general(s):
    p = s.page
    s.reglages("admin:general")
    s.cap_souple("01-general", [(s.onglet("Général", admin=True), "Général"),
                                (p.get_by_text("Vérifier les mises à jour disponibles").first, "Vérifier les mises à jour disponibles"),
                                (s.champ("Canaux"), "Canaux"), (s.champ("Notes"), "Notes"),
                                (s.champ("Automatisations"), "Automatisations")])
    # bas de l'onglet : URL de l'instance, bannières
    p.mouse.move(800, 500); p.mouse.wheel(0, 3000); p.wait_for_timeout(800)
    s.cap_souple("02-general-bas", [(p.get_by_placeholder(re.compile("localhost:3000")).first, "URL de WebUI"),
                                    (p.get_by_role("button", name=re.compile("Ajouter une bannière")).first, "Ajouter une bannière"),
                                    (s.bouton("Enregistrer", exact=True), "Enregistrer")])


def cle_api(s):
    """Autoriser les clés d'API (Authentification), puis en créer une (Compte)."""
    p = s.page
    s.reglages("admin:authentication")
    inter = s.champ("Clés API")
    etat = inter.get_attribute("aria-checked") or inter.get_attribute("data-state")
    if etat not in ("true", "checked"):
        inter.click(); p.wait_for_timeout(500)
    s.cap("03-autoriser-cles", [(s.champ("Clés API"), "Clés API"), (s.bouton("Enregistrer", exact=True), "Enregistrer")])
    s.bouton("Enregistrer", exact=True).click(); p.wait_for_timeout(1500)
    s.reglages("account")
    p.mouse.move(800, 500); p.mouse.wheel(0, 3000); p.wait_for_timeout(800)
    s.note("compte : " + p.get_by_role("dialog").last.inner_text().replace("\n", " | ")[-800:])
    afficher = p.get_by_text("Secrets", exact=True).filter(visible=True).first.locator("xpath=following::button[1]")
    s.cap("04-compte-cles", [(s.onglet("Compte"), "Compte"), (p.get_by_text("Clés API", exact=True).filter(visible=True).first, "Clés API"),
                             (afficher, "Afficher")])
    afficher.click(); p.wait_for_timeout(1200)
    zone = p.get_by_role("dialog").last
    s.note("après Afficher : " + zone.inner_text().replace("\n", " | ")[-500:])
    creer = zone.get_by_role("button", name=re.compile("Créer|Générer|Create|Rotate|Régénérer", re.I)).filter(visible=True)
    s.note("boutons de clé : " + " | ".join(b.inner_text().strip() for b in creer.all()))
    if creer.count():
        creer.last.click(); p.wait_for_timeout(2000)
    p.mouse.move(800, 600); p.mouse.wheel(0, 3000); p.wait_for_timeout(800)
    s.sans_toasts()
    champs = zone.locator("input").filter(visible=True)
    s.cap_souple("04b-cle-creee", [(champs.nth(champs.count() - 2), "Jeton JWT (masqué)"),
                                   (champs.last, "Clé API (masquée)"),
                                   (champs.last.locator("xpath=following::button[2]"), "copier")])
    s.note("après création : " + CLE_SANS(zone.inner_text())[-400:])


def analytique(s):
    p = s.page
    s.reglages("admin:analytics")
    s.cap_souple("05-analytique", [(s.onglet("Analytique", admin=True), "Analytique"),
                                   (p.get_by_text("Tokens").first, "Tokens"), (p.get_by_text("Messages").first, "Messages")])
    s.reglages("usage")
    s.cap_souple("06-consommation", [(s.onglet("Consommation de tokens"), "Consommation de tokens")])


def evaluations(s):
    p = s.page
    s.aller("/admin/evaluations/leaderboard")
    s.cap_souple("07-classement", [(s.el("Évaluations"), "Évaluations"), (s.el("Classement", debut=True), "Classement"),
                                   (s.el("Avis", debut=True), "Avis")])
    s.reglages("admin:evaluations")
    s.cap_souple("08-arene", [(s.onglet("Évaluations", admin=True), "Évaluations"), (s.champ("Modèles d'arène"), "Modèles d'arène")])


def base_de_donnees(s):
    p = s.page
    s.reglages("admin:db")
    p.mouse.move(800, 500); p.mouse.wheel(0, 2000); p.wait_for_timeout(600)
    exp = p.get_by_role("button", name="Exporter").filter(visible=True)
    s.note(f"boutons Exporter visibles : {exp.count()}")
    suiv = lambda txt: p.get_by_text(txt, exact=True).filter(visible=True).first.locator("xpath=following::button[1]")
    s.cap("09-base-de-donnees", [(p.locator("button").filter(has_text=re.compile(r"^\s*Base de données\s*$")).filter(visible=True).first, "Base de données (onglet)"),
                                 (suiv("Importer la configuration"), "Importer"),
                                 (suiv("Exporter la configuration"), "Exporter (configuration)"),
                                 (p.get_by_text("Base de données pour le stockage.").locator("xpath=preceding::button[1]"), "Base de données (télécharger)"),
                                 (suiv("Exporter toutes les conversations"), "Exporter (conversations)"),
                                 (suiv("Utilisateurs"), "Exporter (utilisateurs)")])
    exp = p.get_by_role("button", name="Exporter").filter(visible=True)
    with p.expect_download(timeout=30000) as dl:
        exp.nth(0).click()
    d = dl.value
    s.note(f"export de configuration : {d.suggested_filename}")


def interface_admin(s):
    p = s.page
    s.reglages("admin:interface")
    s.cap_souple("10-interface-taches", [(s.onglet("Interface utilisateur", admin=True), "Interface utilisateur"),
                                         (p.get_by_text("Modèle de tâche local", exact=True).locator("xpath=following::select[1]"), "Modèle de tâche local"),
                                         (p.get_by_text("Modèle de tâche externe", exact=True).locator("xpath=following::select[1]"), "Modèle de tâche externe"),
                                         (p.get_by_text("Paramètres du modèle de tâche", exact=True).locator("xpath=following::button[1]"), "Configurer"),
                                         (s.champ("Génération du Titre"), "Génération du Titre")])


def apropos(s):
    p = s.page
    s.reglages("about")
    s.cap_souple("11-a-propos", [(s.onglet("À propos"), "À propos"), (p.get_by_text("v0.13.3").first, "v0.13.3"),
                                 (p.get_by_text("Vérifier les mises à jour disponibles").first, "Vérifier les mises à jour disponibles")])


def fiche_utilisateur(s):
    p = s.page
    d = identifiants()
    s.aller("/admin/users/overview")
    ligne = p.locator("tr").filter(has_text=d["open-webui.utilisateur.email"]).first
    ligne.get_by_role("button", name="Modifier l'utilisateur").click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    s.note("fiche utilisateur : " + dlg.inner_text().replace("\n", " | ")[:600])
    s.cap_souple("12-fiche-utilisateur", [(dlg.get_by_placeholder(re.compile("nouveau mots? de passe", re.I)).first, "Nouveau mot de passe"),
                                          (dlg.get_by_role("button", name="Enregistrer"), "Enregistrer")])
    p.keyboard.press("Escape")


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([general, cle_api, analytique, evaluations, base_de_donnees, interface_admin, apropos, fiche_utilisateur], s)
    finally:
        s.fermer()
