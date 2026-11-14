"""Chapitre 08 : régler la lecture des documents (Docling, découpage, recherche hybride, reranker `rerank`)."""
import os, re
from ui import Scenario, etapes

CH = "08-regler-la-lecture-des-documents"
CLE = os.environ.get("LLM_CENTRAL_KEY", "")


def selecteur(p, libelle):
    """Liste déroulante située après le libellé `libelle` (texte exact)."""
    return p.get_by_text(libelle, exact=True).filter(visible=True).first.locator("xpath=following::select[1]")


def champ_apres(p, libelle):
    return p.get_by_text(libelle, exact=True).filter(visible=True).first.locator("xpath=following::input[1]")


def extraction(s):
    s.reglages("admin:documents")
    extraction_sans_ouvrir(s)


def extraction_sans_ouvrir(s):
    p = s.page
    moteur = selecteur(p, "Moteur d'extraction de contenu")
    s.cap("01-documents", [(s.onglet("Documents", admin=True), "Documents"), (moteur, "Moteur d'extraction de contenu")])
    moteur.select_option(label="Docling"); p.wait_for_timeout(1000)
    url = p.get_by_placeholder(re.compile("docling|URL", re.I)).filter(visible=True).first
    s.note("après choix Docling : " + p.get_by_role("dialog").last.inner_text()[:900].replace("\n", " | "))
    url.fill("http://rag-docling-serve:5001")
    s.cap_souple("02-docling", [(moteur, "Docling"), (url, "URL du serveur Docling")])


def decoupage(s):
    p = s.page
    s.cap_souple("03-decoupage", [(selecteur(p, "Découpage du texte"), "Découpage du texte"),
                                  (champ_apres(p, "Taille des chunks"), "Taille des chunks"),
                                  (champ_apres(p, "Chevauchement des chunks"), "Chevauchement des chunks"),
                                  (champ_apres(p, "Modèle d'embedding"), "Modèle d'embedding")])


def extraction_seule(s):
    """Reprise des captures 01 et 02 sans enregistrer (l'instance est déjà réglée sur Docling)."""
    p = s.page
    s.reglages("admin:documents")
    selecteur(p, "Moteur d'extraction de contenu").select_option(label="Par défaut"); p.wait_for_timeout(800)
    extraction_sans_ouvrir(s)
    p.keyboard.press("Escape"); p.wait_for_timeout(500)


def zone_danger(s):
    """Bouton « Réindexer » (bas de l'onglet Documents), montré sans être cliqué."""
    p = s.page
    s.reglages("admin:documents")
    titre = p.get_by_text("Réindexer les vecteurs", exact=True).filter(visible=True).first
    titre.evaluate("e => e.scrollIntoView({block: 'center'})"); p.wait_for_timeout(600)
    btn = titre.locator("xpath=following::button[1]")
    s.cap_souple("07-reindexer", [(p.get_by_text("Zone de danger", exact=True).first, "Zone de danger"), (btn, "Réindexer")])
    p.keyboard.press("Escape")


def requetes(s):
    """Génération des requêtes de RAG (Interface utilisateur › Tâches) : désactivée, réponses deux fois plus rapides au banc.
    Montrée dans l'état désactivé, déjà enregistré par le banc « taches » ; rien n'est enregistré ici."""
    p = s.page
    s.reglages("admin:interface")
    lib = p.get_by_text("Génération de requête de RAG", exact=True).filter(visible=True).first
    lib.evaluate("e => e.scrollIntoView({block: 'center'})"); p.wait_for_timeout(600)
    inter = lib.locator("xpath=following::*[@role='switch'][1]")
    s.note("interrupteur génération de requête de RAG : " + str(inter.get_attribute("aria-checked")))
    s.cap_souple("08-requetes", [(s.onglet("Interface utilisateur", admin=True), "Interface utilisateur"), (lib, "Génération de requête de RAG"),
                                 (inter, "interrupteur"), (s.bouton("Enregistrer", exact=True).filter(visible=True).last, "Enregistrer")])
    p.keyboard.press("Escape")


def decoupage_seul(s):
    """Reprise de la capture 03 sans rien modifier : la liste « Découpage du texte » doit rester dans le cadre."""
    p = s.page
    s.reglages("admin:documents")
    titre = p.get_by_text("Découpage du texte", exact=True).filter(visible=True).first
    titre.scroll_into_view_if_needed(); p.wait_for_timeout(300)
    titre.evaluate("e => e.scrollIntoView({block: 'start'})"); p.wait_for_timeout(500)
    decoupage(s)


