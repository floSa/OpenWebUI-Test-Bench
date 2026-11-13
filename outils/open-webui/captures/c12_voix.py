"""Chapitre 12 : voix (dictée par `transcribe`, lecture par la voix du navigateur) et page « Recherche Web » (non branchée).
Faux micro de Chromium : donnees/voix-dictee.wav (14 premières secondes du message vocal du corpus, converties par ffmpeg)."""
import re
from ui import Scenario, etapes

CH = "12-voix-et-recherche-web"
WAV = "/depot/donnees/voix-dictee.wav"
ARGS = ["--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream", f"--use-file-for-fake-audio-capture={WAV}%noloop"]


def selecteur(p, libelle):
    return p.get_by_text(libelle, exact=True).filter(visible=True).first.locator("xpath=following::select[1]")


def reglages_audio(s):
    p = s.page
    s.reglages("admin:audio")
    stt = selecteur(p, "Moteur de reconnaissance vocale")
    stt.evaluate("e => e.scrollIntoView({block: 'center'})"); p.wait_for_timeout(500)
    modele = p.get_by_text("Modèle de Speech-to-Text", exact=True).filter(visible=True).first.locator("xpath=following::input[1]")
    tts = selecteur(p, "Moteur de Text-to-Speech")
    s.note("réglages audio : " + p.get_by_role("dialog").last.inner_text().split("Reconnaissance vocale")[-1][:600].replace("\n", " | "))
    s.cap_souple("01-audio", [(s.onglet("Audio", admin=True), "Audio"), (stt, "Moteur de reconnaissance vocale"),
                              (modele, "Modèle de Speech-to-Text"), (tts, "Moteur de Text-to-Speech")])
    p.keyboard.press("Escape")


def dicter(s):
    """Sollicite `transcribe` : dictée par le faux micro."""
    p = s.page
    s.aller("/")
    micro = p.locator("button[aria-label='Saisie vocale']").first
    s.cap("02-micro", [(micro, "Saisie vocale"), (p.locator("button[aria-label='Mode vocal']").first, "Mode vocal")])
    micro.click(); p.wait_for_timeout(5000)
    s.note("pendant l'enregistrement : " + " | ".join(filter(None, (b.get_attribute("aria-label") for b in p.locator("button[aria-label]").filter(visible=True).all())))[-400:])
    arret = p.locator("button[aria-label*='Confirm' i], button[aria-label*='Arrêter' i], button[aria-label*='Stop' i], button[aria-label*='Valider' i]").filter(visible=True)
    s.cap_souple("03-enregistrement", [(arret.last, "valider l'enregistrement")])
    p.wait_for_timeout(9000)
    if arret.count():
        arret.last.click()
    for _ in range(60):
        v = p.locator("#chat-input").inner_text()
        if v.strip():
            break
        p.wait_for_timeout(1000)
    s.note("texte dicté : " + p.locator("#chat-input").inner_text()[:500])
    s.cap_souple("04-texte-dicte", [(p.locator("#chat-input"), "texte transcrit")])


def lire(s):
    """Bouton « Lire à voix haute » sous une réponse existante (voix du navigateur)."""
    p = s.page
    s.aller("/")
    b = p.locator("button[aria-label='Ouvrir la barre latérale']").filter(visible=True)
    if b.count():
        b.first.click(); p.wait_for_timeout(800)
    p.locator("a[href^='/c/']").filter(has_text="Chiffre d'affaires 2025").first.click(); p.wait_for_timeout(2500)
    msg = p.locator(".chat-assistant").last
    msg.hover(); p.wait_for_timeout(500)
    lire_ = msg.locator("button[aria-label='Lire à voix haute']").first
    s.cap_souple("05-lire", [(lire_, "Lire à voix haute")])
    lire_.click(); p.wait_for_timeout(2000)
    s.note("après lecture : " + " | ".join(filter(None, (x.get_attribute("aria-label") for x in msg.locator("button[aria-label]").all()))))


def recherche_web(s):
    p = s.page
    s.reglages("admin:web")
    inter = p.get_by_text("Recherche Web", exact=True).filter(visible=True).last.locator("xpath=following::*[@role='switch'][1]")
    s.note("recherche web activée : " + str(inter.get_attribute("aria-checked")))
    s.cap_souple("06-recherche-web", [(s.onglet("Recherche Web", admin=True), "Recherche Web"), (inter, "interrupteur")])
    p.keyboard.press("Escape")


if __name__ == "__main__":
    s = Scenario(CH, args=ARGS, permissions=["microphone"])
    try:
        etapes([reglages_audio, dicter, lire, recherche_web], s)
    finally:
        s.fermer()
