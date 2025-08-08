from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# Load your processed training dataset
df = pd.read_csv("model_training/demo_data.csv")

# Features and target
X = df[["start_x", "start_y", "end_x", "end_y", "prev_x", "prev_y", "prev_speed"]]
y = df[["next_x", "next_y", "next_speed"]]

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
