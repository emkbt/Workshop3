import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Step 1: Load and prepare the data
housing_data = pd.read_csv('housing_data.csv')  # Assuming your dataset is named 'housing_data.csv'

# Assuming the target variable is 'price', and other columns are features
X = housing_data.drop(columns=['price'])
y = housing_data['price']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Choose a model and train it
model = LinearRegression()
model.fit(X_train, y_train)

# Step 3: Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Step 4: Save the trained model
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)