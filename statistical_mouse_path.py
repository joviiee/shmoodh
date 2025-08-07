import pyautogui
import numpy as np
import time
import random
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
POINTS = 100  # total steps in movement
JITTER_STD = 1.0  # mouse wobble std dev
PAUSE_PROBABILITY = 0.2  # chance to pause randomly
PAUSE_TIME_RANGE = (0.05, 0.15)  # pause duration range
OVERSHOOT_ENABLED = True


# --- EASING FUNCTION (ease-in-out) ---
def ease_in_out(t):
    return t ** 2 / (t ** 2 + (1 - t) ** 2)


# --- BEZIER CURVE GENERATION (Quadratic) ---
def bezier(t, p0, p1, p2):
    return (1 - t) ** 2 * np.array(p0) + \
           2 * (1 - t) * t * np.array(p1) + \
           t ** 2 * np.array(p2)


# --- GET PATH POINTS FROM START TO END ---
def generate_mouse_path(start, end):
    offset_x = (end[0] - start[0]) * 0.3 + random.uniform(-30, 30)
    offset_y = (end[1] - start[1]) * 0.3 + random.uniform(-30, 30)
    control = (start[0] + offset_x, start[1] + offset_y)

    t_vals = ease_in_out(np.linspace(0, 1, POINTS))
    path = np.array([bezier(t, start, control, end) for t in t_vals])

    # Add small Gaussian noise to simulate human hand jitter
    noise = np.random.normal(0, JITTER_STD, size=path.shape)
    path += noise

    return path


# --- OPTIONAL OVERSHOOT LOGIC ---
def add_overshoot(path, end):
    overshoot_point = (
        end[0] + random.randint(-5, 5),
        end[1] + random.randint(-5, 5)
    )
    overshoot_path = generate_mouse_path(path[-1], overshoot_point)
    correction_path = generate_mouse_path(overshoot_path[-1], end)
    return np.vstack([path, overshoot_path, correction_path])


# --- MAIN MOVE FUNCTION ---
def human_like_mouse_move(end_x, end_y):
    start_x, start_y = pyautogui.position()
    start = (start_x, start_y)
    end = (end_x, end_y)

    path = generate_mouse_path(start, end)

    if OVERSHOOT_ENABLED:
        path = add_overshoot(path, end)
    
    x_values,y_values =[], []
    for i, point in enumerate(path):
        x, y = int(point[0]), int(point[1])
        x_values.append(x)
        y_values.append(y)
        # pyautogui.moveTo(x, y)

        # Variable delay per step
        # time.sleep(random.uniform(0.005, 0.015))

        # # Occasional pause to simulate hesitation
        # if random.random() < PAUSE_PROBABILITY and i != 0 and i != len(path) - 1:
        #     time.sleep(random.uniform(*PAUSE_TIME_RANGE))

    plt.plot(x_values,y_values)
    plt.show()


# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    print("Move the mouse to a target location in 3 seconds...")
    time.sleep(3)
    target = pyautogui.position()
    print(f"Target position: {target}")
    time.sleep(1)

    human_like_mouse_move(target[0], target[1])
