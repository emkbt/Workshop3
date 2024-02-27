import requests

# Liste des noms de modèles
model_names = ['model_linear', 'model_rdc', 'model_svr']

# Liste des URLs de base pour l'API avec ngrok pour chaque modèle
ngrok_urls = [
    'https://71e2-89-30-29-68.ngrok-free.app/predict/',
    'https://71e2-89-30-29-68.ngrok-free.app/predict/',
    'https://71e2-89-30-29-68.ngrok-free.app/predict/'
]  # Assurez-vous que ces URLs sont correctes

# Données à envoyer sous forme de paramètres de requête
params = {
    'feature_values': '7700,1,2,4,1,0,1,0,1,1,0,1,0,0,1,1,0,1,0,0'  # Exemple de chaîne de caractères pour les features
}

# Liste pour stocker les prédictions
predictions = []

# Itérer sur chaque paire de nom de modèle et son URL respective
for model_name, ngrok_url in zip(model_names, ngrok_urls):
    try:
        # Construction de l'URL pour le modèle spécifique
        model_url = f"{ngrok_url}{model_name}"
        
        # Envoi de la requête GET avec les données comme paramètres
        response = requests.get(model_url, params=params)
        
        # Vérification si la réponse est réussie
        if response.status_code == 200:
            prediction = response.json().get('prediction')
            predictions.append(prediction)
            print(f"Prediction for {model_name}:", prediction)
        else:
            print(f"Error for {model_name}:", response.text)
            
    except Exception as e:
        print(f"Error during request for {model_name}:", e)

# Calcul et affichage de la moyenne des prédictions
if predictions:
    average_prediction = sum(predictions) / len(predictions)
    print(f"Consensus prediction from all models: {average_prediction}")
else:
    print("No predictions were made due to errors.")
