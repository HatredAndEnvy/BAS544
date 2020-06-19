# Jerry Day
# BZAN 544
# Movie App
# 2/8/2020

# essential edits... 
# Change the output from trashbin to Schedules... done

# import a few close friends.
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import os
import re
import movieModel

def ScheduleCheckAndMake():
    """Checks for schedules corresponding to the subfolders of DataIn.  It creates any schedules that are missing."""

    # Grab the subfolders (and path) of DataIn.  We want a schedule for each of these folders.
    cinemaFolders = [ f for f in os.scandir("DataIn") if f.is_dir() ] # It would be smart to make sure that there are the right 2 files in these folders... but...
    # Grab the csv files in Schedues.  These are the Schedules we have already made.
    oldSchedules =  [ f.name for f in os.scandir("Schedules") if f.is_file() & bool(re.search(".*\.csv$", f.name)) ]

    # for each subfolder we want to grab the 2 files and run a model.... unless we already have one.
    for cinemaSFP in cinemaFolders:
        if cinemaSFP.name + "_Schedule.csv" not in oldSchedules:
            # print(type(cinemaSFP))
            # print(cinemaSFP)
            # print(cinemaSFP.path)
            ThBookDF = pd.read_csv(cinemaSFP.path + "/Theatre_Bookings.csv")
            #print(ThBookDF)
            ThDetsDF = pd.read_csv(cinemaSFP.path + "/Theatre_Details.csv")
            #print(ThDetsDF)
            # Call some function from movieModel.py to create and run the model...
            movieModel.generateSchedule(ThBookDF,ThDetsDF).to_csv("Schedules/" + cinemaSFP.name + "_Schedule.csv", index = False)  #                  <-------------- must change the TrashBin folder to Schedules folder
    return None

if __name__ == "__main__":
    ScheduleCheckAndMake()


        
