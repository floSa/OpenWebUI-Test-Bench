"""Chapitre 14 : comptes, groupes et permissions (compte fictif Julien Moreau, groupe « Équipe production »)."""
import re, sys
from ui import Scenario, identifiants, etapes

CH = "14-comptes-groupes-permissions"
GROUPE = "Équipe production"


def ajouter_compte(s):
    p = s.page
    d = identifiants()
    s.aller("/admin/users/overview")
    ajout = p.get_by_role("button", name="Ajouter un utilisateur", exact=True).first
    s.cap("01-utilisateurs", [(s.el("Utilisateurs"), "Utilisateurs"),
                              (s.el("Aperçu", debut=True), "Aperçu"),
                              (ajout, "Ajouter un utilisateur")])
    ajout.click()
    dlg = p.get_by_role("dialog").last
    dlg.get_by_placeholder("Entrez votre nom complet").wait_for()
    dlg.get_by_label("Rôle").select_option("user")
    dlg.get_by_placeholder("Entrez votre nom complet").fill(d["open-webui.utilisateur.nom"])
    dlg.get_by_placeholder("Entrez votre adresse e-mail").fill(d["open-webui.utilisateur.email"])
    dlg.get_by_placeholder("Entrez votre mot de passe").fill(d["open-webui.utilisateur.mot_de_passe"])
    s.cap("02-ajouter-utilisateur", [(dlg.get_by_role("button", name="Formulaire"), "Formulaire"),
                                     (dlg.get_by_label("Rôle"), "Rôle"),
                                     (dlg.get_by_placeholder("Entrez votre nom complet"), "Nom d'utilisateur"),
                                     (dlg.get_by_placeholder("Entrez votre adresse e-mail"), "E-mail"),
                                     (dlg.get_by_placeholder("Entrez votre mot de passe"), "Mot de passe"),
                                     (dlg.get_by_role("button", name="Enregistrer"), "Enregistrer")])
    dlg.get_by_role("button", name="Enregistrer").click()
    p.get_by_text(d["open-webui.utilisateur.email"]).first.wait_for()
    s.sans_toasts()
    ligne = p.locator("tr").filter(has_text=d["open-webui.utilisateur.email"]).first
    s.cap_souple("03-liste-comptes", [(ligne, "nouveau compte"),
                                      (ligne.locator("button").first, "rôle"),
                                      (ligne.get_by_role("button", name="Modifier l'utilisateur"), "Modifier l'utilisateur")])


def groupe(s):
    p = s.page
    d = identifiants()
    s.aller("/admin/users/groups")
    nouveau = p.get_by_role("button", name="Nouveau groupe", exact=True).first
    nouveau.click()
    dlg = p.get_by_role("dialog").last
    dlg.get_by_placeholder("Nom du groupe").wait_for()
    dlg.get_by_placeholder("Nom du groupe").fill(GROUPE)
    dlg.get_by_placeholder("Description du groupe").fill("Atelier et logistique de Nantes")
    s.cap("04-nouveau-groupe", [(dlg.get_by_role("button", name="Général"), "Général"),
                                (dlg.get_by_role("button", name="Permissions"), "Permissions"),
                                (dlg.get_by_placeholder("Nom du groupe"), "Nom du groupe"),
                                (dlg.locator("select").first, "Qui est autorisé à partager avec ce groupe"),
                                (dlg.get_by_role("button", name="Enregistrer"), "Enregistrer")])
    dlg.get_by_role("button", name="Permissions").click(); p.wait_for_timeout(1000)
    s.note("permissions du groupe : " + dlg.inner_text().replace("\n", " | ")[:2500])
    s.cap("05-permissions", [(dlg.get_by_role("button", name="Permissions"), "Permissions")], note="permissions par défaut")
    dlg.get_by_role("button", name="Enregistrer").click(); p.wait_for_timeout(1500)
    s.sans_toasts()


def membres(s):
    p = s.page
    d = identifiants()
    s.aller("/admin/users/groups")
    p.get_by_text(GROUPE, exact=True).first.click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog").last
    dlg.get_by_role("button", name="Utilisateurs").click(); p.wait_for_timeout(1200)
    ligne = dlg.locator("tr").filter(has_text=d["open-webui.utilisateur.nom"]).first
    case = ligne.locator("input[type=checkbox], button[role=checkbox], button").first
    case.click(); p.wait_for_timeout(1200)
    s.cap("06-membres", [(dlg.get_by_role("button", name="Utilisateurs"), "Utilisateurs"),
                         (case, "case MEMBRE de Julien Moreau")])
    p.keyboard.press("Escape"); p.wait_for_timeout(1500)
    s.aller("/admin/users/groups")
    s.cap("07-groupes", [(p.get_by_text(GROUPE, exact=True).first, GROUPE),
                         (p.get_by_text("Autorisations par défaut").first, "Autorisations par défaut")])

def authentification(s):
    p = s.page
    s.reglages("admin:authentication")
    s.cap_souple("08-authentification", [(s.onglet("Authentification", admin=True), "Authentification"),
                                         (s.champ("Rôle utilisateur par défaut"), "Rôle utilisateur par défaut"),
                                         (s.champ("Groupe par défaut"), "Groupe par défaut"),
                                         (s.champ("Nouveaux comptes"), "Nouveaux comptes"),
                                         (s.champ("Clés API"), "Clés API")])


