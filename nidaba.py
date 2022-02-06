#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# nidaba.py

import os
from os import path
import argparse
import logging
import time
import getpass
from datetime import date

import Logger
from version import __VERSION
import FileListing.filewalker as file_walker
from config import __WHITELIST

# Defining Static variables
CONF_FILE = 'locations.csv'
USERNAME = getpass.getuser()
__PROGRAM = 'Nidaba'
__AUTHOR = 'Tobias Weisskopf'
__EMAIL = 'me@tobias-weisskopf.dev'


# TODO: Actually Checking if ROOT Permissions
def check_if_root():
    logging.error(f"No sudo permissions detected, please start the application again with root permissions. "
                  f"This is required, because some artifacts are only accessible by root. "
                  f"You can check these artifacts in the configuration file.")


def program_header():
    print(f"Welcome to {__PROGRAM} - {__VERSION}")
    start_time = time.gmtime()
    print(start_time)
    print(25 * "===")


# Main Function of Program
if __name__ == "__main__":

    program_header()

    # TODO: List of Modules in the future, so the user can select what to parse.
    modules = ['soso']

    cur_date = date.today()

    # Define all arguments that can be submitted
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-v', '--verbose', action="store_true", default=False)  # Set verbosity
    arg_parser.add_argument('-o', '--output-path', help='Specify the path for the collectors output e.g. ~/Desktop')
    arg_parser.add_argument('-s', "--start", required=True, help="Specify a starting directory for the file walker")
    arg_parser.add_argument('-H', "--hash",
                            required=False,
                            action="store_true",
                            help="Create file hashes of collected data, currently only md5 is supported")
    arg_parser.add_argument("-w", "--whitelist", nargs='*', required=False, help="Whitelist "
                                                                                 "specified directories to skip")

    args = arg_parser.parse_args()

    #logger = Logger.Logger()

    # Get some logging setup
    # TODO: Define further logging levels
    if args.verbose:
        logging_level = logging.INFO
    else:
        logging_level = logging.WARNING

    log_name = str(cur_date) + "_basic.log"
    logging.basicConfig(filename=log_name, level=logging_level)

    logging.info("It works.")
    logging.info(f"Loaded Modules {modules}")

    if args.whitelist:
        whitelist = args.whitelist
    else:
        whitelist = __WHITELIST

    # Staring Collection Script
    file_walker.run_collection(args.start, args.output_path, args.hash, whitelist)

    # Finishing with some Mass Effect 2 Quotes (Harbinger)
    # https://masseffect.fandom.com/wiki/Harbinger_(Collector)/Battle_Quotes
    print("You are no longer relevant")
