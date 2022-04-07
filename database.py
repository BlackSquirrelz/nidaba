"""Collection of functions to fetch data from the various databases"""


def file_info_table(cur):
    """Create a Table for File Information"""
    cur.execute('''DROP TABLE IF EXISTS fileinfo;''')
    cur.execute('''CREATE TABLE fileinfo
                    (file_name text, filebits NUMERIC, 
                    filetype text, accessed NUMERIC, modified NUMERIC, changed NUMERIC, 
                    birth NUMERIC, uid NUMERIC, gid  NUMERIC,
                    size NUMERIC, special NUMERIC, hash text);''')


def timeline_table(cur):
    """Create a timeline table"""
    cur.execute('''DROP TABLE IF EXISTS timeline;''')
    cur.execute('''CREATE TABLE timeline
                (timestamp NUMERIC, type TEXT, file_name TEXT);''')


def artifact_list(cur):
    """Get the list of artifacts from the database"""
    return cur.execute('''SELECT path FROM artifacts ORDER BY path''').fetchall()
