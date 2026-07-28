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
import subprocess
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


def verify_claim_3() -> dict[str, Any]:
    from reproduction.claims.privacy_factor import certificate

    primary = certificate()
    raw = json.loads(
        (
            ROOT
            / ".openresearch"
            / "artifacts"
            / "claim_3"
            / "raw_results.json"
        ).read_text(encoding="utf-8")
    )
    fixture = primary["fixture"]
    for key, expected in raw["fixture"].items():
        if fixture[key] != expected:
            raise AssertionError(
                f"Claim 3 raw fixture mismatch for {key}: "
                f"{fixture[key]!r} != {expected!r}"
            )

    checker_process = subprocess.run(
        [
            sys.executable,
            "-m",
            "reproduction.claims.privacy_factor_checker",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    print("=== CLAIM 3 INDEPENDENT CHECKER ===")
    print(checker_process.stdout.rstrip())
    if checker_process.returncode != 0:
        raise AssertionError(
            f"Claim 3 independent checker exited {checker_process.returncode}"
        )
    checker = json.loads(checker_process.stdout)
    if checker["status"] != "PASS":
        raise AssertionError("Claim 3 independent checker did not PASS")

    negative_process = subprocess.run(
        [
            sys.executable,
            "-m",
            "reproduction.claims.privacy_factor",
            "--negative-control",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    print("=== CLAIM 3 NEGATIVE CONTROL ===")
    print(negative_process.stdout.rstrip())
    if negative_process.returncode == 0:
        raise AssertionError("Claim 3 negative control unexpectedly passed")
    negative = json.loads(negative_process.stdout)
    if negative["status"] != "FAIL":
        raise AssertionError("Claim 3 negative control did not report FAIL")

    print("=== CLAIM 3 PRIMARY CERTIFICATE ===")
    print(json.dumps(primary, indent=2, sort_keys=True))
    return {
        "claim": 3,
        "status": "VERIFIED",
        "primary_checks": primary["checks"],
        "independent_checker": checker,
        "negative_control": {
            "exit_code": negative_process.returncode,
            "status": negative["status"],
            "error": negative["error"],
        },
    }


def _run_claim_with_control(
    *,
    claim_label: str,
    primary_module: str,
    checker_module: str,
    certificate: Any,
) -> dict[str, Any]:
    primary = certificate()
    checker_process = subprocess.run(
        [sys.executable, "-m", checker_module],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    print(f"=== {claim_label} INDEPENDENT CHECKER ===")
    print(checker_process.stdout.rstrip())
    if checker_process.returncode != 0:
        raise AssertionError(
            f"{claim_label} independent checker exited "
            f"{checker_process.returncode}"
        )
    checker = json.loads(checker_process.stdout)
    if checker["status"] != "PASS":
        raise AssertionError(f"{claim_label} independent checker did not PASS")

    negative_process = subprocess.run(
        [sys.executable, "-m", primary_module, "--negative-control"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    print(f"=== {claim_label} NEGATIVE CONTROL ===")
    print(negative_process.stdout.rstrip())
    if negative_process.returncode == 0:
        raise AssertionError(f"{claim_label} negative control unexpectedly passed")
    negative = json.loads(negative_process.stdout)
    if negative["status"] != "FAIL":
        raise AssertionError(f"{claim_label} negative control did not report FAIL")

    print(f"=== {claim_label} PRIMARY CERTIFICATE ===")
    print(json.dumps(primary, indent=2, sort_keys=True))
    return {
        "claim": primary.get("claim", primary.get("claims")),
        "status": "VERIFIED",
        "primary_checks": primary["checks"],
        "independent_checker": checker,
        "negative_control": {
            "exit_code": negative_process.returncode,
            "status": negative["status"],
            "error": negative["error"],
        },
    }


def verify_claim_1() -> dict[str, Any]:
    from reproduction.claims.log_loss_reduction import certificate

    return _run_claim_with_control(
        claim_label="CLAIM 1",
        primary_module="reproduction.claims.log_loss_reduction",
        checker_module="reproduction.claims.log_loss_reduction_checker",
        certificate=certificate,
    )


def verify_claims_2_and_4() -> dict[str, Any]:
    from reproduction.claims.corruption_order import certificate

    return _run_claim_with_control(
        claim_label="CLAIMS 2 AND 4",
        primary_module="reproduction.claims.corruption_order",
        checker_module="reproduction.claims.corruption_order_checker",
        certificate=certificate,
    )


def verify_claims_5_and_6() -> dict[str, Any]:
    from reproduction.claims.alignment_algorithms import certificate

    primary = certificate()
    raw_5 = json.loads(
        (
            ROOT
            / ".openresearch"
            / "artifacts"
            / "claim_5"
            / "raw_results.json"
        ).read_text(encoding="utf-8")
    )
    raw_6 = json.loads(
        (
            ROOT
            / ".openresearch"
            / "artifacts"
            / "claim_6"
            / "raw_results.json"
        ).read_text(encoding="utf-8")
    )
    fixture = primary["finite_policy_fixture"]
    if raw_5["finite_fixture"]["expected_PrivXPO_selection"] != fixture[
        "PrivXPO_selected"
    ]:
        raise AssertionError("Claim 5 raw PrivXPO selection mismatch")
    if raw_6["finite_fixture"]["PrivChiPO_scores"] != fixture["PrivChiPO_scores"]:
        raise AssertionError("Claim 6 raw PrivChiPO scores mismatch")
    if raw_6["finite_fixture"]["SquareChiPO_losses"] != fixture[
        "SquareChiPO_losses"
    ]:
        raise AssertionError("Claim 6 raw SquareChiPO losses mismatch")

    result = _run_claim_with_control(
        claim_label="CLAIMS 5 AND 6",
        primary_module="reproduction.claims.alignment_algorithms",
        checker_module="reproduction.claims.alignment_algorithms_checker",
        certificate=lambda: primary,
    )
    result["status"] = {"claim_5": "FALSIFIED", "claim_6": "VERIFIED"}
    return result


def _git_sha() -> str:
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return process.stdout.strip()


def main() -> int:
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    try:
        result = {
            "historical_regression": audit_historical_baseline(),
            "claims": [
                verify_claim_1(),
                verify_claims_2_and_4(),
                verify_claim_3(),
                verify_claims_5_and_6(),
            ],
        }
        from reproduction.release import validate_release_surface

        result["release_surface"] = validate_release_surface()
        result["status"] = "PASS"
        exit_code = 0
    except Exception as exc:  # pragma: no cover - exercised by negative controls later
        result = {
            "status": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        }
        exit_code = 1

    runtime_profile = json.loads(
        (
            ROOT
            / ".openresearch"
            / "artifacts"
            / "release"
            / "runtime.json"
        ).read_text(encoding="utf-8")
    )
    result["provenance"] = {
        "git_sha": _git_sha(),
        "fixed_command": "uv run --frozen python -m reproduction.runner",
        "seeds": [],
    }
    result["compute"] = {
        "pre_run_estimate_cores": 1,
        "pre_run_estimate_runtime_seconds": 30,
        "selected_backend": runtime_profile["selected_backend"],
        "selected_flavor": runtime_profile["selected_flavor"],
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
