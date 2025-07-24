import csv
import json
import os
import xml.etree.ElementTree as ET

def extract_manager(filename, demander_suppression_ligne=True):
    filetype = os.path.splitext(filename)[1].lower()
    match filetype:
        case ".csv":
            return extract_csv(filename, demander_suppression_ligne=True)
        case ".json":
            return extract_json(filename, demander_suppression_ligne=True)
        case ".xml":
            return extract_xml(filename, demander_suppression_ligne=True)
        case _:
            raise ValueError("Type de fichier non supporté")

def extract_csv(filename=None, separateur=";", demander_suppression_ligne=True):
    data = []
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

def extract_json(filename=None, demander_suppression_ligne=True):
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

def extract_xml(filename=None, separateur=";", demander_suppression_ligne=True):
    data = []
    # à voir plus tard
    return data

def transform(data_to_transform, remove_col=None):
    if remove_col is None:
        remove_col = []
    for row in data_to_transform:
        for col in remove_col:
            row.pop(col, None)
        if "EmailPromotion" not in row:
            print("Colone absente")
        elif row["EmailPromotion"] == "0":
            row["EmailPromotion"] = "Non" 
        elif row["EmailPromotion"] == "1" or "2":
            row["EmailPromotion"] = "Oui"
    return data_to_transform

def load_json(data_to_load, filename):
    nom_entree = os.path.splitext(filename)[0].lower()
    nom_sortie = nom_entree + ".json"
    if not data_to_load:
        print("Aucune donnée à écrire.")
        return
    with open (nom_sortie, "w", encoding="utf-8") as fichier:
        json.dump(data_to_load, fichier, indent=4, ensure_ascii=False)
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