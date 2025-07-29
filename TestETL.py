from clsETL import extract_manager, transform, load_manager
import os

chemin = input("Chemin du fichier CSV : ").lower().strip()
filetype = os.path.splitext(chemin)[1].lower()
separateur = None
if filetype == ".csv":
    choix_sep = input("Séparateur utilisé (';' par defaut, TAB pour tabulation) : ").lower()
    if choix_sep in ("", ";"):
        separateur = ";"
    elif choix_sep == "tab":
        separateur = "\t"
    elif len(choix_sep) == 1:
        separateur = choix_sep
    else:
        print("Séparateur non reconnu, utilisation de ';' par défaut.")
        separateur = ";"

demander_suppression_ligne = input("Voulez vous supprimer les lignes vides ? o/n : ").lower().strip()

suppression = demander_suppression_ligne == "o"

donnee_lue = extract_manager(filename=chemin, separateur=separateur, demander_suppression_ligne=suppression)

colonnes_a_supprimer = ["rowguid", "AdditionalContactInfo", "Demographics"]

donnee_transforme = transform(donnee_lue, remove_col=colonnes_a_supprimer)

print("Choisissez le format d'enregistrement :")
print("1 - CSV")
print("2 - JSON")
print("3 - XML")
choix = input("Votre choix : ").lower().strip()

load_manager(data_to_load=donnee_transforme, filename=chemin, choix=choix)