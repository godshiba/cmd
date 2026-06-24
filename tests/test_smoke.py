import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_TEST_HOME = tempfile.mkdtemp(prefix="cmd-test-")
os.environ["CMD_HOME"] = _TEST_HOME
if not os.environ.get("CMD_SCRATCH"):
    os.environ["CMD_SCRATCH"] = str(ROOT / ".verify-scratch")
sys.path.insert(0, str(ROOT))

_TEST_ENV = {**os.environ, "CMD_HOME": _TEST_HOME, "CMD_USE_INPROCESS": "1"}

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
        for loc in LOCALES:
            data = json.loads((LOCALE_DIR / loc / "ui.json").read_text(encoding="utf-8"))
            self.assertIsInstance(data.get("help.usage_lines"), list)
            self.assertGreaterEqual(len(data["help.usage_lines"]), 10)


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
        essential_names = {c["name"].lower() for c in load_essential()}
        useful_only = sum(
            1
            for u in load_useful_system()
            if u["name"].lower() not in essential_names
        )
        expected = ESSENTIAL_COUNT + useful_only
        self.assertEqual(len(entries), expected)
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


class TestDocsConsistency(unittest.TestCase):
    def test_readme_version_matches_file(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"# {version}", readme)
        self.assertNotIn("# 1.0.0", readme)

    def test_changelog_has_no_v1_release(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("[0.0.1]", changelog)
        self.assertNotIn("[1.0.0]", changelog)
        self.assertNotIn("releases/tag/v1.0.0", changelog)

    def test_help_no_cmd_copy_subcommand(self):
        import main

        set_locale("en")
        help_text = main.build_help()
        self.assertIn("cmd <query>", help_text)
        self.assertNotIn("cmd copy", help_text)
        self.assertIn("cmd --copy", help_text)

    def test_help_localized_ru(self):
        import main

        set_locale("ru")
        help_text = main.build_help()
        self.assertIn("навигатор по командам", help_text)
        self.assertIn("браузер fzf", help_text)
        self.assertIn("карточка команды", help_text)

    def test_help_localized_zh(self):
        import main

        set_locale("zh")
        help_text = main.build_help()
        self.assertIn("终端命令导航器", help_text)
        self.assertIn("fzf 浏览器", help_text)

    def test_legacy_data_doc_exists(self):
        self.assertTrue((ROOT / "data" / "LEGACY.md").exists())

    def test_legacy_doc_matches_migration_script(self):
        text = (ROOT / "data" / "LEGACY.md").read_text(encoding="utf-8")
        self.assertIn("migrate_legacy.py", text)
        self.assertNotIn("On first import", text)

    def test_paths_legacy_constants(self):
        from lib.paths import CATEGORIES_PATH, ESSENTIAL_PATH, USEFUL_PATH

        self.assertTrue(Path(ESSENTIAL_PATH).exists())
        self.assertTrue(Path(CATEGORIES_PATH).exists())
        self.assertTrue(Path(USEFUL_PATH).exists())
        self.assertIn("/legacy/", CATEGORIES_PATH)
        self.assertIn("/legacy/", USEFUL_PATH)
        self.assertIn("/locales/ru/", ESSENTIAL_PATH)


def _run_cmd(argv, env=None):
    run_env = env or _TEST_ENV
    if run_env.get("CMD_USE_INPROCESS"):
        import io
        from contextlib import redirect_stderr, redirect_stdout

        saved_argv = sys.argv[:]
        saved_env = os.environ.copy()
        os.environ.update(run_env)
        sys.argv = ["main.py", *argv]
        out, err = io.StringIO(), io.StringIO()
        try:
            if str(ROOT) not in sys.path:
                sys.path.insert(0, str(ROOT))
            if "main" in sys.modules:
                del sys.modules["main"]
            import main as main_mod

            with redirect_stdout(out), redirect_stderr(err):
                rc = main_mod.main()
            return subprocess.CompletedProcess(
                [str(ROOT / "cmd"), *argv], rc or 0, out.getvalue(), err.getvalue()
            )
        finally:
            sys.argv = saved_argv
            os.environ.clear()
            os.environ.update(saved_env)
    return subprocess.run(
        [str(ROOT / "cmd"), *argv],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=run_env,
    )


class TestCLI(unittest.TestCase):
    def test_cmd_version(self):
        result = _run_cmd(["--version"])
        self.assertEqual(result.returncode, 0)
        self.assertIn(f"cmd {get_version()}", result.stdout)

    def test_cmd_help(self):
        result = _run_cmd(["--help"], env={**_TEST_ENV, "CMD_LANG": "en"})
        self.assertEqual(result.returncode, 0)
        self.assertIn("terminal command navigator", result.stdout)
        self.assertIn("cmd <query>", result.stdout)
        self.assertNotIn("cmd copy", result.stdout)

    def test_cmd_ls_essential(self):
        result = _run_cmd(["ls"], env={**_TEST_ENV, "CMD_LANG": "en"})
        self.assertEqual(result.returncode, 0)
        self.assertIn("ls", result.stdout)

    def test_cmd_help_ru_localized(self):
        result = _run_cmd(["--help"], env={**_TEST_ENV, "CMD_LANG": "ru"})
        self.assertEqual(result.returncode, 0)
        self.assertIn("браузер fzf", result.stdout)
        self.assertIn("навигатор по командам", result.stdout)
        self.assertNotIn("cmd copy", result.stdout)

    def test_cmd_lang_direct(self):
        result = _run_cmd(["lang", "en"])
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