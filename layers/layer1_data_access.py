"""
============================================================
LAYER 1 — DATA ACCESS LAYER (DAL)
============================================================
Responsibility: Reads from and writes to the database (database.json).
This layer knows NOTHING about business rules or presentation.
It only handles raw data operations.

Think of it like a librarian: it fetches or stores a book,
but does not decide whether the book is appropriate.
============================================================
"""

import json
import os

# Path to our JSON "database"
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/database.json")


# ─────────────────────────────────────────────
# HELPERS (internal — use _ prefix convention)
# ─────────────────────────────────────────────

def _read_database() -> dict:
    """
    Reads the entire database file and returns the parsed dictionary.

    Returns:
        dict: The full database object, e.g. {"entries": [...]}

    TODO:
        - Open the file at DB_PATH in read mode with encoding="utf-8"
        - Parse the file contents with json.load()
        - Return the resulting dictionary
    """
    with open(DB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _write_database(data: dict) -> None:
    """
    Writes a Python dictionary back to the database file as formatted JSON.

    Args:
        data (dict): The full database object to save, e.g. {"entries": [...]}

    TODO:
        - Open the file at DB_PATH in write mode with encoding="utf-8"
        - Use json.dump() with indent=2 to write the data
    """
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def get_all_entries() -> list:
    """
    Retrievals all entries from the database.

    Returns:
        list: A list of entry dicts, each with keys: id, name, text, created_at.

    TODO:
        - Call _read_database() to get the full database dict
        - Return the value at key "entries"
    """
    db = _read_database()
    return db["entries"]


def get_entry_by_id(entry_id: str) -> dict | None:
    """
    Finds a single entry by its unique id.

    Args:
        entry_id (str): The id to search for.

    Returns:
        dict | None: The matching entry dict, or None if not found.

    TODO:
        - Call get_all_entries() to get the list
        - Use a for loop (or next() with a generator) to find the entry
          whose "id" key matches entry_id
        - Return the entry if found, or None if not found
    """
    entries = get_all_entries()
    for entry in entries:
        if entry["id"] == entry_id:
            return entry
    return None


def save_entry(entry: dict) -> dict:
    """
    Saves a new entry dictionary to the database.
    The entry is expected to already have: id, name, text, created_at.

    Args:
        entry (dict): The entry to save.

    Returns:
        dict: The same entry that was saved.

    TODO:
        - Call _read_database() to get the current database
        - Append the new entry to db["entries"]
        - Call _write_database() with the updated database
        - Return the saved entry
    """
    db = _read_database()
    db["entries"].append(entry)
    _write_database(db)
    return entry


def delete_entry(entry_id: str) -> bool:
    """
    Deletes an entry from the database by id.

    Args:
        entry_id (str): The id of the entry to delete.

    Returns:
        bool: True if an entry was deleted, False if it was not found.

    TODO:
        - Call _read_database() to get the current database
        - Filter out the entry with the matching id using a list comprehension:
            [e for e in db["entries"] if e["id"] != entry_id]
        - If the length didn't change, return False (nothing was deleted)
        - Otherwise update db["entries"] with the filtered list,
          call _write_database(), and return True
    """
    db = _read_database()
    original_length = len(db["entries"])
    
    filtered_entries = [e for e in db["entries"] if e["id"] != entry_id]
    
    if len(filtered_entries) == original_length:
        return False
        
    db["entries"] = filtered_entries
    _write_database(db)
    return True