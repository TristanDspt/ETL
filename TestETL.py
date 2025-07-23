import clsETL

chemin = input("Chemin du fichier CSV : ").lower().strip()
demander_suppression_ligne = input("Voulez vous supprimer les lignes vides ? o/n : ").lower().strip()
suppression = demander_suppression_ligne == "o"

donnee_lue = clsETL.extract(filename=chemin, demander_suppression_ligne=suppression)
donnee_transforme = clsETL.transform(donnee_lue)
donnee_chargee = clsETL.load(donnee_transforme, filename=chemin)

def choix_format_extract():
    print("Choisissez le format d'enregistrement :")
    print("1 - CSV")
    print("2 - JSON")
    print("3 - XML")
    choix = input("Votre choix : ")

    if choix == "1":
        clsETL.load_manager(data, filename, "csv")
    elif choix == "2":
        clsETL.load_manager(data, filename, "json")
    elif choix == "3":
        clsETL.load_manager(data, filename, "xml")
    else:
        print("Format non supporté.")