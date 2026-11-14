# Banc Open WebUI — serre — 2026-11-13T15:05:17

| Mesure | Valeur |
|---|---|
| questions | 38 |
| exactes | 32 |
| sur | 34 |
| refus_corrects | 4 |
| pieges | 4 |
| citation_bon_document | 34 |
| citation_bonne_page | 21 |
| citations_avec_page | 24 |
| juge_llm_oui | 34 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 17.09 |
| latence_p95_s | 71.08 |
| par_type | {'tableau': '9/10', 'fait simple': '13/13', 'scan': '4/4', 'anglais': '2/2', 'multi-documents': '2/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-webui': 1571, 'rag-docling-serve': 1971, 'llm-central': 724, 'llm-swap': 5300, 'llm-speaches': 1315} |
| pic_ram_application_mo | 3542 |
| vram | 9652 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 0.0 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | non | False | True | 54.83 | D'après le contexte fourni, le chiffre d'affaires spécifique de l'année 2025 pou |
| Q02 | fait simple | oui | True | True | 16.91 | Vélanor a été fondée en 2014 [1]. |
| Q03 | fait simple | oui | True | True | 23.91 | La présidente de Vélanor est Hélène Marchais [1]. |
| Q04 | fait simple | oui | True | True | 16.03 | L'adresse du siège de Vélanor est située au 12 quai de la Fosse, à Nantes [1]. |
| Q05 | tableau | oui | True | True | 12.27 | Au 31 décembre 2025, Vélanor compte 412 salariés [1]. |
| Q06 | tableau | oui | True | True | 19.87 | Le chiffre d'affaires du troisième trimestre 2025 s'est élevé à 14,2 M€ [1]. |
| Q07 | tableau | oui | True | True | 26.63 | Le modèle Sèvre Trail a produit 15 400 unités en 2025 [1]. |
| Q08 | tableau | oui | True | True | 15.0 | Le prix public TTC du modèle Erdre Cargo est de 4 290 € [1]. |
| Q09 | tableau | oui | True | True | 17.08 | D'après la table d'effectif par site, le nombre de salariés travaillant sur le s |
| Q10 | fait simple | oui | True | True | 13.43 | Selon le contexte, les cadres sont fabriqués à partir d'aluminium recyclé à 82 % |
| Q11 | fait simple | oui | True | True | 15.7 | Selon le contexte fourni, le taux de recyclage des batteries usagées collectées  |
| Q12 | tableau | oui | True | True | 22.3 | Selon le contexte, le fournisseur qui livre les moteurs est **Motodrive Co.**, e |
| Q13 | tableau | oui | True | True | 17.09 | En 2025, Vélanor a dégagé un résultat net de 3,1 M€ [1]. |
| Q14 | fait simple | oui | True | True | 10.58 | Selon les chiffres clés de 2025 présentés dans le contexte, le taux de retour so |
| Q15 | scan | oui | True | True | 25.31 | Selon le contrat d'approvisionnement N° BX-2025-117, le prix unitaire des batter |
| Q16 | scan | oui | True | True | 22.6 | Le délai de livraison prévu par le contrat Batterix est de 21 jours après la com |
| Q17 | scan | oui | True | True | 16.08 | Selon le contrat d'approvisionnement, le plafond des pénalités de retard s'élève |
| Q18 | scan | oui | True | True | 13.97 | Le contrat d'approvisionnement prévu avec Batterix prévoit un volume minimal ann |
| Q19 | fait simple | oui | True | True | 22.77 | Selon le document de référence [1], les batteries doivent être stockées entre 10 |
| Q20 | fait simple | oui | True | True | 21.09 | Selon la procédure PR-SEC-04, le responsable de la charge et du stockage des bat |
| Q21 | tableau | oui | True | True | 15.21 | Selon les informations fournies dans le contexte, le local B2 est inspecté **le  |
| Q22 | fait simple | oui | True | True | 16.13 | Le prix public du modèle Vilaine Compact est de 2 490 € TTC [1]. |
| Q23 | fait simple | oui | True | True | 14.01 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an [1]. |
| Q24 | tableau | oui | True | True | 19.59 | Selon les données fournies dans la table de référence, le stock actuel des batte |
| Q25 | fait simple | oui | True | True | 18.89 | Selon le document fourni, la durée de garantie du cadre est de 7 ans [1]. |
| Q26 | fait simple | oui | True | True | 21.03 | Le numéro de téléphone du service après-vente est 02 40 00 12 34 [1]. |
| Q27 | fait simple | oui | True | True | 10.02 | Selon les décisions présentées, le montant de la prime d'intéressement 2025 est  |
| Q28 | anglais | oui | True | True | 12.9 | Batterix obtained an overall score of 87 out of 100 at the supplier audit [1]. |
| Q29 | anglais | oui | True | True | 11.23 | Selon le rapport d'audit de qualité, le taux de cellules défectueuses mesuré che |
| Q30 | multi-documents | non | False | True | 53.64 | Le délai de livraison contractuel avec Batterix est de **21 jours après la comma |
| Q31 | multi-documents | oui | True | True | 14.9 | Selon les documents fournis :  - Le score de Batterix à l'audit est de **87 sur  |
| Q32 | multi-documents | oui | True | True | 21.91 | Vélanor vise un chiffre d'affaires de 55 M€ en 2026 [1]. Elle prévoit également  |
| Q33 | audio | oui | False | True | 94.38 | Selon les informations fournies, la **ligne d'assemblage numéro 3 de Nantes** se |
| Q34 | audio | oui | True | True | 10.11 | Selon les informations fournies, Julien Moreau est le directeur de production ch |
| Q35 | piège | oui | True | - | 98.33 | Selon le contexte fourni, aucune information spécifique concernant le chiffre d' |
| Q36 | piège | oui | True | - | 71.08 | D'après le document fourni, il n'est pas mentionné de nom pour le directeur fina |
| Q37 | piège | oui | False | - | 71.08 | D'après le contexte fourni, il n'y a aucune information sur le nombre de trottin |
| Q38 | piège | oui | True | - | 40.83 | D'après les documents fournis, il n'est pas possible de connaître le salaire exa |
