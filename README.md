# Tableau de Bord interactif pour visualiser les Petites Villes de Demain

## Bienvenue !
**Une application Dash interactive pour explorer et visualiser les données sur les Petites Villes de Demain.**

---

## Prérequis :
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git installé

---

## Instructions pour lancer l'application :

1. Ouvrir un terminal et exécuter le script suivant :

FILE_ID = "1o0UXLmnEsX0Rqe896gUW0gozul-H_Yp-"
FILE_NAME = utils.rar

```bash

# Déplacez-vous dans le dossier où vous souhaitez cloner le projet :
#cd /chemin/vers/dossier/

# Clonez le dépôt GitHub :
git clone https://github.com/Aziz2805/PIP.git

# Accédez au dossier cloné :
cd PIP

#Installation de gdown pour pouvoir importer les données
echo "Installation de gdown ..."
pip install gdown

#Importation des données
echo "Téléchargement des données depuis Google Drive..."
gdown "https://drive.google.com/uc?id=1o0UXLmnEsX0Rqe896gUW0gozul-H_Yp-" -O "utils.rar" || { echo "Échec du téléchargement. Vérifiez l'ID du fichier."; exit 1; }

# Installation des dépendances du projet :
pip install -r requirements.txt

# Extraction des données:
echo "Extraction des données..."
unzip -o "${FILE_NAME}" -d "utils" || { echo "Échec de l'extraction."; exit 1; }

# Lancez l'application Dash :
python app.py

```


2. Rendez-vous sur http://127.0.0.1:8050/home.

## ✨ Profitez-en !

Parcourez les données et visualisez les informations clés des Petites Villes de Demain.
