import math
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import scipy
from time import monotonic

# Mean Square Error
# locations: [ (lat1, long1), ... ]
# distances: [ distance1, ... ]
from scipy.optimize import minimize

data = [{"distance": 7.29, "location": np.array([-2.96, -2.76, 7.49])},
        {"distance": 0, "location": np.array([2, 4, 3.4])},
        {"distance": 6.81, "location": np.array([6.15, -7.62, 3])},
        ]

locations = [p["location"] for p in data]
x_data = [p[0] for p in locations]
y_data = [p[1] for p in locations]
z_data = [p[2] for p in locations]

distances = [p["distance"] for p in data]
# Initial point: the point with the closest distance
min_distance = float('inf')
closest_location = None
for member in data:
    # A new closest point!
    if member['distance'] < min_distance:
        min_distance = member['distance']
        closest_location = member['location']
initial_location = np.array([0, 0, 0])


def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = euclidean_distance(x[0], x[1], x[2], location[0], location[1], location[2])
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(distances)


def euclidean_distance(x1, y1, z1, x2, y2, z2):
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    return np.linalg.norm(p1 - p2)


# initial_location: (lat, long)
# locations: [ (lat1, long1), ... ]
# distances: [ distance1,     ... ]
time1 = monotonic()
result = minimize(
    mse,  # The error function
    initial_location,  # The initial guess
    args=(locations, distances),  # Additional parameters for mse
    method='nelder-mead',  # The optimisation algorithm
    options={
        'ftol': 1e-2,  # Tolerance
        'maxiter': 1e+10  # Maximum iterations
    })
time2 = monotonic()
print(time2 - time1)
location = result.x
print(location)

fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    if event.dblclick and event.button == 2:
        s = ax.format_coord(event.xdata, event.ydata)
        out = [float(x.split('=')[1].strip().replace("−", "-")) for x in s.split(',')]
        ax.scatter(out[0], out[1], out[2])
        fig.canvas.draw()
        fig.canvas.flush_events()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

ax.scatter(x_data, y_data, z_data)
for distance, tracker in zip(distances, locations):
    ax.plot([tracker[0], location[0]], [tracker[1], location[1]], [tracker[2], location[2]])
    ax.text(tracker[0] * (1 + 0.01), tracker[1] * (1 + 0.01), tracker[2], str(distance), fontsize=12)

