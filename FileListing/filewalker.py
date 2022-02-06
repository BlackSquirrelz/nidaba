import os
import stat
import config
import nidaba_utils
import logging
import sqlite3


def collector(file_name, fi_fd, time_fd, hash_bool, cur):

    try:
        (mode, ino, dev, n_link, uid, gid, size, a_time, m_time, c_time), b_time = nidaba_utils.stat_file(file_name)

        # TODO: Optimize
        # create a string entry for each timestamp
        a_string = f"{nidaba_utils.format_time(a_time)}, accessed, {file_name}\n"  # Accessed Time
        m_string = f"{nidaba_utils.format_time(m_time)}, modified, {file_name}\n"  # Modified Time
        c_string = f"{nidaba_utils.format_time(c_time)}, changed, {file_name}\n"  # Changed Time

        # Birth Time not always present, thus in if packet
        if b_time is not None:
            b_string = f"{nidaba_utils.format_time(b_time)}, changed, {file_name}\n"  # Birth Time
        else:
            b_string = None

        # TODO: to FIX
        # check for special file bits
        x = (mode & stat.S_ISUID) + (mode & stat.S_ISGID) + (mode & stat.S_ISVTX)
        special = ""  #config.__SPECIALBITS(str(x))

        # TODO: Optimize and add SHA256 hashing algorithm? or SHA1?
        filetype = config.__FILETYPES[str.upper(oct(mode)[:3])]
        print(f"{filetype} - {str.upper(oct(mode))}")

        db_data = []

        if hash_bool and os.path.isfile(file_name):
            md5 = nidaba_utils.get_hash(file_name)  # Currently only MD5 to be changed to another algorithm
            file_bits = str.upper(oct(mode)[-3:])
            file_data = f"{file_name} {file_bits} {filetype} " \
                        f"{uid} {gid} {size} {special} {md5}\n"
            db_data.append((file_name, file_bits, filetype, uid, gid, size, special, md5))

        else:
            file_bits = str.upper(oct(mode)[-3:])
            file_data = f"{file_name} {file_bits} {filetype} " \
                        f"{uid} {gid} {size} {special}\n"
            db_data.append((file_name, file_bits, filetype, uid, gid, size, special, "Null"))

        # write data to files
        # Write to File Information
        fi_fd.write(file_data)

        # Write to Timeline File
        time_fd.write(a_string)
        time_fd.write(m_string)
        time_fd.write(c_string)
        if b_time is not None:
            time_fd.write(b_string)

        # Write Data to Database
        cur.executemany('''INSERT INTO fileinfo values (?, ?, ?, ?, ?, ?, ?, ?)''', db_data)

    except OSError:
        logging.log(40, f"OS Error in {file_name}")


# Running the collector
def run_collection(start_dir, dump_dir, hash_bool, whitelist):
    print(f"Assuming direct control...")
    file_info = f"{dump_dir}/file_info.txt"
    file_timeline = f"{dump_dir}/file_timeline.txt"
    con = sqlite3.connect(f"{dump_dir}/collection.db")

    # Prepare to write to Database
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS fileinfo;''')
    cur.execute('''CREATE TABLE fileinfo 
                (file_name text, filebits NUMERIC, 
                filetype text, uid NUMERIC, gid  NUMERIC,
                size NUMERIC, special NUMERIC, hash text);''')

    with open(file_info, mode='w') as fi_fd, open(file_timeline, mode='w') as time_fd:
        for dir_name, dir_names, file_names, in os.walk(start_dir, topdown=True):
            dir_names[:] = [d for d in dir_names if d not in whitelist]
            for file_name in file_names:
                file_with_path = os.path.join(dir_name, file_name)
                collector(file_with_path, fi_fd, time_fd, hash_bool, cur)
    con.commit()
    con.close()
