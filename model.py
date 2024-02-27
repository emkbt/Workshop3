import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # Changed to Regressor
from sklearn.svm import SVR  # Import SVR for regression tasks
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class WeightedEnsemble:
    def __init__(self, models):  # Corrected __init__ method
        self.models = models
        self.weights = [1.0] * len(models)  # Initialize weights equally

    def predict(self, X):
        predictions = []
        for model in self.models:
            predictions.append(model.predict(X))
        weighted_predictions = [weight * pred for weight, pred in zip(self.weights, predictions)]
        return sum(weighted_predictions) / sum(self.weights)  # Weighted average

    def evaluate(self, X_test, y_test):
        ensemble_predictions = self.predict(X_test)
        ensemble_error = mean_squared_error(y_test, ensemble_predictions)
        return ensemble_error

    def adjust_weights(self, X_test, y_test):
        ensemble_predictions = self.predict(X_test)
        ensemble_error = mean_squared_error(y_test, ensemble_predictions)
        for i, model in enumerate(self.models):
            model_predictions = model.predict(X_test)
            model_error = mean_squared_error(y_test, model_predictions)
            self.weights[i] *= model_error / ensemble_error

# Load and prepare the data
housing_data = pd.read_csv('Housing.csv') 

X = housing_data.drop(columns=['price'])
y = housing_data['price']

# Identify non-numeric columns
non_numeric_columns = X.select_dtypes(include=['object']).columns

# Handle categorical variables (example using one-hot encoding)
X = pd.get_dummies(X, columns=non_numeric_columns)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models to train
models = {
    'RandomForestRegressor': RandomForestClassifier(),
    'SVR': SVR(),
    'LinearRegression': LinearRegression()
}

# Train, evaluate, and save each model
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"{name} Mean Squared Error:", mse)
    with open(f'model_{name.lower()}.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