def recherche(s):
    p = s.page
    d = p.get_by_role("dialog").last
    hyb = p.get_by_text("Recherche hybride", exact=True).filter(visible=True).first
    hyb.scroll_into_view_if_needed()
    inter = hyb.locator("xpath=following::*[@role='switch'][1]")
    if inter.get_attribute("aria-checked") != "true":
        inter.click(); p.wait_for_timeout(1000)
    s.note("après hybride : " + d.inner_text().split("Récupération")[-1][:1200].replace("\n", " | "))
    moteur = selecteur(p, "Moteur de ré-ranking")
    try:
        moteur.select_option(label="Externe")
    except Exception:
        s.note("options du moteur : " + moteur.inner_text().replace("\n", " | "))
        moteur.select_option(index=1)
    p.wait_for_timeout(1000)
    zone = p.get_by_text("Moteur de ré-ranking", exact=True).filter(visible=True).first
    url = zone.locator("xpath=following::input[1]")
    cle = zone.locator("xpath=following::input[2]")
    url.fill("http://llm-central:8080/v1/rerank")
    cle.fill(CLE)
    modele = champ_apres(p, "Modèle de ré-ranking")
    modele.fill("rerank")
    s.note("champs rerank : " + d.inner_text().split("Recherche hybride")[-1][:900].replace("\n", " | "))
    zone.scroll_into_view_if_needed(); p.wait_for_timeout(500)
    s.cap_souple("04-reranker", [(inter, "Recherche hybride"), (moteur, "Moteur de ré-ranking"), (url, "URL"),
                                 (cle, "Clé API (masquée)"), (modele, "Modèle de ré-ranking"),
                                 (champ_apres(p, "Top K Reranker"), "Top K Reranker")])


def enregistrer(s):
    p = s.page
    enr = s.bouton("Enregistrer", exact=True).filter(visible=True).last
    enr.click(); p.wait_for_timeout(1500)
    toast = p.locator("[data-sonner-toast]").first
    s.note("enregistrement : " + (toast.inner_text() if toast.count() else "aucun message"))
    s.cap_souple("05-enregistre", [(enr, "Enregistrer"), (toast, "message")])


def reglages_documents(s):
    extraction(s); decoupage(s); recherche(s); enregistrer(s)


def scan(s):
    """Le contrat scanné, refusé au chapitre 05, est maintenant lu par Docling."""
    p = s.page
    s.aller("/workspace/knowledge")
    p.get_by_role("link", name="Démo Vélanor").first.click()
    p.get_by_placeholder("Nom de la connaissance").wait_for(); p.wait_for_timeout(1000)
    p.get_by_role("button", name="Ajouter du contenu").click(); p.wait_for_timeout(800)
    with p.expect_file_chooser() as fc:
        p.get_by_role("menuitem").filter(has_text=re.compile("Téléverser des fichiers")).first.click()
    fc.value.set_files("/depot/banc-essai/corpus/documents/contrat-batterix-scan.pdf")
    ligne = p.locator("button").filter(has_text="contrat-batterix-scan.pdf").first
    ligne.wait_for(timeout=120000)
    for _ in range(90):
        if not p.locator(".animate-spin").count():
            break
        p.wait_for_timeout(1000)
    toast = p.locator("[data-sonner-toast]").first
    s.note("ajout du scan : " + (toast.inner_text() if toast.count() else "aucun message"))
    s.sans_toasts()
    scan_affichage(s, deja=True)


def scan_affichage(s, deja=False):
    p = s.page
    if not deja:
        s.aller("/workspace/knowledge")
        p.get_by_role("link", name="Démo Vélanor").first.click()
        p.get_by_placeholder("Nom de la connaissance").wait_for(); p.wait_for_timeout(1000)
    ligne = p.locator("button").filter(has_text="contrat-batterix-scan.pdf").first
    p.get_by_text("contrat-batterix-scan.pdf", exact=True).first.click(); p.wait_for_timeout(2000)
    idx = p.get_by_text("Indexed text", exact=True).first
    idx.click(); p.wait_for_timeout(1500)
    s.note("texte indexé du scan : " + p.locator("main").inner_text()[-700:].replace("\n", " | "))
    s.cap_souple("06-scan-lu", [(ligne, "contrat-batterix-scan.pdf"), (idx, "Indexed text"),
                                (p.get_by_text(re.compile("Batterix")).last, "texte reconnu")])


if __name__ == "__main__":
    s = Scenario(CH)
    try:
        etapes([reglages_documents, scan, scan_affichage, extraction_seule, decoupage_seul, zone_danger, requetes], s)
    finally:
        s.fermer()
