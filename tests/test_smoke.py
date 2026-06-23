import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_TEST_HOME = tempfile.mkdtemp(prefix="cmd-test-")
os.environ["CMD_HOME"] = _TEST_HOME

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_TEST_ENV = {**os.environ, "CMD_HOME": _TEST_HOME}

from lib.display import format_card, format_browser_line  # noqa: E402
from lib.i18n import get_locale, set_locale, t, load_ui  # noqa: E402
from lib.lookup import (  # noqa: E402
    browser_entries,
    load_essential,
    load_useful_system,
    resolve,
    search,
)
from lib.version import get_version  # noqa: E402

LOCALES = ("en", "ru", "zh")
LOCALE_DIR = ROOT / "data" / "locales"
ESSENTIAL_COUNT = 32
USEFUL_COUNT = 76


class TestVersion(unittest.TestCase):
    def test_version_file_matches_get_version(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(get_version(), version)
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")


class TestLocaleData(unittest.TestCase):
    def test_all_locale_files_exist(self):
        for loc in LOCALES:
            for name in ("essential.json", "useful_system.json", "categories.json", "ui.json"):
                self.assertTrue((LOCALE_DIR / loc / name).exists(), f"missing {loc}/{name}")

    def test_essential_counts_match(self):
        for loc in LOCALES:
            data = json.loads((LOCALE_DIR / loc / "essential.json").read_text(encoding="utf-8"))
            self.assertEqual(len(data), ESSENTIAL_COUNT, loc)

    def test_useful_counts_match(self):
        for loc in LOCALES:
            data = json.loads((LOCALE_DIR / loc / "useful_system.json").read_text(encoding="utf-8"))
            self.assertEqual(len(data), USEFUL_COUNT, loc)

    def test_essential_names_match_across_locales(self):
        names = {}
        for loc in LOCALES:
            data = json.loads((LOCALE_DIR / loc / "essential.json").read_text(encoding="utf-8"))
            names[loc] = [c["name"] for c in data]
        self.assertEqual(names["en"], names["ru"])
        self.assertEqual(names["en"], names["zh"])

    def test_useful_names_match_across_locales(self):
        names = {}
        for loc in LOCALES:
            data = json.loads((LOCALE_DIR / loc / "useful_system.json").read_text(encoding="utf-8"))
            names[loc] = [c["name"] for c in data]
        self.assertEqual(names["en"], names["ru"])
        self.assertEqual(names["en"], names["zh"])

    def test_ui_keys_match_across_locales(self):
        keys = {}
        for loc in LOCALES:
            data = json.loads((LOCALE_DIR / loc / "ui.json").read_text(encoding="utf-8"))
            keys[loc] = set(data.keys())
        self.assertEqual(keys["en"], keys["ru"])
        self.assertEqual(keys["en"], keys["zh"])


class TestI18n(unittest.TestCase):
    def test_set_and_get_locale(self):
        for loc in LOCALES:
            set_locale(loc)
            self.assertEqual(get_locale(), loc)
            self.assertIn("card.what", load_ui(loc))

    def test_t_renders_known_key(self):
        set_locale("en")
        self.assertEqual(t("card.what"), "What it does")
        set_locale("ru")
        self.assertEqual(t("card.what"), "Что делает")


class TestLookup(unittest.TestCase):
    def test_resolve_essential_ls(self):
        for loc in LOCALES:
            set_locale(loc)
            card = resolve("ls")
            self.assertIsNotNone(card, loc)
            self.assertEqual(card["tier"], "essential")
            self.assertTrue(card.get("title"))

    def test_resolve_unknown_returns_none(self):
        set_locale("en")
        self.assertIsNone(resolve("zzz_nonexistent_cmd_xyz"))

    def test_search_finds_essential_by_name(self):
        set_locale("en")
        results = search("grep")
        names = [r["name"] for r in results]
        self.assertIn("grep", names)

    def test_search_finds_by_example_text(self):
        set_locale("en")
        results = search("docker")
        names = [r["name"] for r in results]
        self.assertIn("brew", names)

    def test_browser_entries_without_index(self):
        set_locale("en")
        entries = browser_entries([], show_all=False)
        self.assertGreaterEqual(len(entries), ESSENTIAL_COUNT + USEFUL_COUNT)
        tiers = {e["tier"] for e in entries}
        self.assertIn("essential", tiers)
        self.assertIn("useful", tiers)

    def test_load_counts_per_locale(self):
        for loc in LOCALES:
            set_locale(loc)
            self.assertEqual(len(load_essential()), ESSENTIAL_COUNT)
            self.assertEqual(len(load_useful_system()), USEFUL_COUNT)


class TestDisplay(unittest.TestCase):
    def test_format_card_and_browser_line(self):
        set_locale("en")
        card = resolve("ls")
        text = format_card(card)
        self.assertIn("ls", text)
        self.assertIn("What it does", text)
        line = format_browser_line(card)
        self.assertIn("\t", line)
        self.assertIn("ls", line)


class TestCLI(unittest.TestCase):
    def test_cmd_version(self):
        result = subprocess.run(
            [str(ROOT / "cmd"), "--version"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env=_TEST_ENV,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn(f"cmd {get_version()}", result.stdout)

    def test_cmd_help(self):
        result = subprocess.run(
            [str(ROOT / "cmd"), "--help"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={**_TEST_ENV, "CMD_LANG": "en"},
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("terminal command navigator", result.stdout)

    def test_cmd_ls_essential(self):
        result = subprocess.run(
            [str(ROOT / "cmd"), "ls"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={**_TEST_ENV, "CMD_LANG": "en"},
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("ls", result.stdout)

    def test_cmd_lang_direct(self):
        result = subprocess.run(
            [str(ROOT / "cmd"), "lang", "en"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env=_TEST_ENV,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("English", result.stdout)


class TestModulesImport(unittest.TestCase):
    def test_all_lib_modules_import(self):
        import lib.browser  # noqa: F401
        import lib.clipboard  # noqa: F401
        import lib.display  # noqa: F401
        import lib.examples  # noqa: F401
        import lib.fzf_util  # noqa: F401
        import lib.history  # noqa: F401
        import lib.i18n  # noqa: F401
        import lib.index  # noqa: F401
        import lib.lang_menu  # noqa: F401
        import lib.lookup  # noqa: F401
        import lib.paths  # noqa: F401
        import lib.version  # noqa: F401
        import main  # noqa: F401


if __name__ == "__main__":
    unittest.main()