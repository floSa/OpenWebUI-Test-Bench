"""Carte de l'interface : une capture de repérage par page, par onglet de la fenêtre Réglages et par menu.
Texte de chaque page et liste de ses éléments cliquables dans outils/resultats/open-webui/captures/carte/."""
import json, sys
from ui import Scenario, etapes

PAGES = [("accueil", "/"), ("modeles", "/workspace/models"), ("connaissances", "/workspace/knowledge"),
         ("prompts", "/workspace/prompts"), ("outils", "/workspace/tools"), ("skills", "/workspace/skills"),
         ("notes", "/notes"), ("automatisations", "/automations"), ("calendrier", "/calendar"),
         ("playground", "/playground"), ("playground-completions", "/playground/completions"),
         ("admin-utilisateurs", "/admin/users/overview"), ("admin-groupes", "/admin/users/groups"),
         ("admin-classement", "/admin/evaluations/leaderboard"), ("admin-avis", "/admin/evaluations/feedback"),
         ("admin-fonctions", "/admin/functions"), ("admin-analytique", "/admin/analytics")]
REGLAGES = ["general", "interface", "notifications", "shortcuts", "connections", "tools", "personalization", "audio",
            "data_controls", "usage", "archived_chats", "account", "about",
            "admin:general", "admin:authentication", "admin:interface", "admin:connections", "admin:models",
            "admin:subagents", "admin:integrations", "admin:apps", "admin:documents", "admin:audio", "admin:images",
            "admin:web", "admin:code-execution", "admin:pipelines", "admin:analytics", "admin:evaluations", "admin:db"]


def elements(s):
    return s.page.evaluate("""() => [...document.querySelectorAll('button, a, input, select, textarea, [role=switch], [role=tab], [role=menuitem]')]
      .filter(e => e.offsetParent).map(e => [e.tagName, (e.innerText||'').trim().replace(/\\s+/g,' ').slice(0,60), e.getAttribute('aria-label')||'', e.placeholder||'', e.getAttribute('href')||''])""")


def enregistrer(s, nom):
    s.cap(nom, plein=False)
    (s.page and (s.TXT if hasattr(s, 'TXT') else None))
    from ui import TXT
    (TXT / "carte" / f"{nom}.json").write_text(json.dumps(elements(s), ensure_ascii=False, indent=0))


def pages(s):
    for nom, chemin in PAGES:
        try:
            s.aller(chemin); s.page.wait_for_timeout(1500)
            enregistrer(s, nom)
        except Exception as e:
            s.note(f"{nom} : {e}")


def reglages(s):
    for t in REGLAGES:
        nom = "reglages-" + t.replace(":", "-").replace("_", "-")
        try:
            s.aller(f"/?settings={t}"); s.page.wait_for_timeout(1800)
            enregistrer(s, nom)
        except Exception as e:
            s.note(f"{nom} : {e}")


def menus(s):
    p = s.page
    s.aller("/")
    # menu du compte (avatar en bas de la barre latérale)
    try:
        p.locator("button[aria-label='Menu utilisateur'], button[aria-label='User Menu']").first.click()
    except Exception:
        p.get_by_text("Claire Admin").first.click()
    p.wait_for_timeout(800); enregistrer(s, "menu-compte"); p.keyboard.press("Escape")


if __name__ == "__main__":
    s = Scenario("carte")
    try:
        etapes([pages, reglages, menus], s)
    finally:
        s.fermer()
