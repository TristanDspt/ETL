from tools import ouvrir_fichier_local

def lire_csv(nom_fichier: str, supprimer_lignes_vides = True) -> list[str]:
    with ouvrir_fichier_local("Personnes.csv", "r", "utf-8") as f:
        