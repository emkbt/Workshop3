import json

def update_model_performance(model_name, new_accuracy):
    with open('models_performance.json', 'r') as file:
        data = json.load(file)
    
    model_data = data.get(model_name, {})
    accuracy_change = new_accuracy - model_data.get('accuracy', 0)
    if accuracy_change < 0:
        model_data['deposit'] = max(0, model_data.get('deposit', 1000) - 100)
    model_data['accuracy'] = new_accuracy
    data[model_name] = model_data
    
    with open('models_performance.json', 'w') as file:
        json.dump(data, file)

# Example call to update model performance
# update_model_performance('model1', 0.92)
