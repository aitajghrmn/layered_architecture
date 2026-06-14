"""
============================================================
LAYER 4 — PRESENTATION LAYER
============================================================
Responsibility: Formats and displays information to the user.
It is the only layer that "talks" to the console (or a UI).

This layer calls the Service Layer to get results,
then formats those results into readable output.

It knows NOTHING about databases, validation rules, or IDs.
It just takes what the Service gives it and makes it readable.
============================================================
"""

from layers import layer3_service as service


# ─────────────────────────────────────────────
# DISPLAY HELPERS (internal — use _ prefix convention)
# ─────────────────────────────────────────────

def _print_entry(entry: dict) -> None:
    """
    Prints a formatted entry dictionary to the console.

    Args:
        entry (dict): An entry with keys: id, name, text, created_at.

    TODO:
        Print each field in a readable way, for example:
            print("─" * 40)
            print(f"ID:         {entry['id']}")
            print(f"Name:       {entry['name']}")
            print(f"Text:       {entry['text']}")
            print(f"Created at: {entry['created_at']}")
            print("─" * 40)
    """
    print("─" * 40)
    print(f"ID:         {entry['id']}")
    print(f"Name:       {entry['name']}")
    print(f"Text:       {entry['text']}")
    print(f"Created at: {entry['created_at']}")
    print("─" * 40)


# ─────────────────────────────────────────────
# USER-FACING ACTIONS
# ─────────────────────────────────────────────

def display_add_entry(name: str, text: str) -> None:
    """
    Handles the "add entry" action for the user.
    Calls the service, then reports success or failure.

    Args:
        name (str): The author's name.
        text (str): The content text.

    TODO:
        - Call service.add_entry(name, text)
        - If result["success"] is False:
              print("❌ Failed to add entry: " + result["error"])
        - If result["success"] is True:
              print("✅ Entry added successfully!")
              Call _print_entry(result["data"])
    """
    result = service.add_entry(name, text)
    if result["success"] is False:
        print("❌ Failed to add entry: " + result["error"])
    else:
        print("✅ Entry added successfully!")
        _print_entry(result["data"])


def display_all_entries() -> None:
    """
    Handles the "list all entries" action for the user.
    Prints all entries, or a friendly "no entries" message.

    TODO:
        - Call service.list_entries()
        - If result["data"] is empty (len == 0):
              print("📭 No entries found.")
        - Otherwise:
              print(f"📋 Found {len(result['data'])} entry/entries:\n")
              Loop over result["data"] and call _print_entry() for each one.
    """
    result = service.list_entries()
    if len(result["data"]) == 0:
        print("📭 No entries found.")
    else:
        print(f"📋 Found {len(result['data'])} entry/entries:\n")
        for entry in result["data"]:
            _print_entry(entry)


def display_entry(entry_id: str) -> None:
    """
    Handles the "get single entry" action for the user.

    Args:
        entry_id (str): The id of the entry to display.

    TODO:
        - Call service.get_entry(entry_id)
        - If result["success"] is False:
              print("❌ " + result["error"])
        - Otherwise:
              Call _print_entry(result["data"])
    """
    result = service.get_entry(entry_id)
    if result["success"] is False:
        print("❌ " + result["error"])
    else:
        _print_entry(result["data"])


def display_remove_entry(entry_id: str) -> None:
    """
    Handles the "delete entry" action for the user.

    Args:
        entry_id (str): The id of the entry to delete.

    TODO:
        - Call service.remove_entry(entry_id)
        - If result["success"] is False:
              print("❌ " + result["error"])
        - Otherwise:
              print("🗑️  Entry deleted successfully.")
    """
    result = service.remove_entry(entry_id)
    if result["success"] is False:
        print("❌ " + result["error"])
    else:
        print("🗑️  Entry deleted successfully.")