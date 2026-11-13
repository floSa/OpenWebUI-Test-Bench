# Banc Open WebUI — docling-rerank — 2026-11-13T14:01:19

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 34 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 34 |
| citation_bonne_page | 22 |
| citations_avec_page | 24 |
| juge_llm_oui | 36 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 58.27 |
| latence_p95_s | 114.69 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '4/4', 'anglais': '2/2', 'multi-documents': '3/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-webui': 1595, 'rag-docling-serve': 2393, 'llm-central': 729, 'llm-swap': 5365, 'llm-speaches': 1364} |
| pic_ram_application_mo | 3988 |
| vram | 9667 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 50.9 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | False | True | 53.38 | Selon les données disponibles dans le rapport annuel 2025 de Vélanor, le chiffre |
| Q02 | fait simple | oui | True | True | 54.38 | Selon les informations fournies, Vélanor a été fondée en 2014 [1]. |
| Q03 | fait simple | oui | True | True | 81.06 | La présidente de Vélanor est Hélène Marchais [1]. |
| Q04 | fait simple | oui | True | True | 56.03 | L'adresse du siège de Vélanor est le 12 quai de la Fosse, à Nantes [1]. |
| Q05 | tableau | oui | True | True | 68.12 | Selon les données disponibles, Vélanor compte **412 salariés** au 31 décembre 20 |
| Q06 | tableau | oui | False | True | 108.68 | Selon les données du rapport annuel fourni, le chiffre d'affaires enregistré pou |
| Q07 | tableau | oui | True | True | 55.76 | Selon les données de production par modèle, 15 400 unités du modèle Sèvre Trail  |
| Q08 | tableau | oui | True | True | 57.98 | Le prix public TTC du modèle Erdre Cargo est de 4 290 € [1]. |
| Q09 | tableau | oui | True | True | 80.23 | Selon les informations du rapport annuel, il y a 97 salariés au site de Cholet [ |
| Q10 | fait simple | oui | True | True | 79.8 | La part d'aluminium recyclé dans les cadres est de 82 % [1]. |
| Q11 | fait simple | oui | True | True | 40.45 | Selon les informations fournies, le taux de recyclage des batteries usagées coll |
| Q12 | tableau | oui | True | True | 58.27 | Le fournisseur des moteurs est **Motodrive Co.**, qui est installé au **Taïwan** |
| Q13 | tableau | oui | True | True | 64.21 | En 2025, Vélanor a dégagé un résultat net de 3,1 M€ [1]. |
| Q14 | fait simple | oui | True | True | 46.0 | Le taux de retour sous garantie s'établit à 1,8 % des vélos vendus [1]. |
| Q15 | scan | oui | True | True | 94.7 | Le prix unitaire des batteries prévu par le contrat avec Batterix est de 212 eur |
| Q16 | scan | oui | True | True | 29.95 | Selon le contrat d'approvisionnement n° BX-2025-117, la livraison prévue par Bat |
| Q17 | scan | oui | True | True | 63.01 | Le plafond des pénalités de retard est fixé à **8 % du montant de la commande**  |
| Q18 | scan | oui | True | True | 69.02 | Le contrat d'approvisionnement entre Vélanor SAS et Batterix GmbH précise dans s |
| Q19 | fait simple | oui | True | True | 46.91 | Les batteries doivent être stockées entre 10 °C et 25 °C [1]. |
| Q20 | fait simple | oui | True | True | 24.19 | Selon le document PR-SEC-04 — Charge et stockage des batteries, la procédure de  |
| Q21 | tableau | oui | True | True | 71.67 | D'après les contrôles établis dans le document, le local B2 est inspecté le prem |
| Q22 | fait simple | oui | True | True | 49.6 | Selon le document, le prix public du modèle Vilaine Compact est de 2 490 € TTC [ |
| Q23 | fait simple | oui | True | True | 50.81 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an [1]. |
| Q24 | tableau | oui | True | True | 60.14 | Le stock actuel de batteries BAT-48V-14Ah est de **1 240 unités** [1], tandis qu |
| Q25 | fait simple | oui | True | True | 27.21 | Selon les informations fournies, la durée de garantie du cadre est de 7 ans [1]. |
| Q26 | fait simple | oui | True | True | 76.85 | Le numéro de téléphone du service après-vente est le 02 40 00 12 34 [1]. |
| Q27 | fait simple | oui | True | True | 59.69 | Selon les documents fournis, le montant de la prime d'intéressement 2025 est fix |
| Q28 | anglais | oui | True | True | 37.51 | According to the Supplier Quality Audit document for Batterix GmbH, the overall  |
| Q29 | anglais | oui | True | True | 50.76 | D'après le rapport d'audit de qualité fournisseur concernant Batterix GmbH, le t |
| Q30 | multi-documents | oui | True | True | 48.14 | Selon le contrat d'approvisionnement (Article 5), le délai de livraison contract |
| Q31 | multi-documents | oui | True | True | 35.38 | Selon l'audit qualité, Batterix a obtenu un score de 87 sur 100 [1]. Le contrat  |
| Q32 | multi-documents | oui | True | True | 90.09 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 et prévoit 70 embauches à Sa |
| Q33 | audio | oui | True | True | 114.69 | D'après le contexte fourni, la ligne d'assemblage numéro 3 de Nantes sera arrêté |
| Q34 | audio | oui | True | True | 42.36 | Le directeur de production de Vélanor est Julien Moreau [1]. |
| Q35 | piège | oui | True | - | 118.4 | D'après le contexte fourni, aucune information ne concerne spécifiquement le chi |
| Q36 | piège | oui | True | - | 121.59 | D'après les documents fournis, le directeur financier de Vélanor n'est pas ident |
| Q37 | piège | oui | True | - | 101.22 | D'après le contexte fourni, Vélanor a produit et vendu **61 800 vélos à assistan |
| Q38 | piège | oui | True | - | 78.77 | D'après le contexte fourni, il n'est pas possible de préciser le salaire de Kari |
