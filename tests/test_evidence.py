"""Static invariants + discover-time capture gate (skipped during capture_evidence inner unittest)."""
import importlib.util
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestVerificationEvidence(unittest.TestCase):
    def test_capture_evidence_inner_suite_excludes_gate(self):
        """Inner unittest must not load test_capture_gate (no capture recursion)."""
        src = (ROOT / "scripts" / "capture_evidence.py").read_text(encoding="utf-8")
        self.assertIn("INNER_EVIDENCE_TESTS", src)
        self.assertIn("_ENV_CLI", src)
        self.assertIn("_ENV_TEST", src)
        self.assertIn("test_legacy_data_not_at_data_root", src)
        inner_block = src.split("INNER_EVIDENCE_TESTS", 1)[1].split(")", 1)[0]
        self.assertNotIn("produces_scratch_artifacts", inner_block)
        self.assertNotIn('loadTestsFromName("tests.test_evidence")', src)
        self.assertNotIn("unittest.discover", src)
        self.assertNotIn("discover -s tests", src)
        self.assertIn("CMD_CAPTURE_ACTIVE", src)
        self.assertIn("git add -A", src)
        self.assertIn("post-commit", src)
        self.assertIn("was_dirty", src)
        self.assertIn("git_pure", src)
        gate_src = (ROOT / "tests" / "test_evidence.py").read_text(encoding="utf-8")
        self.assertIn("CMD_CAPTURE_ACTIVE", gate_src)
        self.assertIn("test_capture_gate_produces_scratch_artifacts", gate_src)

    def test_legacy_data_not_at_data_root(self):
        for name in ("essential.json", "categories.json", "useful_system.json"):
            self.assertFalse((ROOT / "data" / name).exists(), name)
        for name in ("categories.json", "useful_system.json"):
            self.assertTrue((ROOT / "data" / "legacy" / name).exists(), name)
        self.assertTrue((ROOT / "data" / "locales" / "ru" / "essential.json").exists())

    def test_capture_gate_produces_scratch_artifacts(self):
        if os.environ.get("CMD_CAPTURE_ACTIVE"):
            self.skipTest("skipped during capture_evidence inner unittest")
        scratch = os.environ.get("CMD_SCRATCH")
        if not scratch:
            self.skipTest("set CMD_SCRATCH to run verification gate")

        spec = importlib.util.spec_from_file_location(
            "capture_evidence", ROOT / "scripts" / "capture_evidence.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        rc = mod.capture_artifacts()
        scratch_path = Path(scratch)
        self.assertEqual(rc, 0, (scratch_path / "summary.txt").read_text(encoding="utf-8"))
        for name in mod.REQUIRED_ARTIFACTS:
            self.assertTrue((scratch_path / name).exists(), name)


if __name__ == "__main__":
    unittest.main()