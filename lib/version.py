from pathlib import Path

_VERSION_FILE = Path(__file__).resolve().parent.parent / "VERSION"


def get_version():
    try:
        return _VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return "0.0.0"