"""Chapitre 04 : première question en dix minutes (un document joint à une conversation, une question, la source)."""
from ui import Scenario, etapes

CH = "04-premiere-question"
DOC = "/depot/corpus/documents/rapport-annuel-2025.pdf"
QUESTION = "Quel est le chiffre d'affaires 2025 de Vélanor ?"


def joindre(s):
    p = s.page
    s.aller("/")
    p.locator("#chat-input").wait_for()
    plus = p.locator("button[aria-label='Plus']").last
    plus.click(); p.wait_for_timeout(800)
    item = p.get_by_role("menuitem").filter(has_text="Téléverser des fichiers").first
    s.cap("01-menu-plus", [(plus, "+"), (item, "Téléverser des fichiers")])
    with p.expect_file_chooser() as fc:
        item.click()
    fc.value.set_files(DOC)
    puce = p.get_by_text("rapport-annuel-2025.pdf").first
    puce.wait_for(timeout=60000)
    p.wait_for_timeout(4000)  # fin du traitement du fichier (lecture, découpage, embeddings)
    p.locator("#chat-input").click()
    p.keyboard.type(QUESTION)
    s.cap("02-document-joint", [(puce, "rapport-annuel-2025.pdf"), (p.locator("#chat-input"), "question"),
                                (p.locator("#send-message-button"), "Envoyer")])
    p.locator("#send-message-button").click()
    rep = s.attendre_reponse()
    s.note(f"réponse : {rep[:400]!r}")
    p.wait_for_timeout(1500)
    msg = p.locator(".chat-assistant").last
    pensee = msg.get_by_text("Pensé", exact=False).first
    sources = msg.locator("button").filter(has_text="rapport-annuel-2025").first
    s.cap_souple("03-reponse", [(pensee, "Pensé pendant …"), (msg.locator("#response-content-container").first, "réponse"),
                                (sources, "source citée")])
    try:
        sources.click(); p.wait_for_timeout(1500)
        dlg = p.get_by_role("dialog").last
        s.cap_souple("04-source", [(dlg.get_by_text("rapport-annuel-2025.pdf").first, "document"),
                                   (dlg.get_by_text("48,6").first, "passage utilisé")])
        p.keyboard.press("Escape")
    except Exception as e:
        s.note(f"source : {e}")


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([joindre], s)
    finally:
        s.fermer()
