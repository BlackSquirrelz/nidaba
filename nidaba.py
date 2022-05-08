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

    arg_parser.add_argument('-d', '--debug',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('-b', '--browser',
                            action="store_true",
                            help="Set to collect browser information",
                            default=False)
    arg_parser.add_argument('-o', '--output-path',
                            help='Specify the path for the collectors output e.g. ~/Desktop',
                            required=True)
    arg_parser.add_argument('-s', "--start",
                            required=False,
                            help="Specify a starting directory for the file walker")
    arg_parser.add_argument('-H', "--hash",
                            required=False,
                            action="store_true",
                            help="Create md5 hash")
    arg_parser.add_argument("-w", "--whitelist",
                            nargs='*',
                            required=False,
                            help="Whitelist specified directories to skip")

    args = arg_parser.parse_args()
    return args


def main():
    """Main Function"""
    args = argument_parser()
    log = Logger(os.path.join(args.output_path, str(time.strftime("%Y%m%d-%H%M%S")) + "_nidaba.log"),
                 logging.DEBUG,
                 logging.INFO)

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    program_header()
    if args.browser:
        browser_parser.browser_parsing(args)
    if args.whitelist:
        whitelist = args.whitelist
    else:
        whitelist = __WHITELIST

    if args.start:
        # Staring Collection Script
        file_walker.run_collection(args.start, args.output_path, args.hash, whitelist)

        # Finishing with some Mass Effect 2 Quotes (Harbinger)
        # https://masseffect.fandom.com/wiki/Harbinger_(Collector)/Battle_Quotes

        # Get Artifacts
        # TODO: Move to Artifacts File-
        artifact_set = artifacts.get_artifact_list()
        no_artifacts = len(artifact_set)
        print(f"Size Artifact List: {no_artifacts}")
        artifact_dump = args.output_path + '/collected_artifacts'
        if not os.path.exists(artifact_dump):
            os.mkdir(artifact_dump)

        for artifact in artifact_set:
            artifacts.get_artifacts(artifact, artifact_dump)

    print(25 * "---" + 'THE END' + 25 * "---")
    print("You are no longer relevant")


# Main Function of Program
if __name__ == "__main__":
    main()
