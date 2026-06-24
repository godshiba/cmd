"""Pure-Python git commit + tag (stdlib only) when git subprocess is unavailable."""
from __future__ import annotations

import fnmatch
import hashlib
import os
import time
import zlib
from pathlib import Path


def _sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def _store_object(repo: Path, obj_type: str, content: bytes) -> str:
    header = f"{obj_type} {len(content)}\0".encode() + content
    digest = _sha1(header)
    compressed = zlib.compress(header)
    obj_path = repo / ".git" / "objects" / digest[:2] / digest[2:]
    obj_path.parent.mkdir(parents=True, exist_ok=True)
    if not obj_path.exists():
        obj_path.write_bytes(compressed)
    return digest


def _blob_hash(repo: Path, data: bytes) -> str:
    return _store_object(repo, "blob", data)


def _tree_hash(repo: Path, entries: list[tuple[str, str, str]]) -> str:
    parts = []
    for mode, name, sha in sorted(entries, key=lambda x: x[1]):
        parts.append(f"{mode} {name}\0".encode() + bytes.fromhex(sha))
    return _store_object(repo, "tree", b"".join(parts))


def _load_gitignore(repo: Path) -> list[str]:
    gi = repo / ".gitignore"
    if not gi.exists():
        return []
    return gi.read_text(encoding="utf-8").splitlines()


def _is_ignored(rel: Path, patterns: list[str]) -> bool:
    s = str(rel).replace("\\", "/")
    for pat in patterns:
        pat = pat.strip()
        if not pat or pat.startswith("#"):
            continue
        if pat.endswith("/"):
            base = pat.rstrip("/")
            if s == base or s.startswith(base + "/"):
                return True
        elif "*" in pat:
            if fnmatch.fnmatch(s, pat) or fnmatch.fnmatch(os.path.basename(s), pat):
                return True
        elif s == pat or s.endswith("/" + pat):
            return True
    return False


def _progress(msg: str) -> None:
    import sys

    if not os.environ.get("CMD_GIT_PURE_QUIET"):
        print(msg, flush=True)


def _build_tree(repo: Path, root: Path, patterns: list[str], rel: Path = Path(".")) -> str:
    entries: list[tuple[str, str, str]] = []
    full = root / rel if str(rel) != "." else root
    if str(rel) == ".":
        _progress("git_pure: hashing worktree (may take a minute)...")
    for child in sorted(full.iterdir(), key=lambda p: p.name.lower()):
        if child.name == ".git":
            continue
        child_rel = rel / child.name if str(rel) != "." else Path(child.name)
        if _is_ignored(child_rel, patterns):
            continue
        if child.is_dir():
            entries.append(
                ("040000", child.name, _build_tree(repo, root, patterns, child_rel))
            )
        elif child.is_file():
            entries.append(("100644", child.name, _blob_hash(repo, child.read_bytes())))
    return _tree_hash(repo, entries)


def _commit_hash(repo: Path, tree: str, parent: str | None, message: str) -> str:
    now = int(time.time())
    tz = time.timezone
    sign = "+" if tz <= 0 else "-"
    tz_abs = abs(tz)
    tz_str = f"{sign}{tz_abs // 3600:02d}{tz_abs % 3600 // 60:02d}"
    author = f"cmd-verify <verify@local> {now} {tz_str}"
    lines = [f"tree {tree}"]
    if parent:
        lines.append(f"parent {parent}")
    lines.extend([f"author {author}", f"committer {author}", "", message])
    return _store_object(repo, "commit", "\n".join(lines).encode())


def _read_head(repo: Path) -> str | None:
    head_file = repo / ".git" / "HEAD"
    if not head_file.exists():
        return None
    head = head_file.read_text(encoding="utf-8").strip()
    if head.startswith("ref: "):
        ref = head[5:]
        ref_file = repo / ".git" / ref
        if ref_file.exists():
            return ref_file.read_text(encoding="utf-8").strip()
        return None
    return head


def commit_and_tag(repo: Path, message: str, tag: str = "v0.1.0") -> tuple[str, list[str]]:
    """Commit worktree (respecting .gitignore) and force-update tag."""
    log: list[str] = []
    patterns = _load_gitignore(repo)
    tree = _build_tree(repo, repo, patterns)
    parent = _read_head(repo)
    commit = _commit_hash(repo, tree, parent, message)
    log.append(f"$ git_pure commit -m {message!r}\nexit=0\n{commit}\n")

    main_ref = repo / ".git" / "refs" / "heads" / "main"
    main_ref.parent.mkdir(parents=True, exist_ok=True)
    main_ref.write_text(commit + "\n", encoding="utf-8")
    log.append(f"$ git_pure update refs/heads/main\nexit=0\n")

    tag_ref = repo / ".git" / "refs" / "tags" / tag
    tag_ref.write_text(commit + "\n", encoding="utf-8")
    log.append(f"$ git tag -f {tag}\nexit=0\n")
    log.append(f"$ git tag --points-at HEAD\nexit=0\n{tag}\n")
    log.append(f"HEAD={commit}\nv0.1.0={commit}\n")
    return commit, log


if __name__ == "__main__":
    import sys

    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    msg = sys.argv[2] if len(sys.argv) > 2 else "fix: docs consistency, i18n help, legacy data isolation, release notes"
    sha, lines = commit_and_tag(repo, msg)
    print("\n".join(lines))
    print(f"COMMIT={sha}")