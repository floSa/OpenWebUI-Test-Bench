"""Exploration : ouvre une page, clique sur une suite d'éléments (texte exact ou aria-label), enregistre le texte affiché
et les éléments visibles après chaque clic (repérage, sans capture annotée).
Usage : explorer_clic.py <chemin> <nom> <cible1> [<cible2> ...]  (cible « aria:Libellé » ou « texte:Libellé » ou « touche:Escape »)"""
import json, sys
from pathlib import Path
from ui import Scenario
chemin, nom, cibles = sys.argv[1], sys.argv[2], sys.argv[3:]
s = Scenario("_exploration")
p = s.page
s.aller(chemin); p.wait_for_timeout(2000)
out = Path("/depot/donnees/exploration"); out.mkdir(parents=True, exist_ok=True)
JS = """() => [...document.querySelectorAll('button, a, input, select, textarea, [role=switch], [role=menuitem], [role=option], label')]
  .filter(e => e.offsetParent).map(e => [e.tagName, (e.innerText||'').trim().slice(0,50), e.getAttribute('aria-label'), e.placeholder||''])"""
for i, c in enumerate(cibles):
    genre, val = c.split(":", 1)
    if genre == "aria":
        p.locator(f"[aria-label='{val}']").filter(visible=True).last.click()
    elif genre == "menu":
        p.get_by_role("menuitem").filter(has_text=val).filter(visible=True).first.click()
    elif genre == "touche":
        p.keyboard.press(val)
    else:
        p.get_by_text(val, exact=True).filter(visible=True).last.click()
    p.wait_for_timeout(1500)
    p.screenshot(path=str(out / f"{nom}-{i+1}.png"))
    dlg = p.get_by_role("dialog")
    txt = dlg.last.inner_text() if dlg.count() else p.inner_text("body")
    (out / f"{nom}-{i+1}.txt").write_text(txt)
    (out / f"{nom}-{i+1}.json").write_text(json.dumps(p.evaluate(JS), ensure_ascii=False))
    print(f"--- après {c} :", txt[:1200].replace("\n", " | "))
s.fermer()
