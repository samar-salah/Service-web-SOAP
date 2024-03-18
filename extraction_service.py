# fastapi_text_processing.py
from http.client import HTTPResponse
from fastapi import FastAPI, HTTPException
import re
from fastapi.responses import HTMLResponse


app = FastAPI()
# Variable globale pour stocker les données
global_data = {}

# Fonction de prétraitement de texte
def preprocess_text(text):
    # Suppression des caractères indésirables (par exemple, les caractères spéciaux)
    text = ''.join(character for character in text if character.isalnum() or character.isspace())

    # Normalisation du texte (mise en minuscules)
    text = text.lower()

    # Correction des erreurs de frappe (vous pouvez ajouter des règles spécifiques ici)

    return text

@app.post("/process_text/")
async def process_text():
    global global_data 
    try:
        with open('demandePret.txt', 'r') as file:
            text = file.read()

        # Prétraitement du texte
        preprocessed_text = preprocess_text(text)

        pattern = r"identifiant du client (.+)\nnom du client (.+)\nadresse (.+)\nmontant du prêt demandé (.+)\ndescription de la propriété (.+)\nrevenu mensuel (.+)\ndépenses mensuelles (.+)"
        match = re.search(pattern, preprocessed_text)

        if match:
            identifiant_client, nom_client, adresse, montant_pret, description_propriete, revenu_mensuel, depenses_mensuelles = match.groups()

            # Création d'un dictionnaire structuré
            data = {
                "Informations Personnelles": {
                    "Identifiant du Client": identifiant_client,
                    "Nom du Client": nom_client,
                    "Adresse": adresse
                },
                "Montants Financiers": {
                    "Montant du Prêt Demandé": montant_pret,
                    "Revenu Mensuel": revenu_mensuel,
                    "Dépenses Mensuelles": depenses_mensuelles
                },
                "Description de la Propriété": description_propriete
            }
            global_data = data.copy()
            return data  # FastAPI convertira automatiquement le dictionnaire en JSON

        else:
            raise HTTPException(status_code=400, detail="Erreur : Les informations n'ont pas pu être extraites.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur : " + str(e))
    
    
# Route pour afficher les données au format HTML
@app.get("/process_text/", response_class=HTMLResponse)
async def display_text_data():
    global global_data  
    html_content = f"<html><body><p>Les informations extraites sont : {global_data}</p></body></html>"
    return HTMLResponse(content=html_content)
