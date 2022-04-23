import sqlite3
import shutil
import database
import sqlite3
from contextlib import closing
from config import __DATABASE_PATH


# Connect to DB to get a list of the artifacts
def get_artifacts_list():
    with closing(sqlite3.connect(__DATABASE_PATH)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT path FROM artifacts;").fetchall()
            return rows


def get_artifact_list():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    fetched_data = database.artifact_list(cur)
    con.close()

    return {artifact[0] for artifact in fetched_data}


# Getting Artifacts based on CONF_FILE
# TODO: Artifacts probably have to be specifically copied instead of all at once
def get_artifacts(art_path, dump_dir):
    try:
        # Use Copy 2 to preserve metadata
        # https://docs.python.org/3/library/shutil.html
        shutil.copy2(art_path, dump_dir)
        print(f"Copied: {art_path}")
    except OSError:
        print(f"Error: {art_path}")
