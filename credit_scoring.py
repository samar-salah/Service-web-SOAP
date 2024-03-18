# fastapi_credit_scoring.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

# Variable globale pour stocker temporairement le score
score = None

# Modèle de données pour la demande de score de crédit
class CreditRequest(BaseModel):
    identifiant_client: int
    dettes_actuelles: int
    paiements_en_retard: int
    faillite: bool

# Fonction de calcul du score de crédit
def calculer_score_credit(credit_request: CreditRequest):
    # Logique de calcul du score de crédit
    score_de_base = 600  # Score de base

    # Les dettes actuelles réduisent le score
    penalite_dettes_actuelles = 10  # Pénalité par unité de dette
    score_dettes = score_de_base - (credit_request.dettes_actuelles * penalite_dettes_actuelles)

    # Les paiements en retard réduisent le score
    penalite_paiements_en_retard = 20  # Pénalité par paiement en retard
    score_paiements_en_retard = score_de_base - (credit_request.paiements_en_retard * penalite_paiements_en_retard)

    # Les antécédents de faillite affectent négativement le score
    penalite_faillite = 100  # Pénalité pour faillite
    if credit_request.faillite:
        score_faillite = score_de_base - penalite_faillite
    else:
        score_faillite = score_de_base

    # Calcule le score final comme la moyenne des scores pénalisés
    score_final = (score_dettes + score_paiements_en_retard + score_faillite) / 3

    score_final = max(300, min(800, score_final))

    return int(score_final)  # Renvoie le score comme un entier

@app.post("/calculate_credit_score/")
async def calculate_credit_score(credit_request: CreditRequest):
    global score
    score = calculer_score_credit(credit_request)
    return {"credit_score": score}

@app.get("/calculate_credit_score/", response_class=HTMLResponse)
async def calculate_credit_score_get():
    global score  # Accédez à la variable globale score
    if score is not None:
        html_content = f"<html><body><p>Le score de crédit est : {score}</p></body></html>"
    else:
        html_content = f"<html><body><p>Le score de crédit n'a pas encore été calculé.</p></body></html>"
    return HTMLResponse(content=html_content)
