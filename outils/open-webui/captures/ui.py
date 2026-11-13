"""Socle des scénarios de captures d'Open WebUI (exécutés dans le conteneur Playwright, outils/communs/captures/lancer.sh).

- navigateur 1440 × 900, interface en français (locale fr-FR et localStorage « locale » = « fr-FR ») ;
- connexion avec les identifiants fictifs de donnees/IDENTIFIANTS-LOCAUX.txt (compte administrateur par défaut) ;
- Scenario.cap(...) : capture annotée (annoter.capture) dans docs/open-webui/img/<chapitre>/<nom>.png, texte de la page dans
  outils/resultats/open-webui/captures/<chapitre>/<nom>.txt, libellés des pastilles dans .../<chapitre>/scenario.json ;
- les secrets (clé du service central, clés d'API, mots de passe) sont masqués avant capture.
"""
import json, os, re, sys, time
from pathlib import Path

from playwright.sync_api import sync_playwright, expect  # noqa: F401
import annoter

CLE_RE = re.compile(r"sk-[A-Za-z0-9_-]{8,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_.-]+")
RACINE = Path("/depot") if Path("/depot").exists() else Path(__file__).resolve().parents[3]
BASE = os.environ.get("OPENWEBUI_URL", "http://rag-open-webui:8080")
IMG = RACINE / "docs/open-webui/img"
TXT = RACINE / "outils/resultats/open-webui/captures"
IDENT = RACINE / "donnees/IDENTIFIANTS-LOCAUX.txt"


def identifiants():
    d = {}
    if IDENT.exists():
        for l in IDENT.read_text().splitlines():
            if "=" in l and l.startswith("open-webui."):
                k, v = l.split("=", 1); d[k.strip()] = v.strip()
    return d


class Scenario:
    def __init__(self, chapitre, connecter=True, compte="admin", langue="fr-FR"):
        self.chapitre = chapitre
        self.journal = []
        self._pw = sync_playwright().start()
        self.navigateur = self._pw.chromium.launch()
        self.contexte = self.navigateur.new_context(viewport={"width": 1440, "height": 900}, locale="fr-FR",
                                                    accept_downloads=True)
        if langue:
            self.contexte.add_init_script(
                f"try {{ if (!localStorage.getItem('locale')) localStorage.setItem('locale', '{langue}') }} catch (e) {{}}")
        self.page = self.contexte.new_page()
        self.page.set_default_timeout(30000)
        if connecter:
            self.connecter(compte)

    # ---------- navigation ----------
    def aller(self, chemin, attendre=None):
        self.page.goto(BASE + chemin)
        try:
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        if attendre is not None:
            attendre.wait_for(state="visible")
        self.page.wait_for_timeout(800)

    def connecter(self, compte="admin"):
        d = identifiants()
        p = self.page
        p.goto(BASE + "/auth")
        p.wait_for_load_state("networkidle")
        email = p.locator("input[type=email], input[name=email]").first
        try:
            email.wait_for(state="visible", timeout=6000)
        except Exception:
            return  # session déjà ouverte
        email.fill(d[f"open-webui.{compte}.email"])
        p.locator("input[type=password]").first.fill(d[f"open-webui.{compte}.mot_de_passe"])
        p.locator("form button[type=submit]").first.click()
        p.wait_for_url(re.compile(r".*/(c/.*)?$"), timeout=30000)
        p.wait_for_load_state("networkidle")
        p.wait_for_timeout(1500)
        self.fermer_nouveautes()

    def fermer_nouveautes(self):
        """Ferme la fenêtre « Nouveautés » (changelog) affichée à la première connexion d'une version."""
        p = self.page
        for nom in ("Okay, allons-y !", "D'accord, allons-y !", "Okay, Let's Go!"):
            b = p.get_by_role("button", name=nom)
            if b.count() and b.first.is_visible():
                b.first.click(); p.wait_for_timeout(600)

    # ---------- captures ----------
    def cap(self, nom, elements=(), masques=(), plein=False, clip=None, attendre=None, note="", auto=True):
        """elements : liste de (locator, libellé). Écrit image, texte de la page et libellés."""
        if attendre is not None:
            attendre.wait_for(state="visible")
        self.page.wait_for_timeout(500)
        img = IMG / self.chapitre / f"{nom}.png"
        txt = TXT / self.chapitre / f"{nom}.txt"
        masques = list(masques) + (self._secrets_visibles() if auto else [])
        libs = annoter.capture(self.page, img, elements, masques=masques, plein=plein, clip=clip, texte=txt)
        txt.write_text(CLE_RE.sub("[clé masquée]", txt.read_text()))
        self.journal.append({"capture": f"{self.chapitre}/{nom}.png", "url": self.page.url.replace(BASE, ""),
                             "pastilles": libs, "note": note, "heure": time.strftime("%H:%M:%S")})
        self._ecrire_journal()
        return libs

    def cap_souple(self, nom, elements=(), **kw):
        """Comme cap, mais ignore (et note) les éléments introuvables ou invisibles."""
        garde = []
        for loc, lib in elements:
            try:
                loc.wait_for(state="visible", timeout=5000); garde.append((loc, lib))
            except Exception:
                self.note(f"{nom} : élément absent « {lib} »")
        return self.cap(nom, garde, **kw)

    def _secrets_visibles(self):
        """Champs de clé ou de mot de passe remplis, et textes ressemblant à une clé : masqués d'office."""
        res = []
        for sel in ("input[type=password]", "input[name*=key i]", "input[placeholder*=clé i]", "input[placeholder*=key i]"):
            for loc in self.page.locator(sel).all():
                try:
                    if loc.is_visible() and loc.input_value():
                        res.append(loc)
                except Exception:
                    pass
        for loc in self.page.get_by_text(CLE_RE).all():
            try:
                if loc.is_visible():
                    res.append(loc)
            except Exception:
                pass
        for loc in self.page.locator("input").all():
            try:
                if loc.is_visible() and CLE_RE.search(loc.input_value() or ""):
                    res.append(loc)
            except Exception:
                pass
        return res

    def _ecrire_journal(self):
        f = TXT / self.chapitre / "scenario.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        anciens = json.loads(f.read_text()) if f.exists() else []
        noms = {j["capture"] for j in self.journal}
        anciens = [a for a in anciens if a["capture"] not in noms]
        f.write_text(json.dumps(anciens + self.journal, ensure_ascii=False, indent=1))

    def note(self, texte):
        texte = CLE_RE.sub("[clé masquée]", str(texte))
        print("NOTE", texte, flush=True)
        f = TXT / self.chapitre / "notes.log"
        f.parent.mkdir(parents=True, exist_ok=True)
        with f.open("a") as h:
            h.write(time.strftime("%Y-%m-%d %H:%M:%S ") + texte + "\n")

    # ---------- aides ----------
    def sans_toasts(self, delai=12000):
        try:
            self.page.wait_for_function("() => document.querySelectorAll('[data-sonner-toast]').length === 0", timeout=delai)
        except Exception:
            self.page.evaluate("() => document.querySelectorAll('[data-sonner-toast]').forEach(t => t.remove())")

    def attendre_reponse(self, stable=4000, maxi=300000):
        """Attend que la dernière réponse du modèle ne change plus pendant `stable` ms (leçon Kotaemon)."""
        p = self.page
        debut, dernier, depuis = time.time(), None, time.time()
        p.wait_for_timeout(2000)
        while time.time() - debut < maxi / 1000:
            t = p.evaluate("() => { const m = document.querySelectorAll('#response-content-container, .chat-assistant'); "
                           "return m.length ? m[m.length-1].innerText : '' }")
            enc = p.locator("button[aria-label='Stop'], button:has-text('Arrêter')").count()
            if t != dernier:
                dernier, depuis = t, time.time()
            elif t and not enc and (time.time() - depuis) * 1000 >= stable:
                return t
            p.wait_for_timeout(700)
        self.note("réponse non stabilisée dans le délai")
        return dernier

    def bouton(self, nom, exact=False):
        return self.page.get_by_role("button", name=nom, exact=exact)

    def texte(self, t, exact=False):
        return self.page.get_by_text(t, exact=exact)

    def fermer(self):
        try:
            self.navigateur.close()
        finally:
            self._pw.stop()


def etapes(fonctions, scenario):
    """Lance les fonctions demandées en argument (ou toutes), dans l'ordre."""
    noms = sys.argv[1:] or [f.__name__ for f in fonctions]
    for f in fonctions:
        if f.__name__ in noms:
            print("==", f.__name__, flush=True)
            f(scenario)
