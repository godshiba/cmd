# cmd — Production Audit Runbook

**Pattern:** sequential  
**Mode:** safe  
**Stop condition:** all tests pass, version tagged, no open P0/P1 bugs

## Pre-flight

```bash
cd ~/scripts/cmd
git status
python3 -m py_compile main.py lib/*.py
python3 -m unittest discover -s tests -v
./cmd --version
```

## Iteration checklist

1. **Static** — py_compile + unittest (no network, no fzf TTY)
2. **CLI** — `cmd --help`, `cmd ls`, `cmd lang en|ru|zh`, `cmd index`
3. **i18n** — browser lines in one language per locale (no EN/RU mix)
4. **Widget** — `source shell/cmd.widget.zsh`, `cmd-keys`, Ctrl+O in zsh
5. **Install** — `bash install.sh`, verify `cmd --version` from PATH

## Quality gates (safe mode)

| Gate | Command | Pass |
|------|---------|------|
| Compile | `python3 -m py_compile main.py lib/*.py` | exit 0 |
| Tests | `python3 -m unittest discover -s tests -v` | all OK |
| Version | `./cmd --version` | matches VERSION file |
| Locales | test `TestLocaleData` | 32 essential, 76 useful × 3 |

## Release

```bash
git add -A
git commit -m "Release v0.1.0: production audit fixes and test suite"
git tag v0.1.0
git push origin main --tags
gh release create v0.1.0 --title "v0.1.0" --notes-file CHANGELOG.md
```

## Fixed in this audit (v0.1.0)

- fzf ZLE: feed items via stdin pipe (removed /dev/tty stdin override)
- `cmd ls` / essential lookup without index
- Search includes example text (e.g. `cmd docker` → brew)
- `browse_related` fallback when fzf missing
- Locale cache invalidation on config/env change
- Smoke test suite: `tests/test_smoke.py`