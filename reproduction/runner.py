"""Fixed OpenResearch entrypoint.

The baseline deliberately audits the historical judged artifact. Descendant
experiments extend ``CHECKS`` in committed code while keeping this command
unchanged.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / ".openresearch" / "artifacts" / "baseline"
EXPECTED_SPACE_SHA = "340d714e1848fb38fa63552937f6a1467560c61c"
EXPECTED_PAPER_SHA256 = (
    "a6f601022be169cb0651f4d4e389e233cae827109c611f79adfb7dd67fddcc0b"
)
EXPECTED_MANIFEST_ENTRIES = 13


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _cpu_allocation() -> dict[str, Any]:
    logical = os.cpu_count()
    quota_cores = None
    cpu_max = Path("/sys/fs/cgroup/cpu.max")
    if cpu_max.exists():
        quota, period = cpu_max.read_text(encoding="utf-8").strip().split()
        if quota != "max":
            quota_cores = float(quota) / float(period)
    return {
        "logical_cpu_count": logical,
        "cgroup_quota_cores": quota_cores,
        "platform": platform.platform(),
    }


def audit_historical_baseline() -> dict[str, Any]:
    manifest = ARTIFACT / "judged_space_manifest.sha256"
    verdict = ARTIFACT / "live_verdict_filtered.json"
    source = ARTIFACT / "paper_source.json"
    visibility = ARTIFACT / "historical_visibility.json"

    manifest_lines = [
        line for line in manifest.read_text(encoding="utf-8").splitlines() if line
    ]
    verdict_data = json.loads(verdict.read_text(encoding="utf-8"))
    source_data = json.loads(source.read_text(encoding="utf-8"))
    visibility_data = json.loads(visibility.read_text(encoding="utf-8"))

    checks = {
        "manifest_has_13_entries": len(manifest_lines) == EXPECTED_MANIFEST_ENTRIES,
        "verdict_selected_by_space_id": (
            verdict_data["space_id"] == "DineshAI/r3PKGNlKET"
        ),
        "judged_revision_exact": verdict_data["sha"] == EXPECTED_SPACE_SHA,
        "paper_source_hash_exact": (
            source_data["sha256"] == EXPECTED_PAPER_SHA256
        ),
        "all_six_claims_inconclusive": all(
            item["verdict"] == "inconclusive" for item in verdict_data["claims"]
        )
        and len(verdict_data["claims"]) == 6,
        "historical_visibility_gate_fails": all(
            not row["release_ready"] for row in visibility_data["rows"]
        ),
        "missing_referenced_outputs_recorded": sorted(
            visibility_data["missing_referenced_paths"]
        )
        == ["outputs/gate.json", "outputs/verdict.json"],
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"historical audit failed: {failed}")

    return {
        "check": "historical_judged_baseline",
        "status": "PASS",
        "scientific_claim_status": "BLOCKED",
        "checks": checks,
        "space_sha": EXPECTED_SPACE_SHA,
        "paper_sha256": EXPECTED_PAPER_SHA256,
        "manifest_sha256": _sha256(manifest),
        "limitations": [
            "This baseline verifies only the evaluator-visible evidence gap.",
            "It provides no support for any of the paper's six scientific claims.",
        ],
    }


def main() -> int:
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    try:
        result = audit_historical_baseline()
        exit_code = 0
    except Exception as exc:  # pragma: no cover - exercised by negative controls later
        result = {
            "check": "historical_judged_baseline",
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        }
        exit_code = 1

    result["compute"] = {
        "pre_run_estimate_cores": 1,
        "pre_run_estimate_runtime_seconds": 30,
        "selected_backend": "local",
        "selected_flavor": None,
        "actual_allocation": _cpu_allocation(),
        "wall_seconds": time.perf_counter() - started_wall,
        "cpu_seconds": time.process_time() - started_cpu,
        "python": sys.version.split()[0],
    }
    print("=== EVAL.md ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
