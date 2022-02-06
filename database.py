def file_info_table(cur):

    cur.execute('''DROP TABLE IF EXISTS fileinfo;''')
    cur.execute('''CREATE TABLE fileinfo 
                    (file_name text, filebits NUMERIC, 
                    filetype text, accessed NUMERIC, modified NUMERIC, changed NUMERIC, 
                    birth NUMERIC, uid NUMERIC, gid  NUMERIC,
                    size NUMERIC, special NUMERIC, hash text);''')


def timeline_table(cur):
    cur.execute('''DROP TABLE IF EXISTS timeline;''')
    cur.execute('''CREATE TABLE timeline
                (timestamp NUMERIC, type TEXT, file_name TEXT);''')
