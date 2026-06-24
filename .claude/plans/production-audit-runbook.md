# cmd — Production Audit Runbook

**Pattern:** sequential  
**Mode:** safe  
**Stop condition:** all tests pass, version tagged, no open P0/P1 bugs

## Pre-flight

```bash
cd ~/scripts/cmd
git status
export CMD_SCRATCH=/tmp/cmd-scratch-$$
bash scripts/verify.sh
cat "$CMD_SCRATCH/summary.txt"   # expect: PASS: all verification steps OK
```

## Iteration checklist

1. **Static** — `scripts/verify.sh` (py_compile + in-process smoke/evidence tests; no fzf TTY)
2. **CLI** — `cmd --help`, `cmd ls`, `cmd lang en|ru|zh`, `cmd index`
3. **i18n** — browser lines in one language per locale (no EN/RU mix)
4. **Widget** — `source shell/cmd.widget.zsh`, `cmd-keys`, Ctrl+O in zsh
5. **Install** — `bash install.sh`, verify `cmd --version` from PATH

## Quality gates (safe mode)

| Gate | Command | Pass |
|------|---------|------|
| Verify | `bash scripts/verify.sh` | exit 0; `summary.txt` = PASS |
| Artifacts | `ls "$CMD_SCRATCH"` | compile.log, tests.log, tag.log, … |
| Version | `cat "$CMD_SCRATCH"/version-0.txt` | `cmd 0.1.0` |
| Locales | `tests.log` → `TestLocaleData` | 32 essential, 76 useful × 3 |

## Release

```bash
git add -A
git commit -m "fix: docs consistency, i18n help, legacy data isolation, release notes"
git tag -f v0.1.0
git push origin main --tags
gh release create v0.1.0 --title "v0.1.0" --notes-file .github/release-notes/v0.1.0.md
```

## Fixed in this audit (v0.1.0)

- fzf ZLE: feed items via stdin pipe (removed /dev/tty stdin override)
- `cmd ls` / essential lookup without index
- Search includes example text (e.g. `cmd docker` → brew)
- `browse_related` fallback when fzf missing
- Locale cache invalidation on config/env change
- Smoke test suite: `tests/test_smoke.py`
- Doc consistency: `cmd <query>` help, CHANGELOG 0.0.1, `data/LEGACY.md`
- i18n `help.usage_lines` (en/ru/zh); `data/legacy/` isolation; `scripts/capture_evidence.py`
- Release notes `v0.1.0.md`; evidence gate `tests/test_evidence.py`
- zsh index builder: correct `commands` / `builtins` array listing