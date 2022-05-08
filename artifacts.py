import sqlite3
import shutil
import database
import sqlite3
from contextlib import closing
from config import __ARTIFACTS_LIST


# Connect to DB to get a list of the artifacts
import nidaba_utils


def get_artifact_list():
    artifacts = nidaba_utils.get_json(__ARTIFACTS_LIST)
    print(artifacts)


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
