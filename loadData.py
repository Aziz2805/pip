import os

path = os.path.dirname(os.path.realpath(__file__))

rar_path = os.path.join(path, "utils.rar")

if os.path.exists(rar_path):
    print(f"Le fichier {rar_path} existe.")
    print(f"Taille du fichier : {os.path.getsize(rar_path)} octets")
else:
    print(f"Erreur : Le fichier {rar_path} est introuvable.")
