# Layered Architecture — Teaching Project (Python)

## Project Goal
This project teaches **layered (n-tier) architecture** by building a small app where
students write the implementation of each function, guided by detailed TODO comments.

---

## Folder Structure

```
layered-app/
│
├── app.py                              ← Entry point. Runs a demo sequence.
│
├── data/
│   └── database.json                  ← The "database" (a JSON file)
│
├── layers/
│   ├── __init__.py
│   ├── layer1_data_access.py          ← Layer 1: reads/writes the database
│   ├── layer2_validation.py           ← Layer 2: checks if data is acceptable
│   ├── layer3_service.py              ← Layer 3: orchestrates layers 1 & 2
│   └── layer4_presentation.py         ← Layer 4: formats output for the user
│
└── tests/
    ├── __init__.py
    ├── test_layer1_dal.py             ← Tests for Layer 1
    ├── test_layer2_validation.py      ← Tests for Layer 2
    └── test_layer3_service.py         ← Tests for Layer 3
```

---

## The Architecture — How Each Layer Works

```
┌──────────────────────────────────┐
│   app.py  (Entry Point)          │  ← Starts the program
└──────────────┬───────────────────┘
               │ calls
┌──────────────▼───────────────────┐
│   LAYER 4: Presentation          │  ← Talks to the user (console / UI)
└──────────────┬───────────────────┘
               │ calls
┌──────────────▼───────────────────┐
│   LAYER 3: Service (Logic)       │  ← Knows the business rules
└──────┬───────────────────┬───────┘
       │ calls             │ calls
┌──────▼──────┐    ┌───────▼───────┐
│  LAYER 1:   │    │   LAYER 2:    │
│  Data Access│    │  Validation   │
└──────┬──────┘    └───────────────┘
       │ reads/writes
┌──────▼──────────────────────────┐
│        data/database.json        │
└─────────────────────────────────┘
```

### The Golden Rule
**Each layer only talks to the layer directly below it.**
- Layer 4 imports and calls Layer 3.
- Layer 3 imports and calls Layer 1 and Layer 2.
- Layer 1 reads/writes the JSON file.
- Layer 2 never touches any file.
- `app.py` only imports Layer 4.

---

## Layer Responsibilities

| Layer | File | Responsibility |
|-------|------|----------------|
| Layer 1 | `layer1_data_access.py` | Read and write `database.json`. No logic, no display. |
| Layer 2 | `layer2_validation.py` | Check if name and text follow the rules. No I/O at all. |
| Layer 3 | `layer3_service.py` | Validate first, then save (or list/delete). The "brain." |
| Layer 4 | `layer4_presentation.py` | Call Layer 3, then print the result nicely. |

---

## How to Run

### Run the demo (all layers working together)
```bash
python app.py
```

### Run individual layer tests
```bash
python tests/test_layer1_dal.py
python tests/test_layer2_validation.py
python tests/test_layer3_service.py
```

> **Note:** Run layer tests in order (1 → 2 → 3), since Layer 3 depends on 1 and 2.

---

## Student Workflow

Complete the layers in this order:

1. **Start with Layer 2** (`layer2_validation.py`)
   - Easiest: pure functions, no files, no imports needed.
   - Test with: `python tests/test_layer2_validation.py`

2. **Then Layer 1** (`layer1_data_access.py`)
   - Learn how to read/write JSON files with Python's `json` and `open()`.
   - Test with: `python tests/test_layer1_dal.py`

3. **Then Layer 3** (`layer3_service.py`)
   - Learn to call other modules and combine their results.
   - Test with: `python tests/test_layer3_service.py`

4. **Finally Layer 4** (`layer4_presentation.py`)
   - No test file — just run `python app.py` and see it all work!

---

## Validation Rules (Layer 2)

| Field | Rule |
|-------|------|
| `name` | Required, not blank, max 50 characters |
| `text` | Required, min 10 characters, max 500 characters |
| `text` | Must NOT contain: `spam`, `badword`, `forbidden` (case-insensitive) |

---

## Data Shape

Each entry stored in `database.json` looks like this:

```json
{
  "id": "entry_1713200000000_4821",
  "name": "Alice",
  "text": "This is a valid message.",
  "created_at": "2024-04-15T10:30:00Z"
}
```

---

## Why This Architecture?

| Benefit | Explanation |
|---------|-------------|
| **Separation of concerns** | Each file has one job. Changes in one layer don't break others. |
| **Testability** | Layer 2 can be tested with zero file system access. |
| **Replaceability** | Swap the JSON file for a real database — only Layer 1 changes. |
| **Readability** | A new developer can understand each layer independently. |
