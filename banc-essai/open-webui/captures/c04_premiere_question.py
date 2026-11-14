"""Chapitre 04 : première question en dix minutes (un document joint à une conversation, une question, la source)."""
from ui import Scenario, etapes

CH = "04-premiere-question"
DOC = "/depot/banc-essai/corpus/documents/rapport-annuel-2025.pdf"
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
    outil = msg.get_by_text("Exploré", exact=False).first
    sources = msg.locator("button").filter(has_text="rapport-annuel-2025").first
    liste = msg.locator("button").filter(has_text="Source").last
    s.cap_souple("03-reponse", [(outil, "Exploré query_chat_files"), (sources, "rapport-annuel-2025.pdf (citation)"),
                                (liste, "1 Source")])
    source(s)


def derniere_conversation(s):
    """Ouvre la conversation la plus récente (API de l'instance, jeton de la session du navigateur)."""
    cid = s.page.evaluate("""async () => { const r = await fetch('/api/v1/chats/?page=1',
        {headers: {Authorization: 'Bearer ' + localStorage.token}}); const d = await r.json(); return d[0].id }""")
    s.aller(f"/c/{cid}")
    s.page.locator(".chat-assistant").last.wait_for()
    s.page.wait_for_timeout(1500)


def source(s):
    p = s.page
    if "/c/" not in p.url:
        derniere_conversation(s)
    msg = p.locator(".chat-assistant").last
    liste = msg.locator("button").filter(has_text="Source").last
    liste.click(); p.wait_for_timeout(1000)
    puce = msg.locator("button").filter(has_text="rapport-annuel-2025").last
    s.cap_souple("04-liste-sources", [(liste, "1 Source"), (puce, "rapport-annuel-2025.pdf")])
    puce.click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog").last
    s.cap_souple("05-source", [(dlg.get_by_text("rapport-annuel-2025.pdf").first, "rapport-annuel-2025.pdf"),
                               (dlg.get_by_text("Contenu", exact=True).first, "Contenu")])
    p.keyboard.press("Escape")

if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([joindre, source], s)
    finally:
        s.fermer()
