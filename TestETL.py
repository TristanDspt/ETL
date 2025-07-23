import clsETL

chemin = input("Chemin du fichier CSV : ").lower().strip()
demander_suppression_ligne = input("Voulez vous supprimer les lignes vides ? o/n : ").lower().strip()
suppression = demander_suppression_ligne == "o"

donnee_lue = clsETL.extract_manager(filename=chemin, demander_suppression_ligne=suppression)

donnee_transforme = clsETL.transform(donnee_lue)

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