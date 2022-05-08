#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# artifacts.py
import logging
import shutil
from config import __ARTIFACTS_LIST
# Connect to DB to get a list of the artifacts
import nidaba_utils


def collect_artifacts(c_type, path):

    if c_type is 0:
        print(f"Collecting Triage Artifacts Only")
        get_artifact_list("triage")
    elif c_type is 1:
        print(f"Collecting all possible artifacts")
        get_artifact_list("additional")
    else:
        logging.error(f"Unknown collection type supplied, aborting")
        exit(1)


def get_artifact_list(c_type):
    artifacts = nidaba_utils.get_json(__ARTIFACTS_LIST)
    print(artifacts[c_type])
    return artifacts


# Getting Artifacts based on CONF_FILE
# TODO: Artifacts probably have to be specifically copied instead of all at once
def copy_artifacts(art_path, dump_dir):
    try:
        # Use Copy 2 to preserve metadata
        # https://docs.python.org/3/library/shutil.html
        shutil.copy2(art_path, dump_dir)
        print(f"Copied: {art_path}")
    except OSError:
        print(f"Error: {art_path}")
