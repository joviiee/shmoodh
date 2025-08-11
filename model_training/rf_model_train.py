from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd

import matplotlib.pyplot as plt

# Load your processed training dataset
df = pd.read_csv("model_training/training_dataset.csv")

# Features and target
X = df[["start_x", "start_y", "end_x", "end_y", "prev_x", "prev_y","prev_speed"]]#, "prev_speed"
y = df[["next_x", "next_y", "next_speed"]] #, "next_speed"

feature_scaler = StandardScaler()
scaled_X = feature_scaler.fit_transform(X)

target_scaler = StandardScaler()
scaled_y = target_scaler.fit_transform(y)

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(scaled_X, scaled_y, test_size=0.2, random_state=42)

# Train
# model = RandomForestRegressor(n_estimators=200,random_state=42)
cubic_model = Pipeline([
    ('poly', PolynomialFeatures(degree=3, include_bias=False)),
    ('linear', LinearRegression())
])
cubic_model.fit(X_train, y_train)

# Predict
y_pred_scaled = cubic_model.predict(X_test)

y_pred = target_scaler.inverse_transform(y_pred_scaled)

pred_to_plot = y_pred[:10]
real_to_plot = target_scaler.inverse_transform(y_test)[:10]

# Evaluate
mse = mean_squared_error(target_scaler.inverse_transform(y_test), y_pred)
rmse = root_mean_squared_error(target_scaler.inverse_transform(y_test), y_pred)
print("Mean Squared Error:", mse)
print(" Root Mean Squared Error:", rmse)

# features = [108,202,783,478,108,204]
# transformed_features = feature_scaler.transform([[108,202,783,478,108,204]])
# scaled_prediction = cubic_model.predict(transformed_features)
# predictions = target_scaler.inverse_transform(scaled_prediction)
# print(f"===============================================")
# print(f"features ======= {features}")
# print(f"transformed_features ======= {transformed_features}")
# print(f"scaled_prediction ======= {scaled_prediction}")
# print(f"predictions ======= {predictions}")

def plot_helper(points):
    plot_x, plot_y = [], []
    for x, y, _ in points:
        plot_x.append(x)
        plot_y.append(y)
    return plot_x, plot_y

pred_x_plot,pred_y_plot = plot_helper(pred_to_plot)
real_x_plot, real_y_plot = plot_helper(real_to_plot)

plt.scatter(pred_x_plot,pred_y_plot)
plt.scatter(real_x_plot, real_y_plot)
plt.plot(pred_to_plot[:,-1], real_to_plot[:,-1])
plt.show()
