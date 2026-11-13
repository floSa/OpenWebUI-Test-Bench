# Banc Open WebUI — defaut-sans-rerank — 2026-11-13T09:08:08

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
| latence_p50_s | 60.14 |
| latence_p95_s | 105.98 |
| par_type | {'tableau': '10/10', 'fait simple': '13/13', 'scan': '0/4', 'anglais': '2/2', 'multi-documents': '1/3', 'audio': '2/2', 'piège': '4/4'} |
| pic_ram_mo | {'rag-open-webui': 1440, 'rag-docling-serve': 902, 'llm-central': 746, 'llm-swap': 5443, 'llm-speaches': 1318} |
| pic_ram_application_mo | 2342 |
| vram | 9436 Mo / 16380 Mo (nvidia-smi, mesuré en fin de banc) |
| indexation_s | 0.0 |

| Id | Type | Exacte | Juge LLM | Doc. cité | Latence (s) | Réponse (début) |
|---|---|---|---|---|---|---|
| Q01 | tableau | oui | True | True | 57.92 | Le chiffre d'affaires de Vélanor en 2025 s'élève à 48,6 M€ [1]. |
| Q02 | fait simple | oui | True | True | 36.12 | Vélanor a été fondée en 2014 [1]. |
| Q03 | fait simple | oui | True | True | 43.92 | La présidente de Vélanor est Hélène Marchais [1]. |
| Q04 | fait simple | oui | True | True | 57.77 | L'adresse du siège de Vélanor est située au 12 quai de la Fosse à Nantes [1]. |
| Q05 | tableau | oui | True | True | 69.22 | Selon le rapport annuel fictif de Vélanor SAS, l'entreprise compte **412 salarié |
| Q06 | tableau | oui | True | True | 48.61 | Le chiffre d'affaires du troisième trimestre 2025 s'est établi à 14,2 M€ [1]. |
| Q07 | tableau | oui | True | True | 77.95 | Selon le rapport annuel de Vélanor SAS, la production du modèle Sèvre Trail s'es |
| Q08 | tableau | oui | True | True | 60.81 | Le prix public TTC du modèle Erdre Cargo est de 4 290 € [1]. |
| Q09 | tableau | oui | True | True | 78.1 | Selon les effectifs par site du document Vélanor SAS, le site de Cholet compte * |
| Q10 | fait simple | oui | True | True | 63.26 | Selon le document de Vélanor SAS, les cadres sont fabriqués à partir d'aluminium |
| Q11 | fait simple | oui | True | True | 59.37 | Le taux de recyclage des batteries usagées collectées atteint 96 % [1]. |
| Q12 | tableau | oui | True | True | 55.32 | Selon les informations fournies, le fournisseur des moteurs est **Motodrive Co.* |
| Q13 | tableau | oui | True | True | 70.58 | D'après le document annuel 2025, Vélanor a dégagé un résultat net de 3,1 M€ en 2 |
| Q14 | fait simple | oui | True | True | 71.1 | Le taux de retour sous garantie s'établit à 1,8 % des vélos vendus [1]. |
| Q15 | scan | non | False | False | 89.51 | D'après les documents fournis, le **prix unitaire des batteries** prévu par le c |
| Q16 | scan | non | False | False | 53.0 | Selon le document fourni, le délai moyen constaté pour les batteries livrées par |
| Q17 | scan | non | False | False | 105.98 | Dans les documents fournis, aucune information n'est disponible concernant le pl |
| Q18 | scan | non | False | False | 98.86 | Dans les documents fournis, aucune information précise sur le volume minimal ann |
| Q19 | fait simple | oui | True | True | 38.09 | Les batteries doivent être stockées entre 10 °C et 25 °C [1]. |
| Q20 | fait simple | oui | True | True | 69.6 | Selon le document de la procédure PR-SEC-04 « Charge et stockage des batteries » |
| Q21 | tableau | oui | True | True | 53.67 | Le local B2 est inspecté le premier lundi de chaque mois [1]. |
| Q22 | fait simple | oui | True | True | 60.14 | Le prix public du modèle Vilaine Compact s'élève à 2 490 € TTC [1]. |
| Q23 | fait simple | oui | True | True | 49.8 | La capacité prévue de l'usine de Saint-Nazaire est de 25 000 vélos par an [2]. |
| Q24 | tableau | oui | True | True | 37.05 | Le stock actuel de batteries **BAT-48V-14Ah** (Batterie 48 V 14 Ah) est de **124 |
| Q25 | fait simple | oui | True | True | 46.65 | Selon les FAQ du service après-vente, le cadre est garanti **7 ans** [1]. La bat |
| Q26 | fait simple | oui | True | True | 55.66 | Le numéro de téléphone du service après-vente est le 02 40 00 12 34 [1]. |
| Q27 | fait simple | oui | True | True | 73.0 | Le montant de la prime d'intéressement pour l'année 2025 est de 1 150 euros par  |
| Q28 | anglais | oui | True | True | 36.7 | At the supplier audit, Batterix GmbH obtained an overall score of 87 out of 100  |
| Q29 | anglais | oui | True | True | 50.68 | Le taux de cellules défectueuses mesuré chez Batterix lors de l'audit est de 0,3 |
| Q30 | multi-documents | non | False | True | 84.09 | D’après le document contenant les données sur les délais moyens constatés [3], l |
| Q31 | multi-documents | non | False | True | 79.18 | Selon le rapport d'audit de qualité fournisseur, Batterix GmbH a obtenu un **sco |
| Q32 | multi-documents | oui | True | True | 54.02 | En 2026, Vélanor vise un chiffre d'affaires de 55 M€ [1]. Par ailleurs, une seco |
| Q33 | audio | oui | True | True | 104.88 | La ligne d'assemblage numéro 3 de Nantes sera arrêtée pour maintenance du 2 au 6 |
| Q34 | audio | oui | True | True | 48.21 | Le directeur de production de Vélanor est Julien Moreau [3]. |
| Q35 | piège | oui | True | - | 110.24 | D'après les documents fournis, il n'est pas possible de déterminer le chiffre d' |
| Q36 | piège | oui | True | - | 80.21 | D’après les documents fournis, aucune information n’est mentionnée concernant le |
| Q37 | piège | oui | True | - | 94.44 | D'après les documents fournis, il n'est pas possible de donner un chiffre précis |
| Q38 | piège | oui | True | - | 110.51 | Selon les documents fournis, il n'est pas possible de déterminer le salaire de K |
