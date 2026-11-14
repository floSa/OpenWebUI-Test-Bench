"""Chapitre 03 : premiers pas (premier compte, repérage de l'écran, langue, connexions aux modèles)."""
import re, sys
from ui import Scenario, identifiants, etapes

CH = "03-premiers-pas"


def premier_compte(s):
    """Écran d'accueil d'une instance neuve, puis création du compte administrateur (premier compte)."""
    p = s.page
    s.connecter_fait = False
    s.aller("/auth")
    s.cap("01-accueil", [(s.bouton("Démarrer"), "Démarrer")])
    s.bouton("Démarrer").click()
    p.get_by_placeholder("Entrez votre nom complet").wait_for()
    d = identifiants()
    p.get_by_placeholder("Entrez votre nom complet").fill(d["open-webui.admin.nom"])
    p.get_by_placeholder("Entrez votre adresse e-mail").fill(d["open-webui.admin.email"])
    p.get_by_placeholder("Entrez votre mot de passe").fill(d["open-webui.admin.mot_de_passe"])
    s.cap("02-compte-administrateur", [
        (p.get_by_placeholder("Entrez votre nom complet"), "Nom d'utilisateur"),
        (p.get_by_placeholder("Entrez votre adresse e-mail"), "E-mail"),
        (p.get_by_placeholder("Entrez votre mot de passe"), "Mot de passe"),
        (s.bouton("Créer un compte administrateur"), "Créer un compte administrateur")])
    s.bouton("Créer un compte administrateur").click()
    p.get_by_role("button", name="D'accord, allons-y !").wait_for(timeout=30000)
    s.cap("03-nouveautes", [(p.get_by_role("button", name="D'accord, allons-y !"), "D'accord, allons-y !")])
    p.get_by_role("button", name="D'accord, allons-y !").click()


MASQUES = ["embed", "rerank", "transcribe", "bge-m3", "bge-reranker-v2-m3", "faster-whisper-small", "qwen3.5-4b"]


def ligne_modele(p, nom):
    """Interrupteur « Activé » de la ligne du modèle `nom` (Réglages › Administrateur › Modèles)."""
    lib = p.locator("button").filter(has_text=re.compile(r"^\s*" + re.escape(nom) + r"\s+Privé")).first
    return lib.locator("xpath=ancestor::*[.//button[@aria-label='Activé']][1]").locator("button[aria-label='Activé']").first


def nouveautes(s):
    """Fenêtre « Quoi de neuf dans Open WebUI », affichée à la première connexion après une installation ou une mise à jour."""
    p = s.page
    s.aller("/auth")
    d = identifiants()
    p.locator("input[type=email], input[name=email]").first.fill(d["open-webui.admin.email"])
    p.locator("input[type=password]").first.fill(d["open-webui.admin.mot_de_passe"])
    s.cap("03-connexion", [(p.locator("input[type=email], input[name=email]").first, "E-mail"),
                           (p.locator("input[type=password]").first, "Mot de passe"),
                           (p.locator("form button[type=submit]").first, "Connexion")])
    p.locator("form button[type=submit]").first.click()
    b = p.get_by_role("button", name="D'accord, allons-y !")
    try:
        b.wait_for(timeout=15000)
        s.cap("03b-nouveautes", [(b, "D'accord, allons-y !")])
        b.click()
    except Exception:
        s.note("fenêtre des nouveautés non affichée à cette connexion")


