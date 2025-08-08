import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("model_training/demo_data.csv")

# List to store processed rows
processed_data = []

# Segment into paths
paths = []
current_path = []

for _, row in df.iterrows():
    if row["State"] == "Released":
        current_path = [row]
    elif row["State"] == "Move" and current_path:
        current_path.append(row)
    elif row["State"] == "Pressed" and current_path:
        current_path.append(row)
        paths.append(current_path)
        current_path = []

# Process each path
for path in paths:
    if len(path) < 3:  # Need at least start, move, end
        continue

    start_x, start_y = path[0]["x"], path[0]["y"]
    end_x, end_y = path[-1]["x"], path[-1]["y"]

    # Iterate through moves
    for i in range(2, len(path)):
        prev = path[i - 1]
        curr = path[i]

        prev_speed = float(prev["Speed"].replace("px/s", "").strip())
        next_speed = float(curr["Speed"].replace("px/s", "").strip())
        # print(prev_speed)

        processed_data.append({
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "prev_x": prev["x"],
            "prev_y": prev["y"],
            "prev_speed": prev_speed,
            "next_x": curr["x"],
            "next_y": curr["y"],
            "next_speed": next_speed
        })

# Create new DataFrame
training_df = pd.DataFrame(processed_data)

# Save to CSV
training_df.to_csv("training_dataset.csv", index=False)

print("Training dataset generated: training_dataset.csv")