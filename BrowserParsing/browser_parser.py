#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# browser_parser.py

"""Parse Browser information collected in the collection step if applicable"""

import logging
import sqlite3
from nidaba_utils import convert_apple_time
import plistlib
import os
import database
import shutil

dt_lookup = {
    0: 'CLEAN',
    1: 'DANGEROUS_FILE',
    2: 'DANGEROUS_URL',
    3: 'DANGEROUS_CONTENT',
    4: 'MAYBE_DANGEROUS_CONTENT',
    5: 'UNCOMMON_CONTENT',
    6: 'USER_VALIDATED',
    7: 'DANGEROUS_HOST',
    8: 'POTENTIALLY_UNWANTED',
    9: 'MAX'
}

def browser_parsing(args):
    con = sqlite3.connect(f"{args.output_path}/collection.db")
    browser_db_cleanup(con)

    print(f"Collecting Browser Information\n")

    # Collecting Safari
    # TODO: Make distinction better between the browsers
    print("Copy Safari Plist File")
    browser_file = os.path.join(os.environ['HOME'], 'Library/Safari/Bookmarks.plist')
    shutil.copy2(browser_file, args.output_path)

    if os.path.join(args.output_path, 'Bookmarks.plist'):
        safari_parser(args, con)
    con.close()

def browser_db_cleanup(con):
    print("\tDropping previous table")
    cur = con.cursor()
    database.browser_data(cur)
    con.commit()


# Write to table browserdata
def write_to_bd_table(data, con):
    print(f"\tWriting Data to browserdata")
    cur = con.cursor()
    db_data = [(item['browser'], item['type'], item['url'], item['created'], item['accessed']) for item in data]
    cur.executemany('''INSERT INTO browserdata VALUES (?,?,?,?,?)''', db_data)
    print(f"Table browserdata should have {len(db_data)} additional entries now.")


# TODO: Move to better location
def print_to_file(string):
    """ Append parsed data to browser history file"""
    output_file = 'browser_history.txt'
    with open(output_file, 'a') as fd:
        fd.write(string)

def safari_parser(args, con):
    print(f"Parsing Artifacts from Safari Browser")


    # Parse ReadingList
    print("Parsing Safari ReadingList")
    safari_readinglist_parser(args.output_path, con)
    con.commit()



def parse_safari_hist_plist(hist_file):
    """ Parse Safari History plist file from older safari versions"""
    logging.info("Parsing Safari PLIST File")
    history_data = plistlib.readPlist(hist_file)
    for x in history_data['WebHistoryDates']:
        ts_last_visit = convert_apple_time(x['lastVisitedDate'])
        print_to_file(f"{ts_last_visit}, safari_history {x['']}")


def parse_safari_hist_db(safari_hist_db):
    """Parsing Safari Database for newer safari versions"""
    logging.info("Parsing Safari DB")
    con = sqlite3.connect(safari_hist_db)
    cur = con.cursor()
    cur.execute('''SELECT h.visit_time, i.url
                    FROM history_visits h
                    INNER JOIN history_items i ON h.history_item = i.id);''')


def parse_safari_downloads_db(safari_downloads_db):
    print("Parsing Safari Downloads")


def parse_chrome_hist_db(chrome_hist_db):
    logging.info("Parsing Chrome")


# Parsing the Readinglist of Safari and storing it into a database
# Inspired by https://gist.github.com/ghutchis/f7362256064e3ad82aaf583511fca503
def safari_readinglist_parser(outpath, con):
    """Function to parse the Safari Readinglist and write it to the collection database"""
    # Load and parse the Bookmarks file
    safari_readlist = os.path.join(outpath, 'Bookmarks.plist')

    with open(safari_readlist, 'rb') as plist_file:
        plist = plistlib.load(plist_file)
        plist_title = 'com.apple.ReadingList'
        children = plist['Children']

        elements = [child['Children'] for child in children if child.get('Title', None) == plist_title]

        data = []

        for element in elements:
            for bookmark in element:
                try:
                    date_last_viewed = bookmark['ReadingList']['DateLastViewed']
                    date_added = bookmark['ReadingList']['DateAdded']
                except:
                    date_last_viewed = "NULL"
                    date_added = "NULL"
                # print(f"Safari', {plist_title}, {bookmark['URLString']}, {date_last_viewed}, {date_added}")

                browser_artefact = {
                         "browser": "Safari",
                         "type": "com.apple.ReadingList",
                         "url": bookmark['URLString'],
                         "created": str(date_added),
                         "accessed": str(date_last_viewed)
                }

                data.append(browser_artefact)

        # WRITE DATA to DB
        write_to_bd_table(data, con)
