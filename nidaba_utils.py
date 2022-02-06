import hashlib
import time
import os
import stat
import config
import os.path


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


def format_time(timestamp):
    return time.strftime("%Y-%m-%dT %H:%M:%S", time.gmtime(timestamp))


def check_type_special(file_path):
    special = file_path.st_mode & stat.S_ISUID + file_path.st_mode & stat.S_ISGID + file_path.st_mode & stat.S_ISVTX
    return config.__SPECIALBITS[str(special)]


def stat_file(file_path):
    return os.stat(file_path), getattr(os.stat(file_path), 'st_birthtime', None)

"""
# TODO: Implement LOGGER
# Check if all directories from the configuration file exist, otherwise create them.
def check_directories(category):
    time.sleep(0.5)
    #exists = path.exists(category)
    if exists:
        print(f'\t{category} exists -> {exists}')
    else: 
        os.mkdir(category)
        print(f'\t{category} does not exists -> {exists}, creating...')
"""