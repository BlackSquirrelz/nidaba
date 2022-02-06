#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# nidaba.py

import os
from os import path
import argparse
import csv
import logging
import time
import shutil
import getpass
from datetime import date
from version import __VERSION
from hashlib import md5
from hashlib import sha1
from hashlib import sha256

# Defining Static variables
CONF_FILE = 'locations.csv'
USERNAME = getpass.getuser()
__PROGRAM = 'Nidaba'
__AUTHOR = 'Tobias Weisskopf'
__EMAIL = 'me@tobias-weisskopf.dev'


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
# TODO: Simplify
def setup():

    print(f"Setting a few things up, hang on...\n")

    # Defining entries for Artifact Categories
    with open(CONF_FILE, 'r', encoding="UTF-8") as f:
        reader = csv.reader(f,delimiter=',')
        return [{'category': entry[0], 'path': entry[1], 'permission': entry[2]} for entry in reader if entry[0] != 'ArtifactCategory']


# TODO: Actually Checking if ROOT Permissions
def check_if_root():
    logging.warning(f"No sudo permissions detected, please "
                    f"start the application again with root permissions. "
                    f"This is required, because some artifacts are only"
                    f" accessible by root. You can check these artifacts in "
                    f"the configuration file.")


# Getting Artifacts based on CONF_FILE
def get_artifacts(art_path, art_category):
    time.sleep(0.5)
    print(f"Copying: {art_path}")
    logging.info(f'Getting {art_category} from {art_path}')

    # Use Copy 2 to preserve metadata
    # https://docs.python.org/3/library/shutil.html
    shutil.copy2(art_path, art_category)


def main():
    # Setting Up Stuff at the beginning.
    artifacts = setup()

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
    start_time = time.gmtime()
    cur_date = date.today()
    # Define all arguments that can be submitted
    arg_parser = argparse.ArgumentParser(description=f"{__PROGRAM} {__VERSION} - Triage tool for macOS by {__AUTHOR}")
    arg_parser.add_argument('-v', '--verbose', action="store_true", default=False) # Set verbosity
    arg_parser.add_argument('-o', '--output-path', help='Specify the path for the collectors output')
    args = arg_parser.parse_args()

    # Get some logging setup
    # TODO: Define further logging levels
    if args.verbose:
        logging_level = logging.INFO
    else:
        logging_level = logging.WARNING

    log_name = str(cur_date) + "_basic.log"
    logging.basicConfig(filename=log_name, level=logging_level)

    logging.info(f"Started Progam: {start_time}")

    # TODO: List of Modules in the future, so the user can select what to parse.
    modules = []
    logging.info(f"Loaded Modules {modules}")
    #main()