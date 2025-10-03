import csv
import json
import os
import xml.etree.ElementTree as ET

def extract_manager(filename, separateur=None, demander_suppression_ligne=True):
    """
    Gestion des méthodes d'extraction.
    
    Args:
        filename (str): Nom du fichier à lire.
        separateur (str): Caractère séparateur utilisé dans le fichier CSV.
        demander_suppression_ligne (bool): Supprimer les lignes vides si True.
        
    Returns:
        Méthode associée.
    """
    filetype = os.path.splitext(filename)[1].lower()
    try:
        match filetype:
            case ".csv":
                if separateur is None:
                    separateur = ";"
                return extract_csv(filename, separateur, demander_suppression_ligne)
            case ".json":
                return extract_json(filename, demander_suppression_ligne)
            case ".xml":
                return extract_xml(filename, demander_suppression_ligne)
            case _:
                raise ValueError("Type de fichier non supporté")
    except FileNotFoundError:
        print(f"Erreur : fichier {filename} introuvable.")
        return None
    

def extract_csv(filename, separateur, demander_suppression_ligne):
    """
    Extrait un fichier CSV dans une liste de dictionnaires.
    
    Args:
        filename (str): Nom du fichier à lire.
        separateur (str): Caractère séparateur utilisé dans le fichier CSV.
        demander_suppression_ligne (bool): Supprimer les lignes vides si True.

    Returns:
        list of dict: Données extraites sous forme de liste de dictionnaires.
    """
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
        return None
    return data

def extract_json(filename, demander_suppression_ligne):
    """
    Extrait un fichier JSON dans une liste de dictionnaires.
    
    Args:
        filename (str): Nom du fichier à lire.
        demander_suppression_ligne (bool): Supprimer les lignes vides si True.

    Returns:
        list of dict: Données extraites sous forme de liste de dictionnaires.
    """
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as fichier:
                lire_json = json.load(fichier)
                if not isinstance(lire_json, list):
                    raise ValueError("Le fichier JSON doit contenir une liste de dictionnaires.")
                for row in lire_json:
                    if demander_suppression_ligne:
                        if any(str(val).strip() for val in row.values()):
                            data.append(row)
                    else:
                        data.append(row)
    except FileNotFoundError:
        print(f"Erreur : fichier {filename} introuvable.")
        return None
    return data

def extract_xml(filename, demander_suppression_ligne):
    """
    Extrait un fichier XML dans une liste de dictionnaires.
    
    Args:
        filename (str): Nom du fichier à lire.
        demander_suppression_ligne (bool): Supprimer les lignes vides si True.

    Returns:
        list of dict: Données extraites sous forme de liste de dictionnaires.
    """
    data = []
    try:
        arbre = ET.parse(filename)
        root = arbre.getroot()

        for item in root.findall("./ligne"):
            row = {}
            for champ in item:
                row[champ.tag] = champ.text if champ.text is not None else ""
            if demander_suppression_ligne:
                if any(str(val).strip() for val in row.values()):
                    data.append(row)
            else:
                data.append(row)

    except FileNotFoundError:
        print(f"Erreur : fichier {filename} introuvable.")
        return None
    except ET.ParseError:
        print(f"Erreur : le fichier {filename} n'est pas un XML valide.")
        return None
    return data

def transform(data_to_transform, remove_col=None):
    if remove_col is None:
        remove_col = []
    for row in data_to_transform:
        if "EmailPromotion" not in row:
            print("Colone absente")
        elif row["EmailPromotion"] == "0":
            row["EmailPromotion"] = "Non" 
        else:                                     
            row["EmailPromotion"] = "Oui"
    return data_to_transform

def load_manager(data_to_load, filename, choix):
    """
    Gestion des méthodes d'ecriture.
    
    Args:
        data_to_load (dict): Liste de dictionnaires à ecrire.
        filename (str): Nom du fichier.
        choix (str): Choix du format de sortie.
        
    Returns:
        Méthode associée.
    """
    formats = {
    "1": "csv",
    "2": "json",
    "3": "xml"
    }
    format_sortie = formats.get(choix)
    if not format_sortie:
        print("Choix invalide.")
        return

    valeur_retour = None
    match format_sortie:
        case "csv":
            valeur_retour = load_csv(data_to_load, filename)
        case "json":
            valeur_retour = load_json(data_to_load, filename)
        case "xml":
            valeur_retour = load_xml(data_to_load, filename)
        case _:
            print("Format non supporté.")
            return

    if valeur_retour == False:
        print("Aucune donnée à écrire.")
    else:
        print(f"Fichier créé : {filename}")

def generer_nom_sortie(filename, extension):
    """
    Genere un nom de fichier en sortie.
    
    Args:
        filename (str): Nom du fichier.
        extension (str): Nom de l'extension.
        
    Returns:
        nom du fichier + extension.
    """
    return os.path.splitext(filename)[0].lower() + extension

def load_csv(data_to_load, filename):
    """
    Ecrit une liste de dictionnaire dans un fichier CSV.
    
    Args:
        data_to_load (dict): Liste de dictionnaires à ecrire.
        filename (str): Nom du fichier.
        
    Returns:
        bool: True si l’écriture a réussi, False sinon.
    """
    nom_sortie = generer_nom_sortie(filename, ".csv")

    if not data_to_load:        
        return False
    
    with open (nom_sortie, "w", encoding="utf-8", newline="") as fichier:
        writer = csv.DictWriter(fichier, delimiter=",", fieldnames=data_to_load[0].keys())
        writer.writeheader()
        for row in data_to_load:
            writer.writerow(row)
    return True

def load_json(data_to_load, filename):
    """
    Ecrit une liste de dictionnaire dans un fichier JSON.
    
    Args:
        data_to_load (dict): Liste de dictionnaires à ecrire.
        filename (str): Lom du fichier.
        
    Returns:
        bool: True si l’écriture a réussi, False sinon.
    """
    nom_sortie = generer_nom_sortie(filename, ".json")

    if not data_to_load:
        return False
    
    with open (nom_sortie, "w", encoding="utf-8") as fichier:
        json.dump(data_to_load, fichier, indent=4, ensure_ascii=False)
    return True

def load_xml(data_to_load, filename):
    """
    Ecrit une liste de dictionnaire dans un fichier XML.
    
    Args:
        data_to_load (dict): Liste de dictionnaires à ecrire.
        filename (str): Nom du fichier.
        
    Returns:
        bool: True si l’écriture a réussi, False sinon.
    """
    nom_sortie = generer_nom_sortie(filename, ".xml")

    if not data_to_load:
        return False
    
    root = ET.Element("données")
    for row in data_to_load:
        item = ET.SubElement(root, "ligne")
        for cle, valeur in row.items():
            champ = ET.SubElement(item, cle)
            champ.text = str(valeur)

    arbre = ET.ElementTree(root)
    arbre.write(nom_sortie, encoding="utf-8", xml_declaration=True)
    return True