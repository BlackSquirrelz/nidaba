#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# nidaba.py

import os
from os import path
import csv
import logging
import time
import shutil
import getpass
from hashlib import md5
from hashlib import sha1
from hashlib import sha256

# Defining Static variables
CONF_FILE = 'locations.csv'
USERNAME = getpass.getuser()
__VERSION = 0.1
__AUTHOR = 'Tobias Weisskopf'


# Check if all directories from the configuration file exist, otherwise create them.
def check_directories(category):
    time.sleep(0.5)
    exists = path.exists(category)
    if exists:
        print(f'\t{category} exists -> {exists}')
    else: 
        os.mkdir(category)
        print(f'\t{category} does not exists -> {exists}, creating...')


# At the begining, do some housekeeping
def setup():

    print(f"Setting a few things up, hang on...\n")

    # Defining entries for Artifact Categories
    with open(CONF_FILE, 'r', encoding="UTF-8") as f:
        reader = csv.reader(f,delimiter=',')
        return [{'category': entry[0], 'path': entry[1], 'permission': entry[2]} for entry in reader if entry[0] != 'ArtifactCategory']


# TODO: Actually Checking if ROOT Permissions
def check_if_root():
    logging.warning(f"No sudo permissions detected, please start the application again with root permissions. This is required, because some artifacts are only accessible by root. You can check these artifacts in the configuration file.")


# Getting Artifacts based on CONF_FILE
def get_artifacts(art_path, art_category):
    time.sleep(0.5)
    print(f"Copying: {art_path}")
    logging.info(f'Getting {art_category} from {art_path}')

    # Use Copy 2 to preserve metadata
    # https://docs.python.org/3/library/shutil.html
    shutil.copy2(art_path, art_category)


def main():
    print(f"Nidaba - Triage tool for MacOS")
    print(30 * '=')

    start_time = time.gmtime()
    print(start_time)

    # Setting Up Stuff at the beginning.
    artifacts = setup()

    print(f"All Set")
    print(30* '-')

    # Add Categories to a Set in order to check if the directories of these have been created
    categories = set()
    for entry in artifacts:
        categories.add(entry['category'])
   
    for category in categories:
        check_directories(category)
        

    # Printing a user dialog for the acquisition of the artifacts
    # TODO!: Check if the user has root permissions, if not need to restart the application with root.
    print(f"\nStarting acquisition\n")
    for category in categories:
        print(f"\n{15 * '='} {category} {15 * '='}\n")
        for artifact in artifacts:
            if artifact['category'] == category:
                try:
                    get_artifacts(artifact['path'], artifact['category'])
                    if category == 'UserAccounts':
                        print(category)
                except OSError as err:
                    logging.warning(f"Error: {err}")
                    pass


# Main Function of Program
if __name__ == "__main__":
    main()