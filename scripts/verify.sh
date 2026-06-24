#!/usr/bin/env bash
# Release verification gate: runs tests, captures artifacts, commits dirty tree, retags v0.1.0.
# Read-only local check: CMD_VERIFY_NO_GIT=1 bash scripts/verify.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export CMD_HOME="${CMD_HOME:-$(mktemp -d -t cmd-verify-XXXXXX)}"
export CMD_LANG="${CMD_LANG:-en}"
export CMD_SCRATCH="${CMD_SCRATCH:-$ROOT/.verify-scratch}"
mkdir -p "$CMD_SCRATCH"

echo "== migrate_legacy =="
python3 -u scripts/migrate_legacy.py
echo "== capture_evidence =="
python3 -u scripts/capture_evidence.py
rc=$?
echo "EXIT=$rc"
cat "$CMD_SCRATCH/summary.txt"
echo "verify.sh: evidence in $CMD_SCRATCH"
exit $rc