def reperage(s):
    """Écran principal annoté, menu du compte."""
    p = s.page
    s.aller("/")
    s.fermer_nouveautes()
    p.get_by_role("button", name="Ouvrir la barre latérale").first.click()
    p.wait_for_timeout(1000)
    s.cap("04-ecran-principal", [
        (p.get_by_role("link", name="Nouvelle conversation").last, "Nouvelle conversation"),
        (p.get_by_role("button", name="Recherche").last, "Recherche"),
        (p.get_by_role("link", name="Notes").last, "Notes"),
        (p.get_by_role("link", name="Espace de travail").last, "Espace de travail"),
        (p.get_by_role("button", name="Modèle sélectionné : chat"), "chat (sélecteur de modèle)"),
        (p.locator("#chat-input"), "Comment puis-je vous aider aujourd'hui ?"),
    ])
    p.get_by_role("button", name="Claire Admin").click()
    p.wait_for_timeout(800)
    menu = p.get_by_role("menu").last
    s.cap_souple("05-menu-compte", [
        (menu.get_by_text("Réglages", exact=True), "Réglages"),
        (menu.get_by_text("Espace de travail", exact=True), "Espace de travail"),
        (menu.get_by_text("Panneau d'administration", exact=True), "Panneau d'administration"),
        (menu.get_by_text("Déconnexion", exact=True), "Déconnexion"),
    ])
    p.keyboard.press("Escape")


def langue(s):
    p = s.page
    s.reglages("general")
    s.cap("06-langue", [(s.onglet("Général"), "Général"), (s.champ("Langue"), "Langue"),
                        (s.bouton("Enregistrer", exact=True), "Enregistrer")])


def connexions(s):
    p = s.page
    s.reglages("admin:connections")
    url = p.get_by_placeholder("URL de base de l'API").first
    s.cap("07-connexions", [
        (s.onglet("Connexions", admin=True), "Connexions"),
        (url, "http://llm-central:8080/v1"),
        (p.get_by_role("button", name="Configurer").first, "Configurer (roue dentée)"),
        (p.get_by_text("API Ollama", exact=True), "API Ollama (désactivée)"),
        (p.get_by_role("button", name="Enregistrer"), "Enregistrer"),
    ])
    p.get_by_role("button", name="Configurer").first.click()
    p.wait_for_timeout(1200)
    dlg = p.get_by_role("dialog").last
    els = []
    for lib, loc in [("URL", dlg.locator("input").first), ("Clé (masquée)", dlg.locator("input").nth(1))]:
        els.append((loc, lib))
    ver = dlg.get_by_role("button", name="Vérifier la connexion")
    if ver.count():
        els.append((ver.first, "Vérifier la connexion"))
    els.append((dlg.get_by_role("button", name="Enregistrer"), "Enregistrer"))
    s.cap_souple("08-modifier-connexion", els)
    if ver.count():
        ver.first.click(); p.wait_for_timeout(3000)
        s.cap_souple("09-connexion-verifiee", [(p.locator("[data-sonner-toast]").first, "Vérification de la connexion réussie")])
    p.keyboard.press("Escape")


def modeles(s):
    """Masquer les modèles qui ne servent pas à converser (embeddings, tri, transcription, alias)."""
    p = s.page
    s.reglages("admin:models")
    p.get_by_placeholder("Rechercher des modèles").wait_for()
    s.cap("10-modeles-avant", [
        (s.onglet("Modèles", admin=True), "Modèles"),
        (ligne_modele(p, "embed"), "Activé (ligne embed)"),
        (ligne_modele(p, "chat"), "Activé (ligne chat)"),
    ])
    for nom in MASQUES:
        b = ligne_modele(p, nom)
        if b.get_attribute("aria-checked") != "false" and b.get_attribute("data-state") != "unchecked":
            b.click(); p.wait_for_timeout(700)
    s.sans_toasts()
    s.cap("11-modeles-apres", [(ligne_modele(p, "embed"), "Activé (désactivé pour embed)"),
                               (ligne_modele(p, "chat"), "Activé (ligne chat)")])
    s.aller("/")
    p.get_by_role("button", name="Modèle sélectionné : chat").click()
    p.wait_for_timeout(1000)
    s.cap_souple("12-selecteur-modeles", [(p.get_by_role("button", name="Modèle sélectionné : chat"), "chat"),
                                          (p.get_by_text("gemma-4-e4b").last, "gemma-4-e4b")])
    p.keyboard.press("Escape")


if __name__ == "__main__":
    s = Scenario(CH, connecter=not {"premier_compte", "nouveautes"} & set(sys.argv))
    try:
        etapes([premier_compte, nouveautes, reperage, langue, connexions, modeles], s)
    finally:
        s.fermer()
