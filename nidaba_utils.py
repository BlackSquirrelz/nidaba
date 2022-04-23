import datetime
import hashlib
import time
import os
import stat
import config
import os.path

""" Utilities that are used often in the application
- Time Conversion
- Hashing
- Lookup of File Stats
"""


# TODO: Create generic Hash Function instead
def get_hash(fp):
    with open(fp, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
            return m.hexdigest()

# ==== TIME Conversion stuff ====


def format_time(timestamp):
    """ Format integer timestamp to the desired timestamp format => 2022-02-09T 12:00:00"""
    return time.strftime("%Y-%m-%dT %H:%M:%S", time.gmtime(timestamp))


def convert_apple_time(apple_formatted_date):
    """Conversion from Apple Time / Mac absolute Time => Seconds since 2001-01-01 00:00:00 to UTC Time"""
    ose = (int(time.mktime(datetime.date(2001, 1, 1).timetuple())) - time.timezone)
    return format_time(ose+float(apple_formatted_date))
    #ts = (time.strftime('%Y-%m-%dT %H:%M:%S', time.gmtime(ose+apple_formatted_date)))

# === FILE SYSTEM Stuff ===


def check_type_special(file_path):
    special = file_path.st_mode & stat.S_ISUID + file_path.st_mode & stat.S_ISGID + file_path.st_mode & stat.S_ISVTX
    return config.__SPECIALBITS[str(special)]


def stat_file(file_path):
    """https://docs.python.org/3/library/stat.html"""
    return os.stat(file_path), getattr(os.stat(file_path), 'st_birthtime', None)


