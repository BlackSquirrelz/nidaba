import logging
import sqlite3
import plistlib
import glob
import time
import datetime
from nidaba_utils import convert_apple_time

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


# TODO: Move to better location
def print_to_file(string):
    """ Append parsed data to browser history file"""
    output_file = 'browser_history.txt'
    with open(output_file, 'a') as fd:
        fd.write(string)


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


def parse_chrome_hist_db(chrome_hist_db):
    logging.info("Parsing Chrome")





