# import bezier
# import numpy as np
# import matplotlib.pyplot as plt

# nodes = np.asfortranarray([
#     [0.0, 0.625, 1.0],
#     [0.0, 0.5  , 0.5],
# ])
# curve = bezier.Curve(nodes, degree=2)
# s_vals = np.linspace(0.0, 1.0, 100)
# points = curve.evaluate_multi(s_vals)
# plt.plot(points[0],points[1])
# plt.show()
# print(points)

import bezier
import numpy as np
import matplotlib.pyplot as plt

# Define start and end points
start = np.array([0.0, 0.0])
end = np.array([1.0, 0.0])
height = 0.3  # vertical distance of control points from the base line

# Define five control points:
# 1. Center
# 2. Between start and center
# 3. Between center and end
# 4. Outside start
# 5. Outside end

# Helper to create curve
def make_curve(p0, p1, p2):
    nodes = np.asfortranarray([
        [p0[0], p1[0], p2[0]],
        [p0[1], p1[1], p2[1]],
    ])
    return bezier.Curve(nodes, degree=2)

# Control points
center = (start + end) / 2
quarter1 = (start + center) / 2
quarter2 = (center + end) / 2
outside_left = start - np.array([0.25, 0.0])
outside_right = end + np.array([0.25, 0.0])

control_points = [
    center + np.array([0.0, height]),        # Center
    quarter1 + np.array([0.0, height]),      # Between start and center
    quarter2 + np.array([0.0, height]),      # Between center and end
    outside_left + np.array([0.0, height]),  # Outside start
    outside_right + np.array([0.0, height])  # Outside end
]

# Generate and plot all curves
s_vals = np.linspace(0.0, 1.0, 100)
plt.figure(figsize=(10, 6))

for idx, cp in enumerate(control_points):
    curve = make_curve(start, cp, end)
    points = curve.evaluate_multi(s_vals)
    plt.plot(points[0], points[1], label=f"Curve {idx+1}")

# Mark start and end points
plt.scatter([start[0], end[0]], [start[1], end[1]], color='black', zorder=5)
plt.title("Bézier curves with different focal points")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()