def partager(s, nom_cap, ouvrir, enregistrer=None):
    """Contrôle d'accès commun aux modèles et aux bases : ajoute le groupe, capture la fenêtre."""
    p = s.page
    ouvrir()
    acces = p.locator("button").filter(has_text=re.compile(r"^\s*Accès\s*$")).filter(visible=True).last
    acces.click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    deja = GROUPE in dlg.inner_text()
    ajout = dlg.get_by_role("button", name=re.compile("Ajouter un accès")).first
    if deja:
        s.note(nom_cap + " : groupe déjà présent, ajout non refait")
    else:
        ajout.click(); p.wait_for_timeout(1200)
    choix = p.get_by_role("dialog").last
    ligne = choix.locator("div, li, label").filter(has_text=GROUPE).last
    if not deja:
        case = choix.locator("input[type=checkbox], button[role=checkbox]").first
        case.click(); p.wait_for_timeout(400)
        s.cap(nom_cap + "-a", [(choix.get_by_text(GROUPE).first, GROUPE), (case, "case à cocher"),
                               (choix.get_by_role("button", name="Ajouter"), "Ajouter")])
        choix.get_by_role("button", name="Ajouter").click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    s.cap_souple(nom_cap + "-b", [(dlg.get_by_role("button", name=re.compile("^Visibilité")).first, "Visibilité"),
                                  (dlg.get_by_text(GROUPE).first, GROUPE)])
    s.note(nom_cap + " : " + dlg.inner_text().replace("\n", " | ")[:600])
    p.keyboard.press("Escape"); p.wait_for_timeout(800)
    if enregistrer:
        enregistrer()


def partager_modele(s):
    p = s.page
    def ouvrir():
        s.reglages("admin:models")
        lib = p.locator("button").filter(has_text=re.compile(r"^\s*chat\b")).first
        lib.locator("xpath=ancestor::*[.//button[@aria-label='Modifier']][1]").locator("button[aria-label='Modifier']").first.click()
        p.wait_for_timeout(2000)
    def enregistrer():
        b = p.get_by_role("button", name="Enregistrer & Mettre à jour")
        if b.count() and b.first.is_visible():
            b.first.click(); p.wait_for_timeout(2000)
    partager(s, "09-partage-modele", ouvrir)
    s.reglages("admin:models")
    s.cap("10-modele-partage", [(p.locator("button").filter(has_text=re.compile(r"^\s*chat\s+Partagé")).filter(visible=True).first, "chat Partagé"),
                                (p.locator("button").filter(has_text=re.compile(r"^\s*gemma-4-e4b\s+Privé")).filter(visible=True).first, "gemma-4-e4b Privé")])


def retirer_partage_bge(s):
    """Nettoyage : un premier passage du scénario a partagé bge-m3 par erreur ; on retire cet accès (croix)."""
    p = s.page
    s.reglages("admin:models")
    lib = p.locator("button").filter(has_text=re.compile(r"^\s*bge-m3\s+Partagé")).filter(visible=True).first
    if not lib.count():
        s.note("bge-m3 non partagé : rien à retirer"); return
    lib.locator("xpath=ancestor::*[.//button[@aria-label='Modifier']][1]").locator("button[aria-label='Modifier']").first.click()
    p.wait_for_timeout(2000)
    p.locator("button").filter(has_text=re.compile(r"^\s*Accès\s*$")).filter(visible=True).last.click(); p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    ligne = dlg.locator("div").filter(has_text=GROUPE).filter(has=p.locator("button")).last
    ligne.locator("button").last.click(); p.wait_for_timeout(1500)
    s.note("accès de bge-m3 après retrait : " + dlg.inner_text().replace("\n", " | ")[:300])


def partager_base(s):
    p = s.page
    def ouvrir():
        s.aller("/workspace/knowledge")
        p.get_by_role("link", name="Démo Vélanor").first.click()
        p.get_by_placeholder("Nom de la connaissance").wait_for(); p.wait_for_timeout(1000)
    partager(s, "11-partage-base", ouvrir)


def cote_utilisateur(s, apres=False):
    """Connexion avec le compte Julien Moreau, avant ou après le partage du modèle et de la base."""
    u = s.autre_session("utilisateur")
    try:
        p = u.page
        p.locator("#chat-input").wait_for()
        sel = p.get_by_role("button", name=re.compile("Modèle sélectionné|Sélectionnez un modèle")).first
        if not apres:
            u.cap("12-utilisateur-avant", [(sel, "Sélectionnez un modèle"), (p.locator("#chat-input"), "zone de saisie")])
            return
        p.locator("#chat-input").click(); p.keyboard.type("#")
        p.wait_for_timeout(1500)
        u.cap_souple("15-utilisateur-apres", [(sel, "chat"), (p.get_by_text("Démo Vélanor").last, "Démo Vélanor")])
        p.keyboard.press("Escape")
    finally:
        u.fermer()


def utilisateur_avant(s):
    cote_utilisateur(s)


def utilisateur_apres(s):
    cote_utilisateur(s, apres=True)

if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([ajouter_compte, groupe, membres, authentification, utilisateur_avant, partager_modele, partager_base, utilisateur_apres, retirer_partage_bge], s)
    finally:
        s.fermer()
