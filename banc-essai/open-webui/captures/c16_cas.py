"""Chapitre 16 : trois cas pratiques de bout en bout ; les trois conversations forment le jeu de démonstration.
Cas 1 : consigne de sécurité pour l'atelier (assistant qualité). Cas 2 : point fournisseur Batterix (contrat scanné + audit
en anglais, base jointe par « # »). Cas 3 : exploiter un message vocal (fichier audio de la base)."""
import re, time
from ui import Scenario, etapes

CH = "16-cas-pratiques"
ASSISTANT = "Assistant qualité Vélanor"
BASE = "Démo Vélanor"


def choisir_modele(s, nom):
    p = s.page
    p.locator("button[aria-label^='Modèle sélectionné']").first.click(); p.wait_for_timeout(800)
    p.get_by_text(nom, exact=True).filter(visible=True).first.click(); p.wait_for_timeout(800)


def joindre_base(s):
    p = s.page
    p.locator("#chat-input").click(); p.keyboard.type("#"); p.wait_for_timeout(1500)
    p.get_by_text(BASE).last.click(); p.wait_for_timeout(1000)


def poser(s, question, nom_cap, base=False, modele=None):
    p = s.page
    s.aller("/")
    if modele:
        choisir_modele(s, modele)
    if base:
        joindre_base(s)
    p.locator("#chat-input").click(); p.keyboard.type(question)
    t0 = time.time()
    p.locator("#send-message-button").click()
    rep = s.attendre_reponse()
    s.note(f"{nom_cap} ({time.time() - t0:.0f} s, attente de stabilité comprise) : {rep[:900]!r}")
    msg = p.locator(".chat-assistant").last
    src = msg.locator("button").filter(has_text=re.compile("Source")).last
    try:
        src.click(); p.wait_for_timeout(1000)
    except Exception:
        pass
    puces = msg.locator("button").filter(has_text=re.compile(r"\.(pdf|docx|xlsx|pptx|html|md|mp3)"))
    s.note(f"{nom_cap} sources : " + " | ".join(b.inner_text().strip() for b in puces.all()))
    s.cap_souple(nom_cap, [(msg.get_by_text(re.compile("Exploré|Voir le résultat")).first, "recherche dans la base"),
                           (msg.locator("p, li").first, "réponse"), (src, "sources")])
    return rep


def cas1(s):
    poser(s, "Prépare une consigne de sécurité courte pour l'atelier sur le stockage et la charge des batteries : "
             "température, local, extincteurs.", "01-consigne", modele=ASSISTANT)


def cas2(s):
    poser(s, "Fais le point sur le fournisseur Batterix : prix unitaire, délai de livraison et pénalités prévus au contrat, "
             "et score obtenu à l'audit qualité.", "02-point-fournisseur", base=True)


def cas3(s):
    poser(s, "D'après le message vocal du directeur de production, quelle ligne sera arrêtée, quand, et où la production "
             "sera-t-elle transférée ?", "03-message-vocal", base=True)


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([cas1, cas2, cas3], s)
    finally:
        s.fermer()
