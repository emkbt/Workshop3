from flask import Flask, jsonify
import requests
import numpy as np

app = Flask(__name__)

# List of model endpoints (replace with actual URLs)
model_endpoints = [
    "http://model1.ngrok.io/predict",
    "http://model2.ngrok.io/predict",
    "http://model3.ngrok.io/predict"
]

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Make requests to individual model endpoints
        predictions = []
        for endpoint in model_endpoints:
            response = requests.get(endpoint)
            prediction = response.json()['prediction']
            predictions.append(prediction)
        
        # Compute consensus prediction by averaging outputs
        consensus_prediction = np.mean(predictions)
        
        return jsonify({'consensus_prediction': consensus_prediction})
    except Exception as e:
        return jsonify({'error': 'Failed to generate consensus prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
