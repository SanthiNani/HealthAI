import json
import os
from datetime import datetime

PATIENT_DB = "data/patients.json"
LOG_FILE = "logs/system.log"

def log_event(event_type, message, to_file=True):
    """
    Log a message with timestamp and event type.
    Optionally write to a log file as well.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{event_type.upper()}] {timestamp} - {message}"
    print(formatted)

    if to_file:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(formatted + "\n")

def load_patient_db():
    """
    Load the entire patient database from a JSON file.
    Returns an empty dict if not found or corrupted.
    """
    if not os.path.exists(PATIENT_DB):
        log_event("warning", f"{PATIENT_DB} not found. Returning empty database.")
        return {}

    try:
        with open(PATIENT_DB, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        log_event("error", f"Corrupted JSON in {PATIENT_DB}. Returning empty database.")
        return {}

def save_patient_db(patient_id, patient_record):
    """Update a single patient's data in the JSON DB."""
    os.makedirs(os.path.dirname(PATIENT_DB), exist_ok=True)

    # Load full database
    if os.path.exists(PATIENT_DB):
        with open(PATIENT_DB, "r") as f:
            db = json.load(f)
    else:
        db = {}

    db[patient_id] = patient_record  # ✅ Correct usage now

    # Save back updated DB
    with open(PATIENT_DB, "w") as f:
        json.dump(db, f, indent=4)


def update_patient_record(patient_id, new_data, metadata=None):
    """
    Add or update a patient record.
    If patient exists, appends a new visit and updates metadata.
    Otherwise, creates a new record.
    """
    db = load_patient_db()

    if patient_id not in db:
        db[patient_id] = {
            "metadata": metadata if metadata else {},
            "visits": []
        }
        log_event("info", f"Created new patient record: {patient_id}")
    else:
        if metadata:
            db[patient_id]["metadata"].update(metadata)
            log_event("info", f"Updated metadata for: {patient_id}")

    new_data["timestamp"] = datetime.now().isoformat()
    db[patient_id]["visits"].append(new_data)

    save_patient_db(patient_id, db[patient_id])  # ✅ FIXED here
    log_event("info", f"Recorded new visit for: {patient_id}")


def get_patient_record(patient_id):
    """Get the full patient record: metadata and visit history."""
    db = load_patient_db()
    return db.get(patient_id, {})

def get_patient_history(patient_id):
    """Retrieve only visit history for a given patient ID."""
    return get_patient_record(patient_id).get("visits", [])

def get_all_patient_ids():
    """List all registered patient IDs."""
    return list(load_patient_db().keys())

def get_patient_metadata(patient_id):
    """Get personal metadata (name, age, gender, etc.) for a patient."""
    return get_patient_record(patient_id).get("metadata", {})
