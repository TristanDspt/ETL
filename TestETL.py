import clsETL

chemin = input("Chemin du fichier CSV : ").lower().strip()
demander_suppression_ligne = input("Voulez vous supprimer les lignes vides ? o/n : ").lower().strip()
suppression = demander_suppression_ligne == "o"

donnee_lue = clsETL.extract(filename=chemin, demander_suppression_ligne=suppression)
donnee_transforme = clsETL.transform(donnee_lue)
donnee_chargee = clsETL.load(donnee_transforme, filename=chemin)
