"""Chapitre 03 : premiers pas (premier compte, repérage de l'écran, langue, connexions aux modèles)."""
import sys
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
    p.wait_for_timeout(5000)
    p.screenshot(path="/depot/donnees/exploration/apres-compte.png")
    print(p.url); print(p.inner_text("body")[:2500])


if __name__ == "__main__":
    s = Scenario(CH, connecter="premier_compte" not in sys.argv)
    try:
        etapes([premier_compte], s)
    finally:
        s.fermer()
