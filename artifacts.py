#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
# artifacts.py
import getpass
import logging
import shutil
import traceback

from config import __ARTIFACTS_LIST, __TRIAGE, __ALL
# Connect to DB to get a list of the artifacts
import nidaba_utils
USERS = nidaba_utils.get_users()


def collect_artifacts(c_type, path):
    artifact_list = nidaba_utils.get_json(__ARTIFACTS_LIST)
    print(f"Collecting {c_type} Type Artifacts")

    artifacts_2_collect = []

    users = nidaba_utils.get_users()
    for artifact in artifact_list:
        if c_type is 0:
            if artifact in __TRIAGE:
                #print(f"Artifact - {artifact} - being copied\n")
                path = artifacts_2_collect.append(extract_artifact_paths(artifact_list[artifact].values(), path))
                print(f"Triage paths: {path}")
        elif c_type is 1:
            if artifact in __ALL:
                #print(f"Artifact - {artifact} - being copied")
                path = artifacts_2_collect.append(extract_artifact_paths(artifact_list[artifact].values(), path))
                print(f"Comprehensive paths: {path}")
        else:
            logging.error(f"Unknown collection type supplied, aborting")
    print(f"Complete Collection: {artifacts_2_collect}")


def extract_artifact_paths(artifacts, dump_dir):
    for value in artifacts:
        if isinstance(value, list):
            extract_artifact_paths(value, dump_dir)
        elif isinstance(value, dict):
            extract_artifact_paths(value.values(), dump_dir)
        elif isinstance(value, str):
            print(value)
            return value
        else:
            logging.debug(f"Unexpected Type found, check your artifact list.")


def copy_artifacts(art_path, dump_dir):
    # Use Copy 2 to preserve metadata
    # https://docs.python.org/3/library/shutil.html
    if "/Users/*/" in art_path:
        for user in USERS:
            original = "/Users/*/"
            new_path = art_path.replace(original, "/Users/" + user + "/")
    else:
        new_path = art_path
        print(f"Copying {new_path}")
    try:
        shutil.copy2(new_path, dump_dir)
    except OSError:
        logging.error(f"\tCould not get file {new_path}, Error: {OSError}")
