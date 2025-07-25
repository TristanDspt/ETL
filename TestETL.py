import clsETL
import os

chemin = input("Chemin du fichier CSV : ").lower().strip()
filetype = os.path.splitext(chemin)[1].lower()
separateur = None
if filetype == ".csv":
    choix_sep = input("Séparateur utilisé (';' par defaut, TAB pour tabulation) : ").lower()
    if choix_sep in ("", ";"):
        separateur = ";"
    elif choix_sep == "tab":
        #La gestion du tab est à reporter dans le code de clsETL.py
        # car c'est une fonctionnalité de l'extract_manager d'autant que si tu te mets à gérer d'autres séparateurs
        # spéciaux, tu vas devoir modifier le code à chaque fois.
        separateur = "\t"
    elif len(choix_sep) == 1:
        separateur = choix_sep
    else:
        print("Séparateur non reconnu, utilisation de ';' par défaut.")
        separateur = ";"

demander_suppression_ligne = input("Voulez vous supprimer les lignes vides ? o/n : ").lower().strip()

suppression = demander_suppression_ligne == "o"

donnee_lue = clsETL.extract_manager(filename=chemin, separateur=separateur, demander_suppression_ligne=suppression)

colonnes_a_supprimer = ["rowguid", "AdditionalContactInfo", "Demographics"]

donnee_transforme = clsETL.transform(donnee_lue, remove_col=colonnes_a_supprimer)

# d'un point de vue formel, le bloc avant le match est à déplacer dans la section ou tu interroge l'utilisateur
# pour toutes les données que tu lui demande. 
# cela devrait d'ailleurs être dans une fonction qui retournerai la liste des valeurs saisies
# comme cela si un jour on décide de mettre en place une vraie interface graphique,
# on pourra facilement adapater le code
print("Choisissez le format d'enregistrement :")
print("1 - CSV")
print("2 - JSON")
print("3 - XML")
choix = input("Votre choix : ")
match choix:
    case "1":
        clsETL.load_csv(donnee_transforme, filename=chemin)
    case "2":
        clsETL.load_json(donnee_transforme, filename=chemin)
    case "3":
        clsETL.load_xml(donnee_transforme, filename=chemin)
    case _:
        print("Format non supporté.")