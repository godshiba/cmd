#!/usr/bin/env bash
# Full verification gate — artifacts in $ROOT/.verify-scratch/
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export CMD_SCRATCH="${CMD_SCRATCH:-$ROOT/.verify-scratch}"
export CMD_HOME="${CMD_HOME:-$CMD_SCRATCH/cmd-test-home}"
mkdir -p "$CMD_SCRATCH" "$CMD_HOME"
echo "== migrate_legacy =="
python3 -u scripts/migrate_legacy.py
echo "== capture_evidence =="
python3 -u scripts/capture_evidence.py
rc=$?
echo "EXIT=$rc"
cat "$CMD_SCRATCH/summary.txt"
echo "Artifacts: $CMD_SCRATCH"
git log -1 --oneline 2>/dev/null || true
git tag --points-at HEAD 2>/dev/null || true
exit $rc