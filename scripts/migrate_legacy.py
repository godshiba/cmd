#!/usr/bin/env python3
"""One-time move of root data/*.json into data/legacy/ (idempotent)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "data" / "legacy"
NAMES = ("categories.json", "useful_system.json")


def main():
    LEGACY.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        src = ROOT / "data" / name
        dst = LEGACY / name
        if src.is_file() and not dst.exists():
            os.replace(src, dst)
            print(f"moved {name}")
        elif dst.is_file():
            print(f"ok {name}")
        else:
            print(f"missing {name}")


if __name__ == "__main__":
    main()
    print("migrate_legacy: done", flush=True)