#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# browser_parser.py

"""Parse Browser information collected in the collection step if applicable"""

import logging
import sqlite3
import os
import database
import shutil
import BrowserParsing.safari_parsing


def browser_parsing(args):
    con = sqlite3.connect(f"{args.output_path}/collection.db")
    browser_db_cleanup(con)

    logging.info(f"Collecting Browser Information\n")

    # Collecting Safari
    # TODO: Make distinction better between the browsers
    logging.info("Copy Safari Files")
    browser_file = os.path.join(os.environ['HOME'], 'Library/Safari/Bookmarks.plist')
    shutil.copy2(browser_file, args.output_path)

    if os.path.join(args.output_path, 'Bookmarks.plist'):
        safari_parsing.safari_parser(args, con)
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


