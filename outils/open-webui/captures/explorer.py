"""Exploration : ouvre une page d'Open WebUI, enregistre texte, éléments cliquables et capture brute (repérage).
Usage : explorer.py <chemin> [nom] [--connecter]"""
import json, sys
from pathlib import Path
from ui import Scenario
args = [a for a in sys.argv[1:] if not a.startswith("--")]
chemin, nom = args[0], (args[1] if len(args) > 1 else "page")
s = Scenario("_exploration", connecter="--connecter" in sys.argv)
s.aller(chemin)
s.page.wait_for_timeout(2500)
out = Path("/depot/donnees/exploration"); out.mkdir(parents=True, exist_ok=True)
s.page.screenshot(path=str(out / f"{nom}.png"))
(out / f"{nom}.txt").write_text(s.page.inner_text("body"))
el = s.page.evaluate("""() => [...document.querySelectorAll('button, a, input, select, textarea, [role=switch], [role=tab], [role=menuitem]')]
  .filter(e => e.offsetParent).map(e => ({tag: e.tagName, txt: (e.innerText||'').trim().slice(0,60), aria: e.getAttribute('aria-label'),
   href: e.getAttribute('href'), id: e.id, name: e.name, type: e.type, ph: e.placeholder}))""")
(out / f"{nom}.json").write_text(json.dumps(el, ensure_ascii=False, indent=0))
print(s.page.url); print(s.page.inner_text("body")[:1500])
s.fermer()
