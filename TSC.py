#!/usr/bin/env python3
import re
import traceback
from pathlib import Path

INPUT_FILE = "trackers_clean.txt"
SCHEMES = r'(?:https?|udp|wss?|ftp)://'

def split_into_trackers(text: str) -> list[str]:
    raw_parts = re.split(f'(?={SCHEMES})', text)
    return [part.strip() for part in raw_parts if part.strip()]

def main() -> None:
    try:
        in_path = Path(INPUT_FILE)
        if not in_path.is_file():
            print(f"Error: {INPUT_FILE} not found in the current directory.")
            input("Press Enter to exit...")
            return

        original_lines = 0
        glued_lines = 0
        total_raw_trackers = 0
        seen = {}

        with in_path.open("r", encoding="utf-8", errors="replace") as f:
            first_line = True
            for line in f:
                stripped = line.strip()
                if first_line:
                    stripped = stripped.lstrip('\ufeff')
                    first_line = False
                if not stripped:
                    continue
                original_lines += 1
                trackers = split_into_trackers(stripped)
                total_raw_trackers += len(trackers)
                if len(trackers) > 1:
                    glued_lines += 1
                for tracker in trackers:
                    if tracker not in seen:
                        seen[tracker] = True

        unique_trackers = len(seen)
        duplicates_dropped = total_raw_trackers - unique_trackers

        with in_path.open("w", encoding="utf-8", newline="\n") as f:
            for tracker in seen:
                f.write(tracker + "\n")

        print("\n" + "="*50)
        print("Tracker Cleaning Summary")
        print("-"*50)
        print(f"Original non‑empty lines: {original_lines}")
        print(f"Lines with concatenated URLs: {glued_lines}")
        print(f"Total trackers before dedup: {total_raw_trackers}")
        print(f"Duplicate trackers removed: {duplicates_dropped}")
        print(f"Unique trackers written: {unique_trackers}")
        print("="*50)

    except Exception:
        print("\n" + "!"*50)
        print("CRASH REPORT")
        print("An unexpected error occurred:")
        print("-"*50)
        print(traceback.format_exc())
        print("!"*50)

    finally:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()