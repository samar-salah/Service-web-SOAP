from http.client import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

print("debut")
# Modèle de données pour la demande de score de crédit
class CreditRequest(BaseModel):
    description_bien : str 
    

# Charger les données de vente récentes à partir du fichier
def charger_ventes_recentes():
    try:
        with open('ventesRecentesBiens.txt', 'r') as file:
            data = file.read()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors du chargement des données de vente récentes")



# Service FastAPI pour estimer le prix d'un bien
@app.post("/estimer_prix_bien/")
async def estimer_prix_bien(description_bien: CreditRequest):
    print("description bienn   ", description_bien.description_bien)
    try:
        ventes_recentes = charger_ventes_recentes()
        lignes = ventes_recentes.split('\n')
        print(ventes_recentes, "veeeneteees recccc")
        
        for ligne in lignes:
            if ":" in ligne:
                partie_description, partie_prix = ligne.split(":", 1)
                partie_description = partie_description.strip().lower()  # Convertir en minuscules
                declow = description_bien.description_bien.strip().lower()  # Convertir en minuscules
                print("PL", partie_description)
                print("DL", declow)
                if declow in partie_description:
                    print("Partie desc low", partie_description)
                    print('description bien  low', declow)
                    # Extraire le prix du bien de la ligne après les ":"
                    prix_str = partie_prix
                    # Supprimer les espaces et le symbole €
                    prix_str = prix_str.replace('€', '').replace(' ', '')
                    # Convertir le prix en entier
                    prix = int(prix_str)
                    return {"prix_estime": prix}
        
        raise HTTPException(404, "Description du bien non trouvée")

    except Exception as e:
        raise HTTPException(500, "Erreur lors de l'estimation du prix du bien : " + str(e))
