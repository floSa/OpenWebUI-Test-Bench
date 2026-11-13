"""Chapitre 05 : créer et alimenter une base de connaissances (« Démo Vélanor », jeu de démonstration)."""
import glob, re, sys
from ui import Scenario, etapes

CH = "05-bases-de-connaissances"
NOM = "Démo Vélanor"
DOCS = sorted(f for f in glob.glob("/depot/corpus/documents/*") if not f.endswith("contrat-batterix-scan.pdf"))
SCAN = "/depot/corpus/documents/contrat-batterix-scan.pdf"


def ouvrir_base(s):
    p = s.page
    s.aller("/workspace/knowledge")
    p.get_by_role("link", name=NOM).first.click()
    p.get_by_placeholder("Nom de la connaissance").wait_for()
    p.wait_for_timeout(1200)


def creer(s):
    p = s.page
    s.aller("/workspace/knowledge")
    creer = p.get_by_role("button", name="Créer", exact=True).first
    s.cap("01-liste", [(p.get_by_role("link", name=re.compile("^Connaissances")).first, "Connaissances"),
                       (creer, "Créer"), (p.get_by_placeholder("Rechercher des connaissances"), "Rechercher des connaissances")])
    creer.click()
    nom = p.get_by_placeholder("Nommez votre base de connaissances")
    nom.wait_for()
    nom.fill(NOM)
    p.get_by_placeholder("Décrivez votre base de connaissances et vos objectifs").fill(
        "Documents fictifs de l'entreprise Vélanor : rapport annuel, procédures, stocks, stratégie, audit, SAV.")
    s.cap("02-creer", [(nom, "Nommez votre base de connaissances"),
                       (p.get_by_placeholder("Décrivez votre base de connaissances et vos objectifs"), "description"),
                       (p.get_by_role("button", name=re.compile("^Visibilité")), "Visibilité"),
                       (p.get_by_role("button", name="Créer une connaissance"), "Créer une connaissance")])
    p.get_by_role("button", name="Créer une connaissance").click()
    p.get_by_placeholder("Nom de la connaissance").wait_for()
    p.wait_for_timeout(1500)
    s.cap("03-base-vide", [(p.get_by_placeholder("Nom de la connaissance"), "nom de la base"),
                           (p.get_by_role("button", name="Ajouter du contenu"), "Ajouter du contenu"),
                           (p.get_by_role("button", name="Accès"), "Accès")])


def alimenter(s):
    p = s.page
    ouvrir_base(s)
    ajout = p.get_by_role("button", name="Ajouter du contenu")
    ajout.click(); p.wait_for_timeout(800)
    item = p.get_by_role("menuitem").filter(has_text=re.compile("Téléverser des fichiers")).first
    items = p.get_by_role("menuitem").all()
    s.note("menu Ajouter du contenu : " + " | ".join(i.inner_text().strip() for i in items))
    s.cap("04-menu-ajout", [(ajout, "Ajouter du contenu"), (item, "Téléverser des fichiers")])
    with p.expect_file_chooser() as fc:
        item.click()
    fc.value.set_files(DOCS)
    p.wait_for_timeout(2500)
    s.cap("05-televersement", [(p.locator("button").filter(has_text="rapport-annuel-2025.pdf").first, "fichier en cours de traitement")],
          note="pendant le traitement")
    # attente : chaque fichier listé et traitement terminé (plus d'indicateur de chargement)
    for _ in range(120):
        n = sum(1 for f in DOCS if p.locator("button").filter(has_text=f.rsplit("/", 1)[1]).count())
        if n == len(DOCS) and not p.locator(".animate-spin").count():
            break
        p.wait_for_timeout(1000)
    s.sans_toasts()
    s.cap("06-base-remplie", [(p.get_by_placeholder("Rechercher une collection"), "Rechercher une collection"),
                              (p.locator("button").filter(has_text="procedure-batteries.docx").first, "procedure-batteries.docx")])
    apercu(s, deja=True)


def apercu(s, deja=False):
    p = s.page
    if not deja:
        ouvrir_base(s)
    s.sans_toasts()
    p.get_by_text("procedure-batteries.docx", exact=True).first.click()
    texte = p.get_by_text("PR-SEC-04", exact=False).first
    try:
        texte.wait_for(timeout=15000)
    except Exception:
        s.note("aperçu : texte non affiché après le clic")
    p.wait_for_timeout(1000)
    s.cap_souple("07-apercu-fichier", [(p.locator("button").filter(has_text="procedure-batteries.docx").first, "fichier choisi"),
                                       (texte, "texte extrait")])

def scan_refuse(s):
    """Le PDF scanné, sans texte, est refusé avec la lecture par défaut (chapitre 17 ; corrigé au chapitre 08)."""
    p = s.page
    ouvrir_base(s)
    p.get_by_role("button", name="Ajouter du contenu").click(); p.wait_for_timeout(800)
    with p.expect_file_chooser() as fc:
        p.get_by_role("menuitem").filter(has_text=re.compile("Téléverser des fichiers")).first.click()
    fc.value.set_files(SCAN)
    toast = p.locator("[data-sonner-toast]").filter(has_text=re.compile("empty|vide", re.I)).first
    try:
        toast.wait_for(timeout=60000)
        s.cap("08-scan-refuse", [(toast, "message d'erreur")])
    except Exception:
        p.wait_for_timeout(3000)
        s.cap_souple("08-scan-refuse", [(p.locator("[data-sonner-toast]").first, "message")])
        s.note("message attendu non trouvé ; texte : " + p.inner_text("body")[:500])


