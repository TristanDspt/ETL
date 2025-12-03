from clsETL import extract_manager, transform, load_manager
import os

# === Chargement ===
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

# === Extraction ===
donnee_lue = extract_manager(filename=chemin, separateur=separateur, demander_suppression_ligne=suppression)

# === Contrôle des erreurs ===
if donnee_lue is None:
    print("Erreur critique : impossible de lire le fichier.")
    exit()
if not donnee_lue:  # liste vide
    print("Le fichier est vide ou toutes les lignes ont été supprimées.")
    exit()

# === Transformation ===
colonnes_a_supprimer = ["rowguid", "AdditionalContactInfo", "Demographics"]
donnee_transforme = transform(donnee_lue, remove_col=colonnes_a_supprimer)

# === Choix du format de sortie ===
print("Choisissez le format d'enregistrement :")
print("1 - CSV")
print("2 - JSON")
print("3 - XML")
choix = input("Votre choix : ").strip()

# === Chargement ===
load_manager(data_to_load=donnee_transforme, filename=chemin, choix=choix)