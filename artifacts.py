import time
import logging
import shutil
import database
import sqlite3


def get_artifact_list():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    fetched_data = database.artifcat_list(cur)
    con.close()

    return {artifact[0] for artifact in fetched_data}


# Getting Artifacts based on CONF_FILE
def get_artifacts(art_path, dump_dir):
    try:
        # Use Copy 2 to preserve metadata
        # https://docs.python.org/3/library/shutil.html
        shutil.copy2(art_path, dump_dir)
        print(f"Copied: {art_path}")
    except OSError:
        print(f"Error: {art_path}")