def retirer(s):
    p = s.page
    ouvrir_base(s)
    ligne = p.locator("button").filter(has_text="contrat-batterix-scan.pdf").first
    if not ligne.count():
        s.note("scan absent de la liste (refusé) : retrait montré sur la ligne faq-sav.html sans cliquer « Supprimer »")
        ligne = p.locator("button").filter(has_text="faq-sav.html").first
    plus = ligne.locator("xpath=following-sibling::*//button[@aria-label='Plus'] | following::button[@aria-label='Plus'][1]").first
    plus.click(); p.wait_for_timeout(800)
    mi = p.get_by_role("menuitem")
    s.cap_souple("09-menu-fichier", [(plus, "Plus"), (mi.filter(has_text="Télécharger").first, "Télécharger"),
                                     (mi.filter(has_text="Renommer").first, "Renommer"),
                                     (mi.filter(has_text="Remove from knowledge").first, "Remove from knowledge")])
    s.note("menu du fichier : " + " | ".join(i.inner_text().strip() for i in p.get_by_role("menuitem").all()))
    p.keyboard.press("Escape")
    s.aller("/workspace/knowledge")
    ligne = p.get_by_role("link", name=NOM).first.locator("xpath=ancestor::*[.//button[@aria-label=\"Plus d'options\"]][1]")
    plus = ligne.locator("button[aria-label=\"Plus d'options\"]").first
    plus.click(); p.wait_for_timeout(800)
    mi = p.get_by_role("menuitem")
    s.cap_souple("10-menu-base", [(plus, "Plus d'options"), (mi.filter(has_text="Accès").first, "Accès"),
                                  (mi.filter(has_text="Exporter").first, "Exporter"),
                                  (mi.filter(has_text="Supprimer").first, "Supprimer")])
    s.note("menu de la base : " + " | ".join(i.inner_text().strip() for i in p.get_by_role("menuitem").all()))
    p.keyboard.press("Escape")



def verifications(s):
    """Sur une base d'essai jetable : options de visibilité, retrait d'un fichier, confirmation de suppression."""
    p = s.page
    s.aller("/workspace/knowledge")
    p.get_by_role("button", name="Créer", exact=True).first.click()
    p.get_by_placeholder("Nommez votre base de connaissances").fill("Essai à supprimer")
    p.get_by_placeholder("Décrivez votre base de connaissances et vos objectifs").fill("Base jetable")
    vis = p.get_by_role("button", name=re.compile("^Visibilité"))
    vis.click(); p.wait_for_timeout(600)
    p.screenshot(path="/depot/donnees/exploration/visibilite.png")
    vis.click(); p.wait_for_timeout(300)
    p.get_by_role("button", name="Avancé").click(); p.wait_for_timeout(600)
    s.note("Avancé : " + p.get_by_role("dialog").last.inner_text()[-600:].replace("\n", " | "))
    p.get_by_role("button", name="Créer une connaissance").click()
    p.wait_for_timeout(2500); p.screenshot(path="/depot/donnees/exploration/apres-creer.png")
    p.get_by_placeholder("Nom de la connaissance").wait_for(); p.wait_for_timeout(1000)
    p.get_by_role("button", name="Ajouter du contenu").click(); p.wait_for_timeout(600)
    with p.expect_file_chooser() as fc:
        p.get_by_role("menuitem").filter(has_text=re.compile("Téléverser des fichiers")).first.click()
    fc.value.set_files("/depot/outils/open-webui/essais/note-de-test.md")
    p.locator("button").filter(has_text="note-de-test.md").first.wait_for(); p.wait_for_timeout(4000)
    p.get_by_text("note-de-test.md", exact=True).first.click(); p.wait_for_timeout(1500)
    for onglet in ("Indexed text",):
        b = p.get_by_text(onglet, exact=True).first
        if b.count():
            b.click(); p.wait_for_timeout(1200)
            s.note(f"{onglet} : " + p.locator("main").inner_text()[-400:].replace("\n", " | "))
    ligne = p.locator("button").filter(has_text="note-de-test.md").first
    ligne.locator("xpath=following::button[@aria-label='Plus'][1]").click(); p.wait_for_timeout(600)
    p.get_by_role("menuitem").filter(has_text="Remove from knowledge").first.click(); p.wait_for_timeout(1500)
    dlg = p.get_by_role("dialog")
    s.note(f"retrait : fenêtre de confirmation = {dlg.count() > 0 and dlg.last.is_visible()} ; fichier encore listé = {p.locator('button').filter(has_text='note-de-test.md').count()}")
    s.aller("/workspace/knowledge")
    ligne = p.get_by_role("link", name="Essai à supprimer").first.locator("xpath=ancestor::*[.//button[@aria-label=\"Plus d'options\"]][1]")
    ligne.locator("button[aria-label=\"Plus d'options\"]").first.click(); p.wait_for_timeout(600)
    p.get_by_role("menuitem").filter(has_text="Supprimer").first.click(); p.wait_for_timeout(1000)
    dlg = p.get_by_role("dialog").last
    s.note("suppression : " + dlg.inner_text().replace("\n", " | ")[:300])
    s.cap("11-confirmer-suppression", [(dlg.get_by_role("button", name="Confirmer"), "Confirmer"),
                                       (dlg.get_by_role("button", name="Annuler"), "Annuler")])
    dlg.get_by_role("button", name="Confirmer").click(); p.wait_for_timeout(1500)
    s.note("base d'essai supprimée : " + str(p.get_by_role("link", name="Essai à supprimer").count() == 0))


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([creer, alimenter, apercu, scan_refuse, retirer, verifications], s)
    finally:
        s.fermer()

