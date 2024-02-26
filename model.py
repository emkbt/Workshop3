import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

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

# Step 4: Choose a model and train it
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Step 6: Save the trained model
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

