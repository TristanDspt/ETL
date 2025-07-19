import csv
import json

def extract(filename="e:\\Data\\Tristan\\Document\\Programmation\\Python\\ETL\\Personnes.csv", separateur=";", demander_suppression_ligne = True):
    data = []
    try:
        with open(filename, "r",encoding="utf-8") as fichier:
                lire_csv = csv.DictReader(fichier, delimiter=separateur)
                for ligne in lire_csv:
                    if demander_suppression_ligne:
                        if any(val.strip() for val in ligne.values()):
                            data.append(ligne)
                    else:
                        data.append(ligne)
    except FileNotFoundError:
        print(f"Erreur : fichier {filename} introuvable.")
    return data

def transform(data_to_transform):
    # Pas de modification, on renvoie tel quel
    return data_to_transform

def load(data_to_load):
    with open ("personnes.json", "w", encoding="utf-8") as fichier:
        json.dump(data_to_load, fichier, indent = 4, ensure_ascii=False)
    return data_to_load
