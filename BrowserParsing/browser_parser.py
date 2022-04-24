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

    for x in data:
        if not isinstance(x, type(None)):
            print(f"{x['browser']}, {x['type']}, {x['title']}, {x['url']}, {x['created']}, {x['accessed']}")
            cur.execute('''INSERT INTO browserdata VALUES (:browser,:type,:title,:url,:created,:accessed)''', x)
            con.commit()


# TODO: Move to better location
def print_to_file(string):
    """ Append parsed data to browser history file"""
    output_file = 'browser_history.txt'
    with open(output_file, 'a') as fd:
        fd.write(string)


def safari_parser(args, con):
    print(f"\n======= SAFARI OLD =======\n")
    print(f"Parsing Artifacts from Safari Browser")
    # For Older Safari Versions
    safari_plist = os.path.join(args.output_path, 'Bookmarks.plist')

    old_safari_artefacts = []

    with open(safari_plist, 'rb') as f:
        safari_data = plistlib.load(f)

        # Parse Reading List Data
        print("[1/2] Parsing Safari ReadingList")
        readlist_data = safari_readinglist_parser(safari_data)
        print(f"\tFound {len(readlist_data)} item(s) in Safari Readinglist")
        old_safari_artefacts.extend(readlist_data)

        # Parse Bookmarks Data
        print("[2/2] Parsing Safari Bookmarks")
        bookmarks_data = [parse_webbookmark_type(child) for child in safari_data['Children']]
        print(f"\tFound {len(bookmarks_data)} item(s) in Safari Bookmarks")
        old_safari_artefacts.extend(bookmarks_data)
        print(f"Adding {len(old_safari_artefacts)} to browserdata table")
        write_to_bd_table(old_safari_artefacts, con)

    print(f"Finished Parsing Safari old\n")


def parse_webbookmark_type(children, title="N/A"):
    """Recursive Loop Through the PLIST"""
    child_element = children['WebBookmarkType']

    if 'Children' in children.keys():
        for x in children['Children']:
            if 'Title' in children.keys():
                parse_webbookmark_type(x, children['Title'])
            else:
                parse_webbookmark_type(x)
    else:
        if child_element == 'WebBookmarkTypeLeaf':
            browser_artefact = {
                "browser": "Safari",
                "type": child_element,
                'title': title,
                "url": children['URLString'],
                "created": "n/a",
                "accessed": "n/a"
            }
            return dict(browser_artefact)
        if child_element == 'WebBookmarkTypeList':
            logging.debug(f"{children.keys()}")
        else:
            logging.debug(f"BookmarkType: {child_element} has {children.keys()}")

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
def safari_readinglist_parser(data):
    """Function to parse the Safari Readinglist and write it to the collection database"""
    plist_title = 'com.apple.ReadingList'
    children = data['Children']

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
                "title": "N/A",
                "created": str(date_added),
                "accessed": str(date_last_viewed)
            }

            data.append(dict(browser_artefact))
        return data


