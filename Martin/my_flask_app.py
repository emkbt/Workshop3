from flask import Flask, request, jsonify
import numpy as np
import pickle
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define model paths
MODEL_PATHS = {
    'model_linear': 'model_linear.pkl',
}

def load_model(model_name):
    """Load the specified model from disk."""
    if model_name not in MODEL_PATHS:
        logger.error(f"Model name '{model_name}' is not recognized.")
        return None
    
    model_path = MODEL_PATHS[model_name]
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        logger.info(f"Model '{model_name}' loaded successfully from {model_path}.")
        return model
    except FileNotFoundError:
        logger.error(f"Model file '{model_path}' not found. Please ensure the model file is present.")
        return None
    except Exception as e:
        logger.error(f"Failed to load model '{model_name}' from {model_path} due to an error: {str(e)}")
        return None

@app.route('/')
def home():
    return "Hello, this is the machine learning model API!"

@app.route('/predict/<model_name>', methods=['GET'])
def predict(model_name):
    # Load the model based on the model_name parameter
    model = load_model(model_name)
    if model is None:
        return jsonify({'error': f'Model {model_name} could not be loaded.'}), 400

    feature_values = request.args.get('feature_values')
    if feature_values:
        try:
            features = np.array([float(x) for x in feature_values.split(',')]).reshape(1, -1)
            prediction = model.predict(features)
            return jsonify({'prediction': int(prediction[0])})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Could not process the request'}), 500
    else:
        return jsonify({'error': 'Missing feature_values parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
