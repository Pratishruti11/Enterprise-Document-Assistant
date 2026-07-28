import json
import os

INDEX_FILE = "data/indexed_files.json"


def load_indexed_files():

    if not os.path.exists(INDEX_FILE):
        return {}

    with open(INDEX_FILE, "r") as f:
        return json.load(f)


def save_indexed_files(indexed_files):

    with open(INDEX_FILE, "w") as f:
        json.dump(indexed_files, f, indent=4)