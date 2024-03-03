import json

# Define a JSON database to track model balance and performance
DATABASE_FILE = 'model_database.json'

def load_model_database():
    try:
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_model_database(database):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(database, f, indent=4)

def register_model(model_name, initial_deposit=1000):
    # Load existing model database or create a new one
    model_database = load_model_database()

    # Check if the model is already registered
    if model_name in model_database:
        print(f"Model '{model_name}' is already registered.")
        return

    # Register the model with initial deposit
    model_database[model_name] = {'balance': initial_deposit, 'accuracy': 0}

    # Save the updated model database
    save_model_database(model_database)
    print(f"Model '{model_name}' registered with an initial deposit of {initial_deposit}.")

def slash_model(model_name, penalty_amount):
    # Load existing model database
    model_database = load_model_database()

    # Check if the model is registered
    if model_name not in model_database:
        print(f"Model '{model_name}' is not registered.")
        return

    # Apply penalty (slash) to the model's balance
    model_database[model_name]['balance'] -= penalty_amount

    # Save the updated model database
    save_model_database(model_database)
    print(f"Penalty of {penalty_amount} applied to model '{model_name}'.")

def update_model_accuracy(model_name, new_accuracy):
    # Load existing model database
    model_database = load_model_database()

    # Check if the model is registered
    if model_name not in model_database:
        print(f"Model '{model_name}' is not registered.")
        return

    # Update the model's accuracy
    model_database[model_name]['accuracy'] = new_accuracy

    # Save the updated model database
    save_model_database(model_database)
    print(f"Accuracy updated for model '{model_name}': {new_accuracy}.")

# Example usage:
# Register a model
register_model('Model A')

# Update model accuracy
update_model_accuracy('Model A', 0.75)

# Slash (apply penalty) to a model
slash_model('Model A', 200)
