import os
import zipfile

path = os.path.dirname(os.path.realpath(__file__))

zip_path = os.path.join(path, "utils.zip")

if os.path.exists(zip_path):
    print(f"Le fichier {zip_path} existe.")
    print(f"Taille du fichier : {os.path.getsize(zip_path)} octets")
    
    try:
        # Ouvrir et extraire le fichier ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(path)  # Extraire dans le même dossier
        print("Extraction terminée avec succès.")
    except zipfile.BadZipFile as e:
        print(f"Erreur lors de l'extraction : {e}")
else:
    print(f"Erreur : Le fichier {zip_path} est introuvable.")
