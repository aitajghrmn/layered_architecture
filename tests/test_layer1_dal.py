"""
============================================================
TESTS — Layer 1: Data Access Layer
============================================================
Run with:  python tests/test_layer1_dal.py

Each test calls a DAL function directly and checks the result.
IMPORTANT: These tests write to the real database.json file.
The setup step resets the database to a clean state first.
============================================================
"""

import sys
import os
import json

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from layers import layer1_data_access as dal

# ─────────────────────────────────────────────
# TEST RUNNER HELPER
# ─────────────────────────────────────────────

passed = 0
failed = 0

def assert_that(label: str, condition: bool) -> None:
    global passed, failed
    if condition:
        print(f"  ✅ PASS — {label}")
        passed += 1
    else:
        print(f"  ❌ FAIL — {label}")
        failed += 1

# ─────────────────────────────────────────────
# SETUP: Reset the database before tests
# ─────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/database.json")
with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump({"entries": []}, f, indent=2)
print("🔄 Database reset to empty state.\n")

# ─────────────────────────────────────────────
# TEST 1 — get_all_entries on empty database
# ─────────────────────────────────────────────

print("TEST 1: get_all_entries() on empty database")
all_empty = dal.get_all_entries()
assert_that("Returns a list", isinstance(all_empty, list))
assert_that("List is empty", len(all_empty) == 0)
print()

# ─────────────────────────────────────────────
# TEST 2 — save_entry adds a record
# ─────────────────────────────────────────────

print("TEST 2: save_entry() stores a new entry")
test_entry = {
    "id": "test_001",
    "name": "Test User",
    "text": "Hello from the test suite.",
    "created_at": "2024-01-01T00:00:00Z",
}
saved = dal.save_entry(test_entry)
assert_that("Returns the saved entry", saved is not None)
assert_that("Saved entry has correct id", saved["id"] == "test_001")
assert_that("Saved entry has correct name", saved["name"] == "Test User")
print()

# ─────────────────────────────────────────────
# TEST 3 — get_all_entries returns the saved entry
# ─────────────────────────────────────────────

print("TEST 3: get_all_entries() after saving one entry")
all_after_save = dal.get_all_entries()
assert_that("List has 1 entry", len(all_after_save) == 1)
assert_that("Entry name matches", all_after_save[0]["name"] == "Test User")
print()

# ─────────────────────────────────────────────
# TEST 4 — get_entry_by_id finds the correct entry
# ─────────────────────────────────────────────

print("TEST 4: get_entry_by_id()")
found = dal.get_entry_by_id("test_001")
assert_that("Found entry is not None", found is not None)
assert_that("Found entry id is correct", found["id"] == "test_001")

not_found = dal.get_entry_by_id("nonexistent_id")
assert_that("Returns None for unknown id", not_found is None)
print()

# ─────────────────────────────────────────────
# TEST 5 — save_entry adds multiple records
# ─────────────────────────────────────────────

print("TEST 5: save_entry() multiple times")
dal.save_entry({"id": "test_002", "name": "Second", "text": "Second entry", "created_at": "2024-01-01T00:00:00Z"})
dal.save_entry({"id": "test_003", "name": "Third",  "text": "Third entry",  "created_at": "2024-01-01T00:00:00Z"})
all_three = dal.get_all_entries()
assert_that("Database now has 3 entries", len(all_three) == 3)
print()

# ─────────────────────────────────────────────
# TEST 6 — delete_entry removes the right entry
# ─────────────────────────────────────────────

print("TEST 6: delete_entry()")
deleted = dal.delete_entry("test_002")
assert_that("delete_entry returns True for existing id", deleted is True)
after_delete = dal.get_all_entries()
assert_that("List now has 2 entries", len(after_delete) == 2)
assert_that("Deleted entry is gone", all(e["id"] != "test_002" for e in after_delete))

deleted_missing = dal.delete_entry("does_not_exist")
assert_that("delete_entry returns False for unknown id", deleted_missing is False)
print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All Layer 1 tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in layer1_data_access.py")
