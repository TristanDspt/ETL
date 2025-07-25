import csv
import json
import os
import xml.etree.ElementTree as ET

def extract_manager(filename, separateur=None, demander_suppression_ligne=True):
    filetype = os.path.splitext(filename)[1].lower()
    # dans le manager le code est faux, tu demande toujours la suppression des lignes!
    match filetype:
        case ".csv":
            return extract_csv(filename, separateur=separateur, demander_suppression_ligne=True)
        case ".json":
            return extract_json(filename, demander_suppression_ligne=True)
        case ".xml":
            return extract_xml(filename, demander_suppression_ligne=True)
        case _:
            raise ValueError("Type de fichier non supporté")

def extract_csv(filename=None, separateur=";", demander_suppression_ligne=True):
    data = []
    # les 2 lignes ci-dessus sont inutiles car le séparateur est déjà géré l'appel
    # par contre tu ne gère pas le cas du tab 
    if separateur is None:
        separateur = ";"
    try:
        with open(filename, "r", encoding="utf-8") as fichier:
                lire_csv = csv.DictReader(fichier, delimiter=separateur)
                for row in lire_csv:
                    if demander_suppression_ligne:
                        if any(val.strip() for val in row.values()):
                            data.append(row)
                    else:
                        data.append(row)
    except FileNotFoundError:
        print(f"Erreur : fichier {filename} introuvable.")
    return data

def extract_json(filename=None, separateur=None, demander_suppression_ligne=True):
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as fichier:
                lire_json = json.load(fichier)
                if not isinstance(lire_json, list):
                    raise ValueError("Le fichier JSON doit contenir une liste de dictionnaires.")
                for row in lire_json:
                    if demander_suppression_ligne:
                        if any(val.strip() for val in row.values()):
                            data.append(row)
                    else:
                        data.append(row)
    except FileNotFoundError:
        print(f"Erreur : fichier {filename} introuvable.")
    return data

def extract_xml(filename=None, separateur=None, demander_suppression_ligne=True):
    data = []
    # à voir plus tard
    return data

def transform(data_to_transform, remove_col=None):
    if remove_col is None:
        remove_col = []
    for row in data_to_transform:
        for col in remove_col:
            row.pop(col, None)
        # C'est louable de tester la présnce de la colonne
        # mais ce n'est utile, à ce stade tu dois faire confiance aux données
        # que tu as lues
        # si tu veux vraiment tester la présence de la colonne, il faut le faire avant
        if "EmailPromotion" not in row:
            print("Colone absente")
        elif row["EmailPromotion"] == "0":
            row["EmailPromotion"] = "Non" 
        elif row["EmailPromotion"] == "1" or "2": # ce code est incorrect, il faut vérifier la logique
                                                  # un in à la place de == 1 or 2 est plus adapté
                                                  # ou bien si tu veux utiliser un or il fait le faire comme ça
                                                  # row["EmailPromotion"] == "1" or row["EmailPromotion"] == "2":
                                                  # On peut discuter ensemble du cas difficile des OR, la logique 
                                                  # informatique est bien plus rigoureuse que la logique humaine
                                                  
            row["EmailPromotion"] = "Oui"
    return data_to_transform

# l'absence de load_manager est un peu choquante car cela alourdit le code appelant qui doit gérer 
# le chargement de chaque type de fichier séparément
# les avantages de l'extract_manager sont tout aussi présents pour le load_manager
# si tu as l'un, tu as l'autre la cohérence du code est importante
# la meilleure preuve est que tu as reporté le code de chargement dans le fichier TestETL.py
def load_json(data_to_load, filename):
    nom_entree = os.path.splitext(filename)[0].lower()
    nom_sortie = nom_entree + ".json"
    if not data_to_load:
        print("Aucune donnée à écrire.")
        return
    with open (nom_sortie, "w", encoding="utf-8") as fichier:
        json.dump(data_to_load, fichier, indent=4, ensure_ascii=False)
    # A quoi sert la ligne suivante ?
    # elle n'est pas nécessaire car tu as déjà écrit les données dans le fichier
    # il serait plus logique de retourner le nom du fichier écrit ou un booléen indiquant que le traitement
    # s'est bien déroulé. A condition bien sur que tu retourne 0 si le fichier n'a pas été écrit.
    return data_to_load

def load_csv(data_to_load, filename):
    nom_entree = os.path.splitext(filename)[0].lower()
    nom_sortie = nom_entree + ".csv"
    if not data_to_load:
        print("Aucune donnée à écrire.")
        return
    with open (nom_sortie, "w", encoding="utf-8", newline="") as fichier:
        writer = csv.DictWriter(fichier, delimiter=",", fieldnames=data_to_load[0].keys())
        writer.writeheader()
        for row in data_to_load:
            writer.writerow(row)
    return data_to_load

def load_xml(data_to_load, filename):
    nom_entree = os.path.splitext(filename)[0].lower()
    nom_sortie = nom_entree + ".xml"
    if not data_to_load:
        print("Aucune donnée à écrire.")
        return
    root = ET.Element("données")
    for row in data_to_load:
        item = ET.SubElement(root, "ligne")
        for cle, valeur in row.items():
            champ = ET.SubElement(item, cle)
            champ.text = valeur

    arbre = ET.ElementTree(root)
    arbre.write(nom_sortie, encoding="utf-8", xml_declaration=True)