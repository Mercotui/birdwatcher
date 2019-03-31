#!/usr/bin/env python3
"""birdwatcher_camera takes a picture with an attached camera an stores it with a timestamp"""
import time
import subprocess
import json
import os
import errno

PICTURE_ROOT = "/tmp/"

def main():
    """Main entry point"""
    current_time = time.localtime()
    time_string = time.strftime("%Y%m%d-%H%M%S", current_time)
    date_string = time.strftime("%Y%m%d", current_time)
    picture_directory = PICTURE_ROOT + date_string + "/"
    picture_name = time_string + ".jpg"

    take_picture(picture_directory, picture_name)
    append_pictures_json(picture_directory, picture_name)
    append_dates_json(date_string)

def take_picture(picture_directory, picture_name):
    """Take the picture and store it in picture_directory"""
    if not os.path.exists(picture_directory):
        try:
            os.makedirs(picture_directory)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    subprocess.run(["fswebcam", "-r", "5000x500000", "--no-banner", "-q", "-S", "30",
                    picture_directory + picture_name])


def append_dates_json(date_string):
    """Add current date to json"""
    try:
        with open(PICTURE_ROOT + "/dates_index.json", "r+") as file:
            days_array = json.load(file)
            if date_string not in days_array:
                days_array.append(date_string)

                file.seek(0)
                json.dump(days_array, file, sort_keys=True)
                file.truncate()
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open(PICTURE_ROOT + "dates_index.json", "w") as file:
            json.dump([date_string], file, sort_keys=True)

def append_pictures_json(picture_directory, picture_name):
    """Add latest picture to json"""
    try:
        with open(picture_directory + "pictures_index.json", "r+") as file:
            pictures = json.load(file)
            if picture_name not in pictures:
                pictures.append(picture_name)

                file.seek(0)
                json.dump(pictures, file, sort_keys=True)
                file.truncate()
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open(picture_directory + "pictures_index.json", "w") as file:
            json.dump([picture_name], file, sort_keys=True)

main()
