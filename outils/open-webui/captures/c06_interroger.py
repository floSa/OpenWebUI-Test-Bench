"""Chapitre 06 : interroger une base avec « # », lire sources et raisonnement, actions sous la réponse."""
import re
from ui import Scenario, etapes

CH = "06-interroger-ses-documents"
BASE = "Démo Vélanor"
QUESTION = "Quel est le taux de recyclage des batteries usagées collectées ?"


def appeler_base(s):
    p = s.page
    s.aller("/")
    p.locator("#chat-input").click(); p.keyboard.type("#")
    p.wait_for_timeout(1500)
    s.cap("01-diese", [(p.locator("#chat-input"), "#"), (p.get_by_text(BASE).last, BASE)])
    p.get_by_text(BASE).last.click(); p.wait_for_timeout(1000)
    p.locator("#chat-input").click(); p.keyboard.type(QUESTION)
    s.cap_souple("02-base-jointe", [(p.get_by_text(BASE).first, BASE + " (jointe)"), (p.locator("#chat-input"), "question")])
    p.locator("#send-message-button").click()
    rep = s.attendre_reponse()
    s.note(f"réponse : {rep[:500]!r}")
    msg = p.locator(".chat-assistant").last
    outil = msg.get_by_text(re.compile("Exploré|Recherché|Pensé|Thought|Searched")).first
    s.cap_souple("03-reponse", [(outil, "étapes de recherche"), (msg.locator("button").filter(has_text=re.compile("Source")).last, "Sources"),
                                (msg.locator("button[aria-label]").first, "actions sous la réponse")])


def detail(s):
    """Déplier les étapes (raisonnement, recherche), lire les sources, actions sous la réponse."""
    p = s.page
    if "/c/" not in p.url:
        cid = p.evaluate("""async () => { const r = await fetch('/api/v1/chats/?page=1',
            {headers: {Authorization: 'Bearer ' + localStorage.token}}); const d = await r.json(); return d[0].id }""")
        s.aller(f"/c/{cid}"); p.locator(".chat-assistant").last.wait_for(); p.wait_for_timeout(1500)
    msg = p.locator(".chat-assistant").last
    etapes_ = msg.get_by_text(re.compile("Exploré|Recherché|Pensé")).first
    etapes_.click(); p.wait_for_timeout(1200)
    s.cap_souple("04-etapes", [(etapes_, "étapes dépliées")])
    s.note("étapes dépliées : " + msg.inner_text().replace("\n", " | ")[:900])
    etapes_.click(); p.wait_for_timeout(600)
    src = msg.locator("button").filter(has_text=re.compile("Source")).last
    src.click(); p.wait_for_timeout(1000)
    puces = msg.locator("button").filter(has_text=re.compile(r"\.(pdf|docx|xlsx|pptx|html|md|mp3)"))
    s.note("sources : " + " | ".join(b.inner_text().strip() for b in puces.all()))
    s.cap_souple("05-sources", [(src, "Sources"), (puces.first, "document cité")])
    puces.first.click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog").last
    s.note("fenêtre source : " + dlg.inner_text().replace("\n", " | ")[:600])
    s.cap_souple("06-passage", [(dlg.locator("a, button, div").filter(has_text=re.compile(r"\.(pdf|docx|xlsx|pptx|html|md|mp3)")).first, "document"),
                                (dlg.get_by_text(re.compile("Pertinence|Relevance|%")).first, "pertinence")])
    p.keyboard.press("Escape"); p.wait_for_timeout(500)
    # actions sous la réponse
    barre = msg.locator("button[aria-label]")
    s.note("actions : " + " | ".join(filter(None, (b.get_attribute("aria-label") for b in barre.all()))))
    msg.hover(); p.wait_for_timeout(500)
    def act(nom):
        return p.locator(f"button[aria-label='{nom}']").last
    suivi = p.locator("button[aria-label^='Question de suivi']")
    s.note("questions de suivi : " + " | ".join(b.get_attribute("aria-label") for b in suivi.all()))
    s.cap_souple("07-actions", [(act("Modifier"), "Modifier"), (act("Copier"), "Copier"), (act("Lire à haute voix"), "Lire à haute voix"),
                                (act("Dupliquer la conversation"), "Dupliquer la conversation"), (act("Bonne réponse"), "Bonne réponse"),
                                (act("Mauvaise réponse"), "Mauvaise réponse"), (act("Continuer la réponse"), "Continuer la réponse"),
                                (act("Regénérer"), "Regénérer"), (suivi.first, "questions de suivi")])


def noter(s):
    p = s.page
    if "/c/" not in p.url:
        detail(s)
    msg = p.locator(".chat-assistant").last
    msg.hover(); p.wait_for_timeout(400)
    b = p.locator("button[aria-label='Bonne réponse']").last
    b.click(); p.wait_for_timeout(1500)
    s.note("après pouce : " + msg.inner_text().replace("\n", " | ")[-400:])
    s.cap_souple("08-noter", [(b, "Bonne réponse"), (msg.get_by_text(re.compile("Pourquoi|Why|raison", re.I)).first, "précisions")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([appeler_base, detail, noter], s)
    finally:
        s.fermer()
