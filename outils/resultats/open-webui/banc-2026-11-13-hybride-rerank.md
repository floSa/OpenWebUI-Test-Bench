# Banc Open WebUI — hybride-rerank — 2026-11-13T09:59:27

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 28 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 30 |
| citation_bonne_page | 18 |
| citations_avec_page | 18 |
| juge_llm_oui | 32 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 66.16 |
| latence_p95_s | 119.49 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-webui': 1550, 'rag-docling-serve': 897, 'llm-central': 742, 'llm-swap': 5439, 'llm-speaches': 1321} |
| pic_ram_application_mo | 2447 |
| vram | 9890 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 0.0 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 49.46 | Selon les informations fournies, le chiffre d'affaires de Vélanor en 2025 s'élèv |
| Q02 | fait simple | oui | True | True | 42.38 | Selon le document annuel, Vélanor a été fondée en 2014 [1]. |
| Q03 | fait simple | oui | True | True | 52.68 | La présidente de Vélanor est Hélène Marchais [1]. |
| Q04 | fait simple | oui | True | True | 48.29 | L'adresse du siège de Vélanor est située au 12 quai de la Fosse à Nantes [1]. |
| Q05 | tableau | oui | True | True | 66.16 | Selon le rapport annuel de Vélanor SAS pour l'année 2025, l'effectif du groupe s |
| Q06 | tableau | oui | True | True | 84.07 | Le chiffre d'affaires du troisième trimestre 2025 s'est élevé à 14,2 M€ [1]. |
| Q07 | tableau | oui | True | True | 72.08 | Selon la section « Production par modèle » du document, le modèle Sèvre Trail a  |
| Q08 | tableau | oui | True | True | 59.54 | Selon les documents fournis, le prix public TTC du modèle Erdre Cargo est de **4 |
| Q09 | tableau | oui | True | True | 85.54 | Selon le document des effectifs par site, 97 salariés travaillent sur le site de |
| Q10 | fait simple | oui | True | True | 68.14 | La part d'aluminium recyclé dans les cadres est de 82 % [1]. |
| Q11 | fait simple | oui | True | True | 63.06 | Selon les documents fournis, le taux de recyclage des batteries usagées collecté |
| Q12 | tableau | oui | True | True | 89.46 | D'après les informations fournies, le fournisseur des moteurs est **Motodrive Co |
| Q13 | tableau | oui | True | True | 65.85 | Selon les chiffres clés publiés, le résultat net de Vélanor s'est élevé à 3,1 M€ |
| Q14 | fait simple | oui | True | True | 67.92 | Selon le document fourni par Vélanor SAS, le taux de retour sous garantie s’étab |
| Q15 | scan | non | False | False | 89.67 | D'après les documents fournis, le prix unitaire des batteries prévu par le contr |
| Q16 | scan | non | False | False | 71.8 | D'après le tableau des délais moyens constatés pour les fournisseurs, le délai a |
| Q17 | scan | non | False | False | 99.35 | Selon les documents fournis, il n'est pas mentionné le montant spécifique du pla |
| Q18 | scan | non | False | False | 99.97 | D'après les documents fournis, il n'est pas spécifié un volume minimal annuel de |
| Q19 | fait simple | oui | True | True | 53.92 | Selon la procédure PR-SEC-04 relative à la charge et le stockage des batteries [ |
| Q20 | fait simple | oui | True | True | 46.43 | Selon la procédure PR-SEC-04 — Charge et stockage des batteries, le responsable  |
| Q21 | tableau | oui | True | True | 48.3 | Selon la procédure PR-SEC-04, le local B2 est inspecté le premier lundi de chaqu |
| Q22 | fait simple | oui | True | True | 53.9 | Le prix public du modèle Vilaine Compact est de 2 490 € TTC [1]. |
| Q23 | fait simple | oui | True | True | 58.64 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an [1]. |
| Q24 | tableau | oui | True | True | 67.84 | Selon les données de stock disponibles dans le contexte, il reste **1240 unités* |
| Q25 | fait simple | oui | True | True | 69.48 | Selon le document FAQ du service après-vente, la durée de garantie du cadre est  |
| Q26 | fait simple | oui | True | True | 67.81 | Le numéro de téléphone du service après-vente est le 02 40 00 12 34 [1]. |
| Q27 | fait simple | oui | True | True | 53.67 | Le montant de la prime d'intéressement pour l'année 2025 est de **1 150 euros pa |
| Q28 | anglais | oui | True | True | 44.21 | According to the Supplier Quality Audit document for Batterix GmbH, the overall  |
| Q29 | anglais | oui | True | True | 57.35 | Selon le rapport d'audit fournisseur de qualité (Supplier Quality Audit) fourni, |
| Q30 | multi-documents | non | False | True | 119.85 | Selon le document de gestion des fournisseurs, le délai moyen constaté pour les  |
| Q31 | multi-documents | non | False | True | 81.66 | Selon le document d'audit de qualité fourni, le score global obtenu par Batterix |
| Q32 | multi-documents | oui | True | True | 51.13 | Selon les informations disponibles, Vélanor vise un chiffre d'affaires de 55 M€  |
| Q33 | audio | oui | True | True | 109.9 | La ligne d'assemblage numéro 3 de Nantes sera arrêtée pour maintenance du 2 au 6 |
| Q34 | audio | oui | True | True | 42.71 | Le directeur de production de Vélanor est Julien Moreau [2]. |
| Q35 | piège | oui | True | - | 108.96 | D'après les documents fournis, il n'est pas possible de connaître le chiffre d'a |
| Q36 | piège | oui | True | - | 119.49 | D'après les documents fournis, l'identité du directeur financier de Vélanor n'es |
| Q37 | piège | oui | True | - | 179.77 | Les documents fournis ne contiennent aucune information concernant la vente de t |
| Q38 | piège | oui | True | - | 56.3 | D'après le contexte fourni, il n'existe aucune information concernant le salaire |
