"""Collection of functions to fetch data from the various databases"""


# fileinfo table
def file_info_table(cur):
    """Create a Table for File Information"""
    cur.execute('''DROP TABLE IF EXISTS fileinfo;''')
    cur.execute('''CREATE TABLE fileinfo
                    (file_name text, filebits NUMERIC, 
                    filetype text, accessed NUMERIC, modified NUMERIC, changed NUMERIC, 
                    birth NUMERIC, uid NUMERIC, gid  NUMERIC,
                    size NUMERIC, special NUMERIC, hash text);''')


# timeline table
def timeline_table(cur):
    """Create a timeline table"""
    cur.execute('''DROP TABLE IF EXISTS timeline;''')
    cur.execute('''CREATE TABLE timeline
                (timestamp NUMERIC, type TEXT, file_name TEXT);''')


# Browser data
def browser_data(cur):
    """Create table to store parsed browser data"""
    cur.execute('''DROP TABLE if EXISTS browserdata;''')
    cur.execute('''CREATE TABLE browserdata
                (browser TEXT, type TEXT, title TEXT, url TEXT, created NUMERIC, accessed NUMERIC);''')

