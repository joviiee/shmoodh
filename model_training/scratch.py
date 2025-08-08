from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# Load your processed training dataset
df = pd.read_csv("model_training/demo_data.csv")
print(df.columns)