"""Evaluator-visible release gates and candidate-tree audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPACE = ROOT / "space"
RELEASE = SPACE / "release"
HISTORICAL_PAGE_SHA256 = (
    "7612f7a7d8d7b9451b88dbf5504aac20e01a5b030a895b62e076e3c6c52f6def"
)
CONTROLLED_OLD_PATHS = {"README.md", "logbook.json"}
EXPECTED_VERDICTS = {
    1: "VERIFIED",
    2: "VERIFIED",
    3: "VERIFIED",
    4: "VERIFIED",
    5: "FALSIFIED",
    6: "VERIFIED",
}
MANDATORY_EVIDENCE = {
    "claim_contract.json",
    "source_audit.md",
    "method.md",
    "raw_results.json",
    "checker_output.json",
    "negative_control_output.json",
    "command.txt",
    "runtime.json",
    "EVAL.md",
    "limitations.md",
}
TEXT_SUFFIXES = {
    ".json",
    ".lock",
    ".md",
    ".py",
    ".sha256",
    ".toml",
    ".txt",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        digest, relative = line.split("  ", 1)
        entries[relative] = digest
    return entries


def _tree_files(node: dict[str, Any]) -> list[str]:
    files = [node["file"]]
    for child in node.get("children", []):
        files.extend(_tree_files(child))
    return files


def _local_markdown_links(path: Path) -> list[Path]:
    links: list[Path] = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        links.append((path.parent / target).resolve())
    return links


def intended_upload_paths() -> list[str]:
    paths = {"README.md", "logbook.json"}
    for root in (
        SPACE / "environment",
        SPACE / "evidence",
        SPACE / "pages" / "claims",
        SPACE / "release",
    ):
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                paths.add(path.relative_to(SPACE).as_posix())
    paths.add("pages/current/page.md")
    paths.discard("pages/overview/page.md")
    paths.add("release/upload_allowlist.txt")
    paths.add("release/upload_manifest.sha256")
    return sorted(paths)


def write_upload_metadata() -> dict[str, Any]:
    RELEASE.mkdir(parents=True, exist_ok=True)
    allowlist_path = RELEASE / "upload_allowlist.txt"
    manifest_path = RELEASE / "upload_manifest.sha256"
    paths = intended_upload_paths()
    allowlist_path.write_text("\n".join(paths) + "\n", encoding="utf-8")
    hashed = [
        path
        for path in paths
        if path not in {
            "release/upload_allowlist.txt",
            "release/upload_manifest.sha256",
        }
    ]
    hashed.append("release/upload_allowlist.txt")
    manifest_path.write_text(
        "\n".join(f"{sha256(SPACE / path)}  {path}" for path in sorted(hashed))
        + "\n",
        encoding="utf-8",
    )
    return {
        "allowlist_entries": len(paths),
        "manifest_entries": len(hashed),
        "manifest_excludes_itself_to_avoid_a_circular_hash": True,
    }


def audit_candidate(
    candidate: Path,
    protected_manifest: Path,
    *,
    write_result: bool = False,
) -> dict[str, Any]:
    protected = _manifest(protected_manifest)
    missing = sorted(path for path in protected if not (candidate / path).is_file())
    changed_uncontrolled = sorted(
        path
        for path, expected_hash in protected.items()
        if path not in CONTROLLED_OLD_PATHS
        and (candidate / path).is_file()
        and sha256(candidate / path) != expected_hash
    )
    result = {
        "judged_revision": "340d714e1848fb38fa63552937f6a1467560c61c",
        "protected_path_count": len(protected),
        "all_old_paths_present": not missing,
        "missing_old_paths": missing,
        "controlled_updated_paths": sorted(CONTROLLED_OLD_PATHS),
        "all_other_old_files_byte_identical": not changed_uncontrolled,
        "changed_uncontrolled_old_paths": changed_uncontrolled,
        "historical_page_sha256": sha256(
            candidate / "pages" / "overview" / "page.md"
        ),
        "historical_page_byte_identical": sha256(
            candidate / "pages" / "overview" / "page.md"
        )
        == HISTORICAL_PAGE_SHA256,
    }
    result["status"] = (
        "PASS"
        if result["all_old_paths_present"]
        and result["all_other_old_files_byte_identical"]
        and result["historical_page_byte_identical"]
        else "FAIL"
    )
    if write_result:
        (RELEASE / "subset_check.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if result["status"] != "PASS":
        raise AssertionError(f"protected candidate audit failed: {result}")
    return result


def validate_release_surface() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    logbook = json.loads((SPACE / "logbook.json").read_text(encoding="utf-8"))
    checks["correct_space_id"] = logbook["space_id"] == "DineshAI/r3PKGNlKET"
    checks["canonical_root_is_current"] = (
        logbook["root"]["file"] == "pages/current/page.md"
    )
    tree_files = _tree_files(logbook["root"])
    checks["all_logbook_pages_exist"] = all(
        (SPACE / path).is_file() for path in tree_files
    )
    checks["historical_label_exact"] = any(
        child["title"] == "Historical rejected baseline"
        and child["file"] == "pages/overview/page.md"
        for child in logbook["root"]["children"]
    )
    checks["historical_page_byte_identical"] = (
        sha256(SPACE / "pages" / "overview" / "page.md")
        == HISTORICAL_PAGE_SHA256
    )

    matrix = json.loads(
        (RELEASE / "visibility_matrix.json").read_text(encoding="utf-8")
    )
    checks["matrix_has_six_claims"] = len(matrix["rows"]) == 6
    checks["matrix_has_no_missing_cells"] = all(
        row["reviewer_verdict"] == EXPECTED_VERDICTS[row["claim"]]
        and all(
            row[field]
            for field in (
                "code_visible",
                "data_inline",
                "raw_link",
                "checker",
                "control",
                "exact_claim_tested",
            )
        )
        for row in matrix["rows"]
    )

    all_evidence = True
    all_outputs = True
    all_commands = True
    all_runtime = True
    all_page_links = True
    for claim, verdict in EXPECTED_VERDICTS.items():
        evidence = SPACE / "evidence" / f"claim_{claim}"
        all_evidence &= MANDATORY_EVIDENCE.issubset(
            {path.name for path in evidence.iterdir() if path.is_file()}
        )
        checker = json.loads(
            (evidence / "checker_output.json").read_text(encoding="utf-8")
        )
        control = json.loads(
            (evidence / "negative_control_output.json").read_text(
                encoding="utf-8"
            )
        )
        raw = json.loads(
            (evidence / "raw_results.json").read_text(encoding="utf-8")
        )
        raw_verdict = raw.get("verdict", raw.get("status"))
        control_status = control.get("status", control.get("observed_status"))
        all_outputs &= (
            checker["status"] == "PASS"
            and control_status == "FAIL"
            and raw_verdict == verdict
        )
        all_commands &= (
            evidence.joinpath("command.txt").read_text(encoding="utf-8").strip()
            == "uv run --frozen python -m reproduction.runner"
        )
        runtime = json.loads(
            (evidence / "runtime.json").read_text(encoding="utf-8")
        )
        all_runtime &= (
            "selected_backend" in runtime
            and (
                "actual_run" in runtime
                or claim in {1, 2, 4}
                and "actual_run" in runtime
            )
        )
        page = SPACE / "pages" / "claims" / f"claim-{claim}" / "page.md"
        links = _local_markdown_links(page)
        all_page_links &= bool(links) and all(link.is_file() for link in links)
        page_text = page.read_text(encoding="utf-8")
        all_page_links &= verdict in page_text

    checks["all_mandatory_evidence_present"] = all_evidence
    checks["checkers_pass_and_controls_fail"] = all_outputs
    checks["fixed_command_identical"] = all_commands
    checks["runtime_and_allocation_recorded"] = all_runtime
    checks["all_claim_page_links_resolve"] = all_page_links

    notebook = ROOT / "notebooks" / "reproduction.py"
    report = ROOT / "reports" / "reproduction" / "report.md"
    checks["public_report_and_notebook_exist"] = notebook.is_file() and report.is_file()
    images = sorted((report.parent / "images").glob("*.svg"))
    checks["four_evidence_figures_exist"] = len(images) == 4 and all(
        "<svg" in image.read_text(encoding="utf-8") for image in images
    )

    allowlist = [
        line
        for line in (RELEASE / "upload_allowlist.txt")
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    ]
    checks["allowlist_sorted_unique_exact"] = (
        allowlist == sorted(set(allowlist))
        and allowlist == intended_upload_paths()
    )
    checks["allowlist_text_only"] = all(
        (SPACE / path).is_file() and (SPACE / path).suffix in TEXT_SUFFIXES
        for path in allowlist
    )
    upload_manifest = _manifest(RELEASE / "upload_manifest.sha256")
    checks["upload_hashes_exact"] = all(
        (SPACE / path).is_file() and sha256(SPACE / path) == digest
        for path, digest in upload_manifest.items()
    )
    checks["manifest_has_all_noncircular_uploads"] = set(upload_manifest) == (
        set(allowlist) - {"release/upload_manifest.sha256"}
    )

    subset = json.loads(
        (RELEASE / "subset_check.json").read_text(encoding="utf-8")
    )
    checks["protected_tree_subset_passes"] = subset["status"] == "PASS"
    red_team = (RELEASE / "red_team.md").read_text(encoding="utf-8")
    checks["blind_red_team_repeated_after_fixes"] = (
        "Review A" in red_team
        and "Review B" in red_team
        and "No conclusion remained unverifiable" in red_team
    )

    secret_patterns = (
        re.compile(r"hf_[A-Za-z0-9]{20,}"),
        re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"),
        re.compile(r"(?i)(?:api[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
    )
    secret_hits: list[str] = []
    for relative in allowlist:
        text = (SPACE / relative).read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in secret_patterns):
            secret_hits.append(relative)
    checks["no_secret_patterns"] = not secret_hits

    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "status": "PASS" if not failed else "FAIL",
        "checks": checks,
        "failed": failed,
        "secret_hit_paths": secret_hits,
        "allowlist_entries": len(allowlist),
        "upload_manifest_entries": len(upload_manifest),
    }
    if failed:
        raise AssertionError(f"release surface gates failed: {failed}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--protected-manifest", type=Path)
    parser.add_argument("--write-subset-result", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        print(json.dumps(write_upload_metadata(), indent=2, sort_keys=True))
        return 0
    if args.candidate:
        if not args.protected_manifest:
            parser.error("--candidate requires --protected-manifest")
        print(
            json.dumps(
                audit_candidate(
                    args.candidate,
                    args.protected_manifest,
                    write_result=args.write_subset_result,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    print(json.dumps(validate_release_surface(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
