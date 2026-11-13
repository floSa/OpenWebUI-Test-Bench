# Banc Open WebUI — sans-reflexion — 2026-11-13T15:23:11

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
| juge_llm_oui | 37 |
| juge_llm_sur | 38 |
| erreurs | 0 |
| latence_p50_s | 1.29 |
| latence_p95_s | 3.09 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '4/4', 'anglais': '2/2', 'multi-documents': '3/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-webui': 1571, 'rag-docling-serve': 1971, 'llm-central': 722, 'llm-swap': 5262, 'llm-speaches': 1309} |
| pic_ram_application_mo | 3542 |
| vram | 9652 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 0.0 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 1.68 | Le chiffre d'affaires de Vélanor pour l'année 2025 s'élève à **48,6 M€** [3]. Ce |
| Q02 | fait simple | oui | True | True | 1.01 | Vélanor a été fondée en **2014** [1]. |
| Q03 | fait simple | oui | True | True | 1.24 | La présidente de Vélanor est **Hélène Marchais** [1]. Elle dirige l'entreprise d |
| Q04 | fait simple | oui | True | True | 1.15 | Selon le document [1], le siège social de l'entreprise Vélanor est situé au **12 |
| Q05 | tableau | oui | True | True | 13.11 | Selon les données du rapport annuel, le chiffre d'affaires était de 48,6 M€, ave |
| Q06 | tableau | oui | True | True | 1.29 | Le chiffre d'affaires du troisième trimestre (T3) 2025 a été de **14,2 millions  |
| Q07 | tableau | oui | True | True | 1.19 | 15 400 unités du modèle Sèvre Trail ont été produites en 2025 [1]. |
| Q08 | tableau | oui | True | True | 1.49 | Le prix public TTC du modèle **Erdre Cargo** est de **4 290 €**.  Cette informat |
| Q09 | tableau | oui | True | True | 1.02 | Selon les données fournies, il y a **97 salariés** au sein du site de Cholet [1] |
| Q10 | fait simple | oui | True | True | 0.97 | La part d'aluminium recyclé dans les cadres est de **82 %** [1]. |
| Q11 | fait simple | oui | True | True | 1.15 | Le taux de recyclage des batteries usagées collectées atteint **96 %**. Cet obje |
| Q12 | tableau | oui | True | True | 1.02 | Le fournisseur des moteurs est **Motodrive Co.** [2], qui est installé au **Taïw |
| Q13 | tableau | oui | True | True | 1.34 | En 2025, le résultat net de Vélanor s'est élevé à **3,1 M€**, soit une augmentat |
| Q14 | fait simple | oui | True | True | 1.03 | Le taux de retour sous garantie s'établit à **1,8 %** des vélos vendus [1]. |
| Q15 | scan | oui | True | True | 2.16 | Le prix unitaire des batteries dans le contrat d'approvisionnement signé avec Ba |
| Q16 | scan | oui | True | True | 3.09 | Le délai de livraison prévu pour l'achat des batteries auprès du fournisseur Bat |
| Q17 | scan | oui | True | True | 1.09 | Le contrat stipule que le montant des pénalités de retard est plafonné à **8 %** |
| Q18 | scan | oui | True | True | 1.17 | Le contrat d'approvisionnement n° BX-2025-117 prévoit un volume minimal annuel d |
| Q19 | fait simple | oui | True | True | 1.45 | Les batteries doivent être stockées entre **10 °C et 25 °C** [1]. De plus, en ca |
| Q20 | fait simple | oui | True | True | 1.33 | La responsabilité de la procédure de charge et de stockage des batteries (Procéd |
| Q21 | tableau | oui | True | True | 1.27 | Selon la procédure PR-SEC-04, le local B2 doit être inspecté **le premier lundi  |
| Q22 | fait simple | oui | True | True | 2.13 | Le prix public TTC du modèle Vilaine Compact est de **2 490 €**, comme annoncé l |
| Q23 | fait simple | oui | True | True | 1.13 | La capacité prévue de l'usine de Saint-Nazaire est de **25 000 vélos par an** [1 |
| Q24 | tableau | oui | True | True | 1.89 | D'après le tableau des stocks disponibles dans le contexte [1], il reste **1 240 |
| Q25 | fait simple | oui | True | True | 0.92 | La durée de garantie du cadre est de **7 ans** [1]. |
| Q26 | fait simple | oui | True | True | 1.28 | Le numéro de téléphone du service après-vente est le **02 40 00 12 34** [1]. Ce  |
| Q27 | fait simple | oui | True | True | 1.36 | Selon les décisions communales, la **prime d'intéressement pour 2025** est fixée |
| Q28 | anglais | oui | True | True | 1.09 | Batterix obtained an overall score of **87 out of 100** at the supplier quality  |
| Q29 | anglais | oui | True | True | 1.24 | Selon l'audit de qualité fournisseur effectué chez Batterix GmbH en juin 2025, l |
| Q30 | multi-documents | oui | True | True | 1.78 | Le délai de livraison contractuel établi par le contrat avec Batterix GmbH est d |
| Q31 | multi-documents | oui | True | True | 2.06 | Batterix GmbH a obtenu un **score de 87 sur 100** à l'audit de qualité réalisé l |
| Q32 | multi-documents | oui | True | True | 1.56 | Vélanor vise un chiffre d'affaires de **55 M€** en 2026 [1]. Une seconde usine d |
| Q33 | audio | oui | False | True | 1.66 | La ligne d'assemblage arrêtée est la **ligne numéro 3 de l'usine de Nantes**. El |
| Q34 | audio | oui | True | True | 1.04 | Le directeur de production chez Vélanor est Julien Moreau, selon un message voca |
| Q35 | piège | oui | True | - | 1.54 | D'après les informations fournies, il n'est pas possible de connaître le chiffre |
| Q36 | piège | oui | True | - | 1.81 | La information sur l'identité du directeur financier de Vélanor n'est pas présen |
| Q37 | piège | oui | True | - | 3.58 | D'après le contexte fourni, Vélanor n'a vendu **aucune** trottinette électrique  |
| Q38 | piège | oui | True | - | 1.84 | D'après les informations disponibles dans le contexte fourni, le salaire exact d |
