"""
============================================================
TESTS — Layer 3: Service Layer
============================================================
Run with:  python tests/test_layer3_service.py

The Service Layer coordinates Layer 1 and Layer 2.
These tests verify that the orchestration is correct:
  - Bad input gets rejected (validator is called)
  - Good input gets saved (DAL is called)
  - Returned dicts have the right shape
============================================================
"""

import sys
import os
import json

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from layers import layer3_service as service

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
print("🔄 Database reset.\n")

# ─────────────────────────────────────────────
# TEST 1 — add_entry with valid data
# ─────────────────────────────────────────────

print("TEST 1: add_entry() with valid input")
result1 = service.add_entry("Alice", "This is a perfectly valid entry that should be saved.")
assert_that("success is True", result1["success"] is True)
assert_that("data is present", "data" in result1)
assert_that("data['id'] is a string", isinstance(result1["data"]["id"], str))
assert_that("data['name'] is correct", result1["data"]["name"] == "Alice")
assert_that("data['text'] is correct", result1["data"]["text"] == "This is a perfectly valid entry that should be saved.")
assert_that("data['created_at'] is a string", isinstance(result1["data"]["created_at"], str))
assert_that("no 'error' key in result", "error" not in result1)
print()

# ─────────────────────────────────────────────
# TEST 2 — add_entry with invalid name
# ─────────────────────────────────────────────

print("TEST 2: add_entry() with empty name")
result2 = service.add_entry("", "This is a valid message but the name is empty.")
assert_that("success is False", result2["success"] is False)
assert_that("error message is a string", isinstance(result2["error"], str))
assert_that("no 'data' key in result", "data" not in result2)
print()

# ─────────────────────────────────────────────
# TEST 3 — add_entry with forbidden word
# ─────────────────────────────────────────────

print("TEST 3: add_entry() with forbidden word in text")
result3 = service.add_entry("Bob", "This message has a spam word inside it which is not allowed.")
assert_that("success is False", result3["success"] is False)
assert_that("error message is a string", isinstance(result3["error"], str))
print()

# ─────────────────────────────────────────────
# TEST 4 — list_entries returns only valid entries
# ─────────────────────────────────────────────

print("TEST 4: list_entries() returns saved entries")
result4 = service.list_entries()
assert_that("success is True", result4["success"] is True)
assert_that("data is a list", isinstance(result4["data"], list))
assert_that("only 1 entry was saved (the valid one)", len(result4["data"]) == 1)
print()

# ─────────────────────────────────────────────
# TEST 5 — get_entry finds a specific entry
# ─────────────────────────────────────────────

print("TEST 5: get_entry() by id")
saved_id = result1["data"]["id"]
result5 = service.get_entry(saved_id)
assert_that("success is True", result5["success"] is True)
assert_that("data['id'] matches", result5["data"]["id"] == saved_id)

result5b = service.get_entry("nonexistent_id")
assert_that("Returns failure for unknown id", result5b["success"] is False)
assert_that("Error message is a string", isinstance(result5b["error"], str))
print()

# ─────────────────────────────────────────────
# TEST 6 — remove_entry deletes correctly
# ─────────────────────────────────────────────

print("TEST 6: remove_entry() by id")
result6 = service.remove_entry(saved_id)
assert_that("success is True", result6["success"] is True)

# Verify it's gone
result6b = service.get_entry(saved_id)
assert_that("Entry no longer retrievable after deletion", result6b["success"] is False)

result6c = service.remove_entry("already_gone")
assert_that("Deleting nonexistent id returns failure", result6c["success"] is False)
print()

# ─────────────────────────────────────────────
# TEST 7 — list_entries is empty after deletion
# ─────────────────────────────────────────────

print("TEST 7: list_entries() after deletion")
result7 = service.list_entries()
assert_that("success is True", result7["success"] is True)
assert_that("data list is empty", len(result7["data"]) == 0)
print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All Layer 3 tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in layer3_service.py")
