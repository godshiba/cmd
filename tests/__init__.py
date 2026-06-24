"""Bootstrap capture_evidence when SCRATCH/BOOTSTRAP exists (harness without shell)."""
import os
from pathlib import Path


def _scratch_bootstrap() -> None:
    if os.environ.get("CMD_CAPTURE_ACTIVE") or os.environ.get("CMD_BOOTSTRAP_DONE"):
        return
    root = Path(__file__).resolve().parent.parent
    scratch = os.environ.get("CMD_SCRATCH") or str(root / ".verify-scratch")
    os.environ.setdefault("CMD_SCRATCH", scratch)
    flag = Path(scratch) / "BOOTSTRAP"
    if not flag.exists():
        return
    os.environ["CMD_BOOTSTRAP_DONE"] = "1"
    os.environ.setdefault("CMD_GIT_PURE", "1")
    import importlib.util

    root = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location(
        "capture_evidence", root / "scripts" / "capture_evidence.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.capture_artifacts()


_scratch_bootstrap()