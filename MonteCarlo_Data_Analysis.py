import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


res = pd.read_excel("MonteCarlo_sim_outputs.xlsx")
del res[0]
length = len(res)
res = np.array_split(res, length)
apogee_x = np.array(res[5])
apogee_y = np.array(res[6])
impact_x = np.array(res[8])
impact_y = np.array(res[9])

# Creates figure
plt.figure(num=None, figsize=(6, 6), dpi=150, facecolor="w", edgecolor="k")

# Draw launch point
plt.scatter(0, 0, s=30, marker="*", color="black", label="Launch Point")
# Draw apogee points
plt.scatter(
    apogee_x, apogee_y, s=5, marker="^", color="green", label="Simulated Apogee"
)
# Draw impact points
plt.scatter(
    impact_x, impact_y, s=5, marker="v", color="blue", label="Simulated Landing Point"
)

# Add Labels to plots
plt.legend(loc=2, prop={'size': 6})
plt.title("Dispersion Analysis")
plt.ylabel("North (m)")
plt.xlabel("East (m)")

plt.show()



