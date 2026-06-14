"""
============================================================
LAYER 2 — VALIDATION LAYER
============================================================
Responsibility: Enforces rules about the DATA — not the database,
not the screen. Just: "Is this input acceptable?"

This layer has NO idea how data is stored or displayed.
It receives raw values, checks them, and returns a result dict.

Rules to enforce:
  - name must be a non-empty string (max 50 chars)
  - text must be a non-empty string (min 10, max 500 chars)
  - text must NOT contain forbidden words (case-insensitive)
============================================================
"""

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

# Words that are not allowed inside the text field
FORBIDDEN_WORDS = ["spam", "badword", "forbidden"]

# Text length limits
TEXT_MIN_LENGTH = 10
TEXT_MAX_LENGTH = 500

# Name length limit
NAME_MAX_LENGTH = 50


# ─────────────────────────────────────────────
# INDIVIDUAL VALIDATORS
# ─────────────────────────────────────────────

def validate_name(name: str) -> dict:
    """
    Checks that the name is a non-empty string within the length limit.

    Args:
        name (str): The name to validate.

    Returns:
        dict: {"valid": bool, "error": str | None}

    TODO:
        - If name is None or not a str → return {"valid": False, "error": "Name is required."}
        - If name.strip() == "" → return {"valid": False, "error": "Name cannot be blank."}
        - If len(name) > NAME_MAX_LENGTH → return {"valid": False, "error": f"Name must be {NAME_MAX_LENGTH} characters or fewer."}
        - If all checks pass → return {"valid": True, "error": None}
    """
    if name is None or not isinstance(name, str):
        return {"valid": False, "error": "Name is required."}
    if name.strip() == "":
        return {"valid": False, "error": "Name cannot be blank."}
    if len(name) > NAME_MAX_LENGTH:
        return {"valid": False, "error": f"Name must be {NAME_MAX_LENGTH} characters or fewer."}
    return {"valid": True, "error": None}


def validate_text_length(text: str) -> dict:
    """
    Checks that the text meets minimum and maximum length requirements.

    Args:
        text (str): The text to validate.

    Returns:
        dict: {"valid": bool, "error": str | None}

    TODO:
        - If text is None or not a str → return {"valid": False, "error": "Text is required."}
        - If len(text.strip()) < TEXT_MIN_LENGTH → return {"valid": False, "error": f"Text must be at least {TEXT_MIN_LENGTH} characters."}
        - If len(text) > TEXT_MAX_LENGTH → return {"valid": False, "error": f"Text must be {TEXT_MAX_LENGTH} characters or fewer."}
        - If all checks pass → return {"valid": True, "error": None}
    """
    if text is None or not isinstance(text, str):
        return {"valid": False, "error": "Text is required."}
    if len(text.strip()) < TEXT_MIN_LENGTH:
        return {"valid": False, "error": f"Text must be at least {TEXT_MIN_LENGTH} characters."}
    if len(text) > TEXT_MAX_LENGTH:
        return {"valid": False, "error": f"Text must be {TEXT_MAX_LENGTH} characters or fewer."}
    return {"valid": True, "error": None}


def validate_text_content(text: str) -> dict:
    """
    Checks that the text does not contain any forbidden words.
    The check must be case-insensitive.

    Args:
        text (str): The text to check.

    Returns:
        dict: {"valid": bool, "error": str | None, "found_word": str | None}

    TODO:
        - Convert text to lowercase: text_lower = text.lower()
        - Loop through FORBIDDEN_WORDS
        - If text_lower contains a forbidden word:
            return {"valid": False, "error": f'Text contains a forbidden word: "{word}".', "found_word": word}
        - If no forbidden words found:
            return {"valid": True, "error": None, "found_word": None}
    """
    text_lower = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            return {"valid": False, "error": f'Text contains a forbidden word: "{word}".', "found_word": word}
    return {"valid": True, "error": None, "found_word": None}


# ─────────────────────────────────────────────
# COMBINED VALIDATOR
# ─────────────────────────────────────────────

def validate_entry(name: str, text: str) -> dict:
    """
    Runs all validation checks on a name + text pair.
    Stops and returns on the first failure found.

    Args:
        name (str): The name to validate.
        text (str): The text to validate.

    Returns:
        dict: {"valid": bool, "error": str | None}

    TODO:
        - Call validate_name(name). If result["valid"] is False, return that result.
        - Call validate_text_length(text). If result["valid"] is False, return that result.
        - Call validate_text_content(text). If result["valid"] is False, return that result.
        - If everything passed → return {"valid": True, "error": None}
    """
    name_result = validate_name(name)
    if name_result["valid"] is False:
        return name_result

    length_result = validate_text_length(text)
    if length_result["valid"] is False:
        return length_result

    content_result = validate_text_content(text)
    if content_result["valid"] is False:
        return {"valid": False, "error": content_result["error"]}

    return {"valid": True, "error": None}