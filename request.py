import requests

# Define the URL of the Flask app
url = 'http://127.0.0.1:5000/predict/random_forest'

# Define the input data as a JSON object
data = {
    'Pclass_1': 1,
    'Pclass_2': 0,
    'Pclass_3': 0,
    'Sex_female': 1,
    'Sex_male': 0,
    'Embarked_C': 0,
    'Embarked_Q': 1,
    'Embarked_S': 0,
    'Age': 24,
    'SibSp': 0,
    'Parch': 0,
    'Fare': 50,
}
try:
    # Send the GET request with the input data
    response = requests.get(url, params=data)

    # Check if the response is successful
    if response.status_code == 200:
        print("Prediction:", response.json())
    else:
        print("Error:", response.text)

except Exception as e:
    print("Error:", e)
