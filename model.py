import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from weighted_ensemble import WeightedEnsemble  

# Step 1: Load and prepare the data
housing_data = pd.read_csv('Housing.csv')  

X = housing_data.drop(columns=['price'])
y = housing_data['price']

# Step 1: Identify non-numeric columns
non_numeric_columns = X.select_dtypes(include=['object']).columns
print("Non-numeric columns:", non_numeric_columns)

# Step 2: Handle categorical variables (example using one-hot encoding)
X = pd.get_dummies(X, columns=non_numeric_columns)
print(X.columns)

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Choose models and train them
# Linear Regression Model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Random Forest Model
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)

# Support Vector Machine (SVM) Model
svm_model = SVR()
svm_model.fit(X_train, y_train)

# Step 5: Save the trained models
with open('linear_model.pkl', 'wb') as linear_model_file:
    pickle.dump(linear_model, linear_model_file)

with open('rf_model.pkl', 'wb') as rf_model_file:
    pickle.dump(rf_model, rf_model_file)
    
with open('svm_model.pkl', 'wb') as svm_model_file:
    pickle.dump(svm_model, svm_model_file)

# Step 6: Create a weighted ensemble
weighted_ensemble = WeightedEnsemble([linear_model, rf_model, svm_model])

# Step 7: Evaluate the ensemble's performance
ensemble_error = weighted_ensemble.evaluate(X_test, y_test)
print("Mean Squared Error (Ensemble):", ensemble_error)

# Step 8: Adjust weights based on consensus
weighted_ensemble.adjust_weights(X_test, y_test)
