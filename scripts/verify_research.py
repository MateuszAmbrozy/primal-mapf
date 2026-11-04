"""Verify published experiment files and count measurement rows."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify():
    research = ROOT / "research"
    records = json.loads((research / "checksums.json").read_text())
    files = {path.relative_to(research).as_posix()
             for folder in ("results", "fine_tuning")
             for path in (research / folder).rglob("*") if path.is_file()}
    if files != set(records):
        raise ValueError("Experiment files differ from research/checksums.json")
    measurements = 0
    for name, expected in records.items():
        path = research / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Experiment checksum mismatch: {path}")
        if path.suffix == ".csv":
            with path.open(newline="") as stream:
                measurements += sum(1 for _ in csv.DictReader(stream))
    print(f"Verified {len(records)} experiment files and {measurements} measurement rows.")
    return len(records), measurements


if __name__ == "__main__":
    verify()
