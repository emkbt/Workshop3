import requests

# Define the URL of the Flask app
url = 'http://localhost:6000/predict'
ngrok_url = 'https://645c-89-30-29-68.ngrok-free.app/predict'

# Define the input data as a JSON object
data = {
    'area': 7700,
    'bedrooms': 1,
    'bathrooms' : 2,
    'stories': 4,
    'parking' : 1,
    'mainroad_no': 0,
    'mainroad_yes' : 1,
    'guestroom_no' : 0,
    'guestroom_yes' : 1,
    'basement_no' : 1,
    'basement_yes' : 0,
    'hotwaterheating_no' : 1,
    'hotwaterheating_yes': 0,
    'airconditioning_no' : 0,
    'airconditioning_yes' : 1,
    'prefarea_no' : 1,
    'prefarea_yes' : 0,
    'furnishingstatus_furnished' : 1,
    'furnishingstatus_semi-furnished' : 0,
    'furnishingstatus_unfurnished' : 0
}

try:
    # Send the POST request with the input data
    response = requests.post(ngrok_url, json=data)

    # Check if the response is successful
    if response.status_code == 200:
        print("Prediction:", response.json())
    else:
        print("Error:", response.text)

except Exception as e:
    print("Error:", e)
