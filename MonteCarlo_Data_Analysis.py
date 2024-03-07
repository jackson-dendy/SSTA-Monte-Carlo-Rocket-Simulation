import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
from matplotlib.patches import Ellipse

#############################################
# Analysis code for the output excel sheets
# from the monte carlo simulation
# HEAVY USE OF ROCKETPY CODE - Big thank you to
# the rocket py devs for writing fantastic 
# documentation
##############################################

class Plots():

    def __init__(self):
        self.name = "Big Liquid"
        self.file = "Outputs\\MonteCarlo_sim_outputs.xlsx"
        self.wind = "Outputs\\MonteCarlo_sim_wind.xlsx"
    
    def disp(self):
        #image = img.imread("C:\\Users\\lejay\\OneDrive - University of Tennessee\\Pictures\\Screenshots\\Screenshot 2024-02-22 171802.png")
        res = pd.read_excel(self.file)
        del res[0]
        length = len(res)
        res = np.array_split(res, length)
        apogee_x = np.array(res[5])
        apogee_y = np.array(res[6])
        impact_x = np.array(res[8])
        impact_y = np.array(res[9])


        # Creates figure
        plt.figure(num=None, figsize = (5,5), dpi=150, facecolor="w", edgecolor="k")
        ax = plt.subplot(111)
        ax1 = plt.gca()
        

        # Creates Error Ellipses

        def eigsorted(cov):
            vals, vecs = np.linalg.eigh(cov)
            order = vals.argsort()[::-1]
            return vals[order], vecs[:, order]
        
        # Calc Error Ellipses for impact
        impactCov = np.cov(impact_x, impact_y)
        impactVals, impactVecs = eigsorted(impactCov)
        impactTheta = np.degrees(np.arctan2(*impactVecs[:, 0][::-1]))
        impactW, impactH = 2 * np.sqrt(impactVals)

        # Draw Impact Error Ellipses
        impact_ellipses = [1, 2, 3]
        for j in [1, 2, 3]:
            impactEll = Ellipse(
                xy=(np.mean(impact_x), np.mean(impact_y)),
                width=impactW * j,
                height=impactH * j,
                angle=impactTheta,
                color="black",
            )
            impactEll.set_facecolor((0, 0, 1, 0.2))
            impact_ellipses.append(impactEll)
            ax.add_artist(impactEll)

        # Calculate error ellipses for apogee
        apogeeCov = np.cov(apogee_x, apogee_y)
        apogeeVals, apogeeVecs = eigsorted(apogeeCov)
        apogeeTheta = np.degrees(np.arctan2(*apogeeVecs[:, 0][::-1]))
        apogeeW, apogeeH = 2 * np.sqrt(apogeeVals)

        # Draw error ellipses for apogee
        for j in [1, 2, 3]:
            apogeeEll = Ellipse(
                xy=(np.mean(apogee_x), np.mean(apogee_y)),
                width=apogeeW * j,
                height=apogeeH * j,
                angle=apogeeTheta,
                color="black",
            )
            apogeeEll.set_facecolor((0, 1, 0, 0.2))
            ax.add_artist(apogeeEll)

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
        plt.title("Dispersion Analysis for Big Liquid")
        plt.ylabel("North (m)")
        plt.xlabel("East (m)")
        #plt.imshow(image, extent=[-20000, 20000, -20000, 20000])
        plt.show()

    def wind_plot(self, plots):

        res = pd.read_excel(self.wind)
       
        for i in range(plots):
            plot = plt.figure(num=None, figsize = (7,5), dpi=125, facecolor="w", edgecolor="k")
            plt.title("Wind Velocity X and Y")
            plt.xlabel("Velocity (m/s)")
            plt.ylabel("Altitude (m)")
            if i == 0:
                plt.plot(res["x (m/s)"], res['m'], label = "x velocity")
                plt.plot(res["y (m/s)"], res['m'], label= "y velocity")
                plt.legend(loc=1, prop={'size': 6})
                plt.show()
                continue
            else:
                header = f".{i}"

            plt.plot(res[f"x (m/s){header}"], res['m'], label= "x velocity")
            plt.plot(res[f"y (m/s){header}"], res['m'], label = "y velocity")
            plt.legend(loc=1, prop={'size': 6})
            plt.show()


        


bruh = Plots()

bruh.wind_plot(1)




