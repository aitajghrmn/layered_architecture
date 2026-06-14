"""
============================================================
MAIN ENTRY POINT — app.py
============================================================
This file is the "top" of the application.
It imports only the Presentation Layer and drives the demo.

In a real app, this is where you would hook up a web framework
(Flask, FastAPI), a CLI library, or a UI event loop.

Notice: app.py does NOT import dal, validator, or service.
Each layer only talks to the layer directly below it.
============================================================
"""

from layers import layer4_presentation as ui

print("=== Layered Architecture Demo ===\n")

# ── DEMO SEQUENCE ──────────────────────────────────────────

# 1. Try to add a valid entry
print("1) Adding a valid entry...")
ui.display_add_entry("Alice", "This is a perfectly fine message that follows all the rules.")

print()

# 2. Try to add an entry with a forbidden word
print("2) Adding an entry with a forbidden word...")
ui.display_add_entry("Bob", "This message contains spam content inside it.")

print()

# 3. Try to add an entry with text that is too short
print("3) Adding an entry with text that is too short...")
ui.display_add_entry("Charlie", "Hi.")

print()

# 4. List all stored entries
print("4) Listing all entries...")
ui.display_all_entries()

print()

# 5. Add a second valid entry
print("5) Adding a second valid entry...")
ui.display_add_entry("Diana", "Another thoughtful and well-written message for the database.")

print()

# 6. List all entries again
print("6) Listing all entries again...")
ui.display_all_entries()
