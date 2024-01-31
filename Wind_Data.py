from rocketpy import Environment
import os
import shutil
import Tools
import numpy as np
import multiprocessing

########################################################################
# Method for aquistion of wind data per specifed date and array of years
# using multiprocessing for bigger data sizes
########################################################################

# Function for making file
def file_make():
    print("Collecting Wind data")
    print("########################\n")
    file = "Outputs\\WindData"
    if os.path.exists(file):
        shutil.rmtree(file)
        os.makedirs(file)
    else:
        os.makedirs(file)



# Creates a directory of environmeny JSONS using diferent wind data
def wind_data1(year, month=6, day=6, soundingstation=72388):
    # Retrives the data from Wyoming Soundings at selected set of years, month, day and station
    while(True):
        try:
            env = Environment(date = (year, month, day, 12))
            url ="http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR={0}&MONTH={1}&FROM={3}12&TO={3}12&STNM={2}".format(year, month, soundingstation, day)
            env.set_atmospheric_model(
            type="wyoming_sounding",
            file=url
            )
        except ImportError:
                continue
        else:
            # Exports the data to a json in folder
            env.export_environment(filename="Winddata{:}".format(year))
            shutil.move("Winddata{:}.json".format(year), "Outputs\\WindData")
            break
    return year

# Creates a file to be written to for the final environment data
def finalfile(year):
    ans = Tools.fileexist("Outputs\\WindData\\Final_Wind.json")
    if ans == True:
        with open("Final_Wind.json",'w') as w, open("Outputs\\WindData\\Winddata2021.json", "r") as r:
            w.write(r.read())
            w.close()
            r.close()
        shutil.move("Final_Wind.json", "Outputs\\WindData")

    else:
        quit()


# Multi Process the Environments for speed
def multipro(year):
        file_make()
        result = []
        with multiprocessing.Pool(10) as p:   
            results = p.map(wind_data1, year)
            p.close()
            p.join()
            finalfile(year)
            for results in results:
                result.append(results)
            print(result)
            print()









        


    





    



















