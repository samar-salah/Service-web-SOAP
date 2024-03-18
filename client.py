import requests
import json
import certifi
import tkinter as tk
from tkinter import ttk

session = requests.Session()
session.verify = certifi.where()
# URL du service d'extraction de données
text_processing_url = "http://localhost:8000/process_text/"

# URL du service de calcul de score de crédit
credit_scoring_url = "http://localhost:8001/calculate_credit_score/"



# URL du service d'évaluation de la propriété
evaluationProp_service_url = "http://localhost:8002/estimer_prix_bien/"

# URL du service de decision
decision_dapprobationService_url = "http://localhost:8003/prendre_decision_approbation/"

# Envoyer une requête POST au service d'extraction de données
response_text_processing = requests.post(text_processing_url)
print("Résultat de l'extraction de données:")
data = response_text_processing.json()  # Convertit la réponse en JSON
print(data)

# Extraire l'identifiant du client du résultat de l'extraction
identifiant_client = data['Informations Personnelles']['Identifiant du Client']
print('Identifiant client extrait:')
print(identifiant_client)

# Charger le fichier JSON de la base de données
with open('BD_Banque.json', 'r') as db_file:
    db_data = json.load(db_file)

# Rechercher les informations associées à l'identifiant du client
client_info = None
for employe in db_data['employes']:
    if employe['id'] == int(identifiant_client):
        client_info = employe
        break

# Vérifier si des informations client ont été trouvées
if client_info is not None:
    # Créer un objet credit_request avec les informations du client
    credit_request = {
        "identifiant_client": client_info['id'],
        "dettes_actuelles": client_info['dettes_en_cours'],
        "paiements_en_retard": client_info['paiements_en_retard'],
        "faillite": bool(client_info['faillite'])
    }

    print("\nDonnées envoyées au service de calcul de score de crédit:")
    print(credit_request)

    # Envoyer les informations au service de calcul de score de crédit
    response_credit_scoring = requests.post(credit_scoring_url, verify=False, json=credit_request)
    print("\nRésultat du calcul de score de crédit:")
    print(response_credit_scoring.json())  # Convertit la réponse en JSON
else:
    print("\nAucune information client trouvée pour l'identifiant", identifiant_client)

# Extraire la description de la propriété du client du résultat de l'extraction
description_propriete = data['Description de la Propriété']
print('Description de la Propriété client:')
print(description_propriete)

# Envoyer la description de la propriété au service d'estimation de prix
response_evaluationProp_service = requests.post(evaluationProp_service_url, json={"description_bien": description_propriete})
print("\nPrix estimé (réponse du service d'estimation de prix de la propriété):")
print(response_evaluationProp_service.json())  # Convertit la réponse en JSON




# Extraction de la partie numérique des chaînes et conversion en types appropriés
montantPretDemande = int(data['Montants Financiers']['Montant du Prêt Demandé'].split()[0])
revenuMensuel = int(data['Montants Financiers']['Revenu Mensuel'].split()[0])

if client_info is not None:
    # Créer un objet credit_requestDec avec les informations du client
    credit_requestDec = {
        "score_credit": response_credit_scoring.json()['credit_score'],
        "montant_pret": montantPretDemande,
        "valeur_propriete": response_evaluationProp_service.json()['prix_estime'],
        "montant_dettes": client_info['dettes_en_cours'],
        "revenu_mensuel": revenuMensuel
    }
    print("\nDonnées envoyées au service de décision:")
    print(credit_requestDec)

    # Envoyer les informations au service de décision
    response_decision_dapprobationService = requests.post(decision_dapprobationService_url, json=credit_requestDec)
    print("\nRésultat du service de décision:")
    print(response_decision_dapprobationService.json())  # Convertit la réponse en JSON
else:
    print("\nAucune information client trouvée pour l'identifiant", identifiant_client)


def display_section(section_name):
    response = requests.post("http://localhost:8000/process_text/")
    data = response.json()
    section_data = data.get(section_name, "Aucune donnée disponible pour cette section.")
    
    if isinstance(section_data, dict):
        formatted_data = "\n".join([f"{key}: {value}" for key, value in section_data.items()])
    else:
        formatted_data = section_data

    # Afficher le nom de la section en rouge
    section_label.config(text=f"{section_name}:\n{formatted_data}", foreground="red")




def extract_and_display_data():
    root = tk.Tk()
    root.title("Evaluation de demande de prêt immobilier")

    title_label = ttk.Label(root, text="Evaluation de demande de prêt immobilier", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=10)

    sections = ["Informations Personnelles", "Montants Financiers", "Description de la Propriété"]

    for section_name in sections:
        ttk.Button(root, text=section_name, command=lambda s=section_name: display_section(s)).pack(pady=5)

    global section_label
    section_label = ttk.Label(root, text="", wraplength=400)
    section_label.pack(pady=10)

    root.mainloop()
    
if __name__ == "__main__":
    extract_and_display_data()
    
