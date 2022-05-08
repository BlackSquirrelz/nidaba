#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# nidaba.py

""" Getting Forensic Artifacts from macOS X"""

import os
import argparse
import logging
import sys
import time
import getpass
import traceback
from datetime import date
from BrowserParsing import browser_parser
import artifacts
from version import __VERSION
import FileListing.filewalker as file_walker
from config import __WHITELIST

# Defining Static variables
CONF_FILE = 'locations.csv'
USERNAME = getpass.getuser()
__PROGRAM = 'Nidaba'
__AUTHOR = 'Tobias Weisskopf'
__EMAIL = 'me@tobias-weisskopf.dev'


def Logger(log_file_path, log_file_level=logging.DEBUG, log_console_level=logging.INFO):
    """Create custom logger"""
    try:
        print("Create Logger")
        logger = logging.getLogger('MAIN')
        lf_handler = logging.FileHandler(log_file_path, encoding='UTF-8')
        lf_format = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        lf_handler.setFormatter(lf_format)
        logger.addHandler(lf_handler)
    except Exception as e:
        logging.error(traceback.print_exc())
        sys.exit("The logging function raised an exception")
    return logger


def program_header():
    """Program Header"""
    print(f"Welcome to {__PROGRAM} - {__VERSION}")
    start_time = time.gmtime()
    print(start_time)
    print(25 * "---" + 'Start Collection' + 25 * "---")


# Parser for Commandline Arguments / Options
def argument_parser():
    """Parses the user given flags into actionable stuff"""
    # Define all arguments that can be submitted
    arg_parser = argparse.ArgumentParser(description="macOS Incident Response - Kit")

    # 01 - Collection Type
    arg_parser.add_argument("-c", "--collection_type",
                            type=int, default=0,
                            required=False,
                            help="Set collection type 0 triage, 1 comprehensive, if not set only triage.")

    # 02 - Output Path
    arg_parser.add_argument('-o', '--output-path',
                            help='Specify the path for the collectors output e.g. ~/Desktop',
                            required=True)

    # 03 - Debug Mode
    arg_parser.add_argument('-d', '--debug',
                            action="store_true",
                            default=False)

    # 04 - Browser
    arg_parser.add_argument('-b', '--browser',
                            action="store_true",
                            help="Set to collect browser information",
                            default=False)
    # 05 - File-listing
    arg_parser.add_argument('-l', "--listing",
                            required=False,
                            help="Specify a starting directory for the file walker")

    # 06 - Calculate md5 hash for file-listings
    arg_parser.add_argument('-H', "--hash",
                            required=False,
                            action="store_true",
                            help="Create md5 hash")

    # 07 - Whitelist stuff
    arg_parser.add_argument("-w", "--whitelist",
                            nargs='*',
                            required=False,
                            help="Whitelist specified directories to skip")

    args = arg_parser.parse_args()
    return args


def main():
    """Main Function"""
    # Program Header in Console
    program_header()

    # Parse users supplied arguments
    args = argument_parser()

    # Setup Logging Functionality
    log = Logger(os.path.join(args.output_path, str(time.strftime("%Y%m%d-%H%M%S")) + "_nidaba.log"),
                 logging.DEBUG,
                 logging.INFO)

    # Program Logic based on supplied arguments

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    if args.browser:
        browser_parser.browser_parsing(args)
    if args.whitelist:
        whitelist = args.whitelist
    else:
        whitelist = __WHITELIST
    if args.listing:
        # Staring Collection Script
        file_walker.run_collection(args.listing, args.output_path, args.hash, whitelist)
    if args.collection_type:
        artifacts.collect_artifacts(args.collection_type, args.output_path)
    else:
        logging.info(f"Collection Type was not set, defaulting to triage.")
        artifacts.collect_artifacts(args.collection_type, args.output_path)


    # Finishing with some Mass Effect 2 Quotes (Harbinger)
    # https://masseffect.fandom.com/wiki/Harbinger_(Collector)/Battle_Quotes

    print(25 * "---" + 'THE END' + 25 * "---")
    print("You are no longer relevant")


# Main Function of Program
if __name__ == "__main__":
    main()
