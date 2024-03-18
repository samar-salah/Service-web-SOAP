*** EL KAMEL Sirine + SALAH Samar ****
*** IATIC 5 ****

**Lancement des Services**
Pour exécuter les services REST API, ouvrez un terminal et suivez ces étapes :

    Service 1 => Cette command permet de lancer le premier service sur le port 8000.
        uvicorn extraction_service:app --host 0.0.0.0 --port 8000

    Service 2
        dans un autre terminal 
        uvicorn credit_scoring:app --host 0.0.0.0 --port 8001

    Service 3
        dans un autre terminal 
        uvicorn evaluationProp_service:app --host 0.0.0.0 --port 8002

    Service 4
        dans un autre terminal
        uvicorn decision_dapprobationService:app --host 0.0.0.0 --port 8003

**lancement du client (Composite)**
Une fois que les services sont en cours d'exécution, ouvrez un nouveau terminal et exécutez le client.py :

    python3 client.py

Interface Graphique
Le client.py propose également une interface graphique. Suivez ces étapes pour l'utiliser :

Exécutez le client.py comme indiqué précédemment.
Une fenêtre graphique s'ouvrira.
Dans cette interface, entrez l'identifiant du client dans le champ prévu.
Cliquez sur le bouton pour soumettre la demande.
Vous obtiendrez la réponse dans la fenêtre graphique
