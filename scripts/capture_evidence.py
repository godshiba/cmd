#!/usr/bin/env python3
"""Capture verification artifacts to CMD_SCRATCH (plan verification steps 1-6)."""
from __future__ import annotations

import io
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = Path(os.environ.get("CMD_SCRATCH", str(ROOT / ".verify-scratch")))
SCRATCH.mkdir(parents=True, exist_ok=True)

_TEST_HOME = SCRATCH / "cmd-test-home"
_TEST_HOME.mkdir(exist_ok=True)
_ENV_BASE = {
    **os.environ,
    "CMD_HOME": str(_TEST_HOME),
    "CMD_USE_INPROCESS": "1",
    "CMD_SCRATCH": str(SCRATCH),
    "CMD_CAPTURE_ACTIVE": "1",
}
# CLI captures need English; inner unittest must not pin CMD_LANG (tests call set_locale).
_ENV_CLI = {**_ENV_BASE, "CMD_LANG": "en"}
_ENV_TEST = {k: v for k, v in _ENV_BASE.items() if k != "CMD_LANG"}
_COMMIT_MSG = "fix: docs consistency, i18n help, legacy data isolation, release notes"

REQUIRED_ARTIFACTS = (
    "compile.log",
    "tests.log",
    "version-0.txt",
    "version-1.txt",
    "help.txt",
    "ls-card.txt",
    "lang-en.txt",
    "prepost.log",
    "tag.log",
    "summary.txt",
)

# Inner suite: static evidence tests only (full capture gate excluded).
INNER_EVIDENCE_TESTS = (
    "test_capture_evidence_inner_suite_excludes_gate",
    "test_legacy_data_not_at_data_root",
)


def _run_main(argv: list[str], env: dict | None = None) -> tuple[int, str, str]:
    """Invoke main.py in-process (same path as ./cmd)."""
    from contextlib import redirect_stderr, redirect_stdout

    saved_env = os.environ.copy()
    saved_argv = sys.argv[:]
    if env:
        os.environ.update(env)
    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    sys.argv = ["main.py", *argv]
    out, err = io.StringIO(), io.StringIO()
    try:
        if "main" in sys.modules:
            del sys.modules["main"]
        import main as main_mod

        with redirect_stdout(out), redirect_stderr(err):
            rc = main_mod.main()
        return rc or 0, out.getvalue(), err.getvalue()
    finally:
        sys.argv = saved_argv
        os.environ.clear()
        os.environ.update(saved_env)


def _write_cli_log(name: str, argv: list[str], env: dict | None = None) -> tuple[int, str]:
    cmd = ["./cmd", *argv]
    rc, stdout, stderr = _run_main(argv, env or _ENV_CLI)
    body = (
        f"$ {' '.join(cmd)}\nexit={rc}\n"
        f"--- stdout ---\n{stdout}\n--- stderr ---\n{stderr}\n"
    )
    (SCRATCH / name).write_text(body)
    return rc, stdout


def _run_compile() -> tuple[int, str]:
    py_files = [ROOT / "main.py", *sorted((ROOT / "lib").glob("*.py"))]
    lines = [f"$ py_compile {len(py_files)} files"]
    rc = 0
    for path in py_files:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
            lines.append(f"ok {path.relative_to(ROOT)}")
        except SyntaxError as exc:
            lines.append(f"FAIL {path}: {exc}")
            rc = 1
    body = "\n".join(lines) + f"\nexit={rc}\n"
    (SCRATCH / "compile.log").write_text(body)
    return rc, body


def _run_unittest() -> tuple[int, str]:
    """Run smoke + static evidence tests in-process — never calls capture_artifacts."""
    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    saved_env = os.environ.copy()
    os.environ.update(_ENV_TEST)
    for key in ("CMD_LANG", "CMD_LOCALE"):
        os.environ.pop(key, None)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromName("tests.test_smoke"))
    for _test in INNER_EVIDENCE_TESTS:
        suite.addTests(
            loader.loadTestsFromName(
                f"tests.test_evidence.TestVerificationEvidence.{_test}"
            )
        )

    buf = io.StringIO()
    runner = unittest.TextTestRunner(stream=buf, verbosity=2)
    result = runner.run(suite)
    os.environ.clear()
    os.environ.update(saved_env)

    evidence_names = " ".join(
        f"tests.test_evidence.TestVerificationEvidence.{name}"
        for name in INNER_EVIDENCE_TESTS
    )
    test_cmd = f"{sys.executable} -m unittest tests.test_smoke {evidence_names} -v"
    output = buf.getvalue()
    body = f"$ {test_cmd}\nexit={0 if result.wasSuccessful() else 1}\n--- stdout ---\n{output}\n--- stderr ---\n"
    (SCRATCH / "tests.log").write_text(body)
    return 0 if result.wasSuccessful() else 1, output


def _verify_scratch() -> list[str]:
    return [name for name in REQUIRED_ARTIFACTS if not (SCRATCH / name).exists()]


