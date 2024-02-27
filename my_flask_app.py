from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained models
with open('model.pkl', 'rb') as model_file:
    linear_model = pickle.load(model_file)

with open('rf_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

with open('svm_model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.json
    
    # Convert the input data to a DataFrame
    input_data = pd.DataFrame(data, index=[0])
    
    # Predict using both models
    linear_prediction = linear_model.predict(input_data)
    rf_prediction = rf_model.predict(input_data)
    svm_prediction = svm_model.predict(input_data)

    # Calculate consensus prediction (average of predictions)
    consensus_prediction = (linear_prediction + rf_prediction + svm_prediction) / 3
    
    # Format the response
    response = {'consensus_prediction': consensus_prediction[0]}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
