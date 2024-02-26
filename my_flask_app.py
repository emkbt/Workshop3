from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.json
    
    # Convert the input data to a DataFrame
    input_data = pd.DataFrame(data, index=[0])  # Assuming data is a dictionary
    
    # Perform prediction using the trained model
    prediction = model.predict(input_data)
    
    # Format the response
    response = {'prediction': prediction[0]}  # Assuming the prediction is a single value
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)