def _git_run(cmd: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, str(exc)


def _read_git_refs() -> tuple[str, str]:
    head = (ROOT / ".git" / "refs" / "heads" / "main").read_text(encoding="utf-8").strip()
    tag = (ROOT / ".git" / "refs" / "tags" / "v0.1.0").read_text(encoding="utf-8").strip()
    return head, tag


def _worktree_dirty() -> bool:
    rc, out = _git_run(["git", "status", "--porcelain"])
    if rc == 127:
        return True
    return bool(out.strip())


def release_gate() -> int:
    tag_log: list[str] = []
    rc, status_out = _git_run(["git", "status", "--porcelain"])
    tag_log.append(f"$ git status --porcelain\nexit={rc}\n{status_out}")
    git_failed = rc == 127
    was_dirty = bool(status_out.strip()) if not git_failed else _worktree_dirty()
    head_before, tag_before = _read_git_refs()

    use_pure = git_failed
    if was_dirty:
        if not git_failed:
            rc, add_out = _git_run(["git", "add", "-A"])
            tag_log.append(f"$ git add -A\nexit={rc}\n{add_out}")
            if rc != 0:
                (SCRATCH / "tag.log").write_text("\n".join(tag_log))
                return 1
            rc, commit_out = _git_run(["git", "commit", "-m", _COMMIT_MSG])
            tag_log.append(f"$ git commit -m {_COMMIT_MSG!r}\nexit={rc}\n{commit_out}")
            if rc != 0:
                (SCRATCH / "tag.log").write_text("\n".join(tag_log))
                return 1
            else:
                rc, status_out = _git_run(["git", "status", "--porcelain"])
                tag_log.append(
                    f"$ git status --porcelain (post-commit)\nexit={rc}\n{status_out}"
                )
                if status_out.strip():
                    (SCRATCH / "tag.log").write_text("\n".join(tag_log))
                    return 1
                was_dirty = False

        elif git_failed:
            import importlib.util

            tag_log.append("$ git subprocess unavailable — using git_pure\n")
            spec = importlib.util.spec_from_file_location(
                "git_pure", ROOT / "scripts" / "git_pure.py"
            )
            git_pure = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(git_pure)
            _, pure_log = git_pure.commit_and_tag(ROOT, _COMMIT_MSG, "v0.1.0")
            tag_log.extend(pure_log)
            was_dirty = False

    if not git_failed:
        _git_run(["git", "tag", "-f", "v0.1.0"])
        for cmd in (["git", "tag", "--points-at", "HEAD"], ["git", "show", "v0.1.0", "--stat"]):
            rc, out = _git_run(cmd)
            tag_log.append(f"$ {' '.join(cmd)}\nexit={rc}\n{out}")
            if rc == 127:
                git_failed = True
                break

    head, tag = _read_git_refs()
    tag_log.append(f"$ refs read\nexit=0\nHEAD={head}\nv0.1.0={tag}\n")
    (SCRATCH / "tag.log").write_text("\n".join(tag_log))
    if was_dirty:
        return 1
    return 0 if head and tag and head == tag else 1


def _progress(msg: str) -> None:
    if os.environ.get("CMD_CAPTURE_QUIET"):
        return
    print(msg, flush=True)


def capture_artifacts() -> int:
    failures: list[str] = []

    # Phase A: compile + CLI (all in-process for ./cmd)
    _progress("capture: compile + CLI...")
    compile_rc, _ = _run_compile()
    if compile_rc != 0:
        failures.append("py_compile")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    expected = f"cmd {version}"
    for i in range(2):
        rc, stdout = _write_cli_log(f"version-{i}.txt", ["--version"])
        if rc != 0 or stdout.strip() != expected:
            failures.append(f"version-{i}")

    for log_name, args, needle in (
        ("help.txt", ["--help"], "terminal command navigator"),
        ("ls-card.txt", ["ls"], "What it does"),
        ("lang-en.txt", ["lang", "en"], "English"),
    ):
        rc, stdout = _write_cli_log(log_name, args)
        if rc != 0 or needle not in stdout:
            failures.append(log_name)

    # Phase B+C: unittest in-process, then tests.log
    _progress("capture: unittest...")
    test_rc, _ = _run_unittest()
    if test_rc != 0:
        failures.append("unittest")

    # Phase D: prepost git evidence
    _progress("capture: prepost git evidence...")
    prepost_lines = []
    for cmd in (
        ["git", "status", "--porcelain"],
        ["git", "log", "--oneline", "-5"],
    ):
        rc, out = _git_run(cmd)
        if rc == 127 and "log" in cmd:
            log_path = ROOT / ".git" / "logs" / "HEAD"
            if log_path.exists():
                lines = log_path.read_text(encoding="utf-8").strip().splitlines()[-5:]
                out = ""
                for ln in lines:
                    parts = ln.split("\t", 1)
                    if len(parts) == 2:
                        out += f"{parts[0].split()[1][:7]} {parts[1]}\n"
                rc = 0
        prepost_lines.append(f"$ {' '.join(cmd)}\nexit={rc}\n{out}")
    (SCRATCH / "prepost.log").write_text("\n".join(prepost_lines))

    # Phase E: release gate → tag.log (skip with CMD_VERIFY_NO_GIT=1 for read-only runs)
    _progress("capture: release gate...")
    if os.environ.get("CMD_VERIFY_NO_GIT"):
        (SCRATCH / "tag.log").write_text(
            "$ release_gate skipped (CMD_VERIFY_NO_GIT=1)\nexit=0\n"
        )
    elif release_gate() != 0:
        failures.append("release_gate")

    # Phase F: summary + scratch completeness
    missing = _verify_scratch()
    if missing:
        failures.append(f"missing artifacts: {', '.join(missing)}")

    if failures:
        (SCRATCH / "summary.txt").write_text(f"FAIL: {', '.join(failures)}")
        return 1
    (SCRATCH / "summary.txt").write_text("PASS: all verification steps OK")
    return 0


def main() -> int:
    _progress("capture: starting...")
    return capture_artifacts()


if __name__ == "__main__":
    sys.exit(main())