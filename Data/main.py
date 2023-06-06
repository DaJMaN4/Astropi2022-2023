# Phase 2 - Drawers Coding Team
#
# Description of the program
#
# The program is designed to minimize the amount of failure points.
# So the point is to do as little as possible and in addition is protected
# by try functions to ensure that it operates reliably in space.
#
# The program captures photos and stores data about them.
# The processing of the photos will be done on Earth,
# in order to minimize the possibility of failure in space.
#
# When the program runs, it takes a low-resolution photo and checks the color of the pixels.
# If there are any light pixels in the image, the program takes another photo,
# this time at a higher resolution.
# The program then writes the data to a CSV file and saves the high-resolution photo.
#
# The photos are stored in JPG format to maximize the amount of photos that can be captured.
# The accuracy of the photos is not critical for the investigation.
# The most important thing is to capture as much data as possible to create more accurate maps.

import cv2
from pathlib import Path
import csv
from datetime import datetime
from picamera import PiCamera
from orbit import ISS
from time import sleep
from sense_hat import SenseHat
import os                                       # Used just for getting the size of photos

base_folder = Path(__file__).parent.resolve()   # path to folder for this script
data_file = base_folder / 'data.csv'            # path for csv file

camera = PiCamera()                             # Creating camera object
camera.resolution = (3280, 2464)                # Maximal resolution of the camera

photoNumber = 1                                 # helps to name photos
hourStart = datetime.now().hour                 # the hour when the program started
minuteStart = datetime.now().minute             # the minute when the program started
size = 0                                        # total size of stored data

sense = SenseHat()                              # creating sansehat object
sense.clear()                                   


sleep(1)                                        # delay to ensure everything is working before starting the main loop
with open(data_file, 'w', buffering=1) as f:    # initialize the CSV file for data
    writer = csv.writer(f)                      # creates a csv file to log and store data
    while True:
        try:
            location = ISS.coordinates()
        except:
            row = (datetime.now(), "failed to find the location of ISS")  # writing information to row
            writer.writerow(row)                                          # writes a row to the data file
            location = "location error"
        try:
            if datetime.now().hour - 3 == hourStart \
                    and datetime.now().minute +2 == minuteStart: # Checking if 2 hours and 58 minutes has past
                break
        except:
            row = (datetime.now(), "failed to check current time", location)  # writing information to a row
            writer.writerow(row)                                              # writes a row to the data file
        try:
            if size > 2950000000: # checks if photos takes more than 2.95GB of space
                break
        except:
            row = (datetime.now(), "failed to check size of files", location)  # writing information to a row
            writer.writerow(row)                                               # writes a row to the data file
        try:
            camera.capture(f'{base_folder}/testImage.jpg')
        except:
            row = (datetime.now(), "failed to take a photo", location)  # writing information to a row
            writer.writerow(row)                                        # writes a row to the data file
        try:
            image = cv2.imread(f'{base_folder}/testImage.jpg')  # reads low resolution photo
            gimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)      # Makes gray version of the image
        except:
            row = (datetime.now(), "failed to check the darkness of an image",location)  # writing information to a row
            writer.writerow(row)                                                         # writes a row to the data file
        try:
            temp = sense.get_temperature()
            humidity = sense.get_humidity()
            pressure = sense.get_pressure()
            gyro_only = sense.get_gyroscope()
            raw = sense.get_compass_raw()
            if gimg.sum() != 10000:               # If the photo is not compliantly dark, uses numpy to sum all the values
                camera.resolution = (3280, 2464)  # resolution of store photos
                camera.capture(f'{base_folder}/Image' + photoNumber.__str__() + ".jpg") # store photos and add name to it
                camera.resolution = (1000, 1000)                                          # resolution for checking darkness

                row = (datetime.now(), photoNumber, "day", location, temp, humidity, pressure, gyro_only, raw)  # write information to a row
                writer.writerow(row)                                  # writes a row to the data file

                size = os.path.getsize(f'{base_folder}/Image' + photoNumber.__str__() + ".jpg") + size # adds size of photos to variabel size
            else:
                row = (datetime.now(), photoNumber, "night", location, temp, humidity, pressure, gyro_only, raw)  # writing information to a row
                writer.writerow(row)                                    # writes a row to the data file
        except:
            row = (datetime.now(), "something failed while storing photo",location)  # writing information to a row
            writer.writerow(row) # writes a row to the data file
        photoNumber += 1         # number of photo, helps to find photo that corresponds to csv file
        sleep(10)                # delay between taken photos. While testing we found that 10 seconds is the most optimal value