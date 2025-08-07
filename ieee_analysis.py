import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("demo_data.csv")

x = data["x"][:500]
y = data["y"][:500]
timestamp = data["Timems"][:500]
velocity = data["Speed"][:500]

plt.plot(timestamp,velocity)
# plt.text(20,20,len(x))
plt.show()