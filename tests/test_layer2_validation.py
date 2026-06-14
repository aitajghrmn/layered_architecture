"""
============================================================
TESTS — Layer 2: Validation Layer
============================================================
Run with:  python tests/test_layer2_validation.py

These tests are pure — no file I/O, no database.
We just pass values in and check what comes out.
============================================================
"""

import sys
import os

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from layers import layer2_validation as v

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
# TEST BLOCK A — validate_name()
# ─────────────────────────────────────────────

print("TEST A: validate_name()")

r = v.validate_name("Alice")
assert_that("Valid name → valid: True", r["valid"] is True)
assert_that("Valid name → error: None", r["error"] is None)

r = v.validate_name("")
assert_that("Empty string is invalid", r["valid"] is False)
assert_that("Empty string has an error message", isinstance(r["error"], str))

r = v.validate_name("   ")
assert_that("Whitespace-only name is invalid", r["valid"] is False)

r = v.validate_name(None)
assert_that("None name is invalid", r["valid"] is False)

r = v.validate_name("A" * (v.NAME_MAX_LENGTH + 1))
assert_that(f"Name longer than {v.NAME_MAX_LENGTH} chars is invalid", r["valid"] is False)

r = v.validate_name("A" * v.NAME_MAX_LENGTH)
assert_that(f"Name of exactly {v.NAME_MAX_LENGTH} chars is valid", r["valid"] is True)

print()

# ─────────────────────────────────────────────
# TEST BLOCK B — validate_text_length()
# ─────────────────────────────────────────────

print("TEST B: validate_text_length()")

r = v.validate_text_length("This is a normal length message that fits easily.")
assert_that("Normal text is valid", r["valid"] is True)

r = v.validate_text_length("Short")
assert_that(f"Text shorter than {v.TEXT_MIN_LENGTH} chars is invalid", r["valid"] is False)

r = v.validate_text_length("x" * (v.TEXT_MAX_LENGTH + 1))
assert_that(f"Text longer than {v.TEXT_MAX_LENGTH} chars is invalid", r["valid"] is False)

r = v.validate_text_length("x" * v.TEXT_MIN_LENGTH)
assert_that(f"Text of exactly {v.TEXT_MIN_LENGTH} chars is valid", r["valid"] is True)

r = v.validate_text_length("")
assert_that("Empty string is invalid", r["valid"] is False)

r = v.validate_text_length(None)
assert_that("None text is invalid", r["valid"] is False)

print()

# ─────────────────────────────────────────────
# TEST BLOCK C — validate_text_content()
# ─────────────────────────────────────────────

print("TEST C: validate_text_content()")

r = v.validate_text_content("This is a perfectly clean and acceptable message.")
assert_that("Clean text is valid", r["valid"] is True)
assert_that("Clean text has found_word: None", r["found_word"] is None)

# Test each forbidden word from the config list
for word in v.FORBIDDEN_WORDS:
    r = v.validate_text_content(f"This message contains the word {word} inside it.")
    assert_that(f'Detects forbidden word "{word}"', r["valid"] is False)
    assert_that(f'found_word is "{word}"', r["found_word"] == word)

# Case-insensitivity check
r = v.validate_text_content("This message contains SPAM in uppercase.")
assert_that("Detection is case-insensitive (SPAM → spam)", r["valid"] is False)

print()

# ─────────────────────────────────────────────
# TEST BLOCK D — validate_entry() (combined)
# ─────────────────────────────────────────────

print("TEST D: validate_entry() — combined validator")

r = v.validate_entry("Alice", "This is a valid message that passes all checks.")
assert_that("Valid name + valid text → valid", r["valid"] is True)

r = v.validate_entry("", "This is a valid message that passes all checks.")
assert_that("Invalid name → fails", r["valid"] is False)

r = v.validate_entry("Alice", "Too short")
assert_that("Text too short → fails", r["valid"] is False)

r = v.validate_entry("Alice", "This message contains a forbidden spam word inside.")
assert_that("Forbidden word in text → fails", r["valid"] is False)

print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All Layer 2 tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in layer2_validation.py")
