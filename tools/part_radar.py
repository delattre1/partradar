#!/usr/bin/env python3
"""Validate research evidence and persist local engineering work orders.

OpenClaw does the research. This helper performs no searching or CAD work.
Input is JSON so OpenClaw can write it with its normal file tool; output is
YAML and JSON under the persistent Plow volume.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


STATUSES = {"FOUND", "ADAPTABLE", "NOT_FOUND"}
LICENSES = {"OPEN_SOURCE_CONFIRMED", "OPEN_SOURCE_UNCLEAR", "NO_LICENSE_FOUND", "RESTRICTED"}
OPEN_LICENSES = {
    "MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "GPL-2.0-only",
    "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later", "LGPL-2.1-only",
    "LGPL-3.0-only", "MPL-2.0", "CERN-OHL-P-2.0", "CERN-OHL-S-2.0",
    "CERN-OHL-W-2.0", "CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def string(value: Any, field: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{field} must be a nonempty string")
    return value.strip()


def url(value: Any, field: str) -> str:
    value = string(value, field)
    parsed = urlsplit(value)
    require(parsed.scheme == "https" and bool(parsed.netloc), f"{field} must be an HTTPS URL")
    return value


def text_list(value: Any, field: str) -> list[str]:
    require(isinstance(value, list), f"{field} must be a list")
    return [string(item, field) for item in value]


def license_classification(name: str | None, evidence_url: str | None) -> str:
    if not name:
        return "NO_LICENSE_FOUND"
    normalized = name.strip()
    if re.search(r"(?:^|[- ])(?:NC|ND)(?:[- .]|$)", normalized, re.I) or normalized.lower() in {
        "all rights reserved", "proprietary", "personal use only", "non-commercial"
    }:
        return "RESTRICTED"
    if normalized in OPEN_LICENSES and evidence_url:
        return "OPEN_SOURCE_CONFIRMED"
    return "OPEN_SOURCE_UNCLEAR"


def validate(data: Any) -> dict[str, Any]:
    require(isinstance(data, dict), "input must be an object")
    request_id = string(data.get("request_id"), "request_id")
    require(bool(re.fullmatch(r"REQ-[0-9]{4,8}", request_id)), "request_id must be REQ- followed by 4-8 digits")
    status = string(data.get("status"), "status")
    require(status in STATUSES, "status must be FOUND, ADAPTABLE, or NOT_FOUND")
    request = data.get("request")
    require(isinstance(request, dict), "request must be an object")
    request = {
        "object": string(request.get("object"), "request.object"),
        "requirements": request.get("requirements"),
    }
    require(isinstance(request["requirements"], dict) and bool(request["requirements"]),
            "request.requirements must be a nonempty object")
    for key, value in request["requirements"].items():
        string(key, "requirement key")
        string(value, f"request.requirements.{key}")

    search = data.get("search")
    require(isinstance(search, dict), "search must be an object")
    queries = text_list(search.get("queries"), "search.queries")
    require(bool(queries), "record at least one search query")
    sources = search.get("sources")
    require(isinstance(sources, list) and bool(sources), "record at least one searched source")
    for source in sources:
        url(source, "search.sources item")

    candidates = data.get("candidates")
    require(isinstance(candidates, list), "candidates must be a list")
    seen: set[str] = set()
    for candidate in candidates:
        require(isinstance(candidate, dict), "candidate must be an object")
        candidate_id = string(candidate.get("id"), "candidate.id")
        require(candidate_id not in seen, "candidate IDs must be unique")
        seen.add(candidate_id)
        string(candidate.get("name"), "candidate.name")
        string(candidate.get("description"), "candidate.description")
        source = candidate.get("source")
        require(isinstance(source, dict), "candidate.source must be an object")
        string(source.get("provider"), "candidate.source.provider")
        url(source.get("url"), "candidate.source.url")
        license_info = candidate.get("license")
        require(isinstance(license_info, dict), "candidate.license must be an object")
        name = license_info.get("name")
        evidence_url = license_info.get("url")
        if name is not None:
            name = string(name, "candidate.license.name")
        if evidence_url is not None:
            url(evidence_url, "candidate.license.url")
        classification = license_classification(name, evidence_url)
        declared = license_info.get("classification")
        require(declared in LICENSES, "candidate.license.classification is required")
        require(declared == classification, f"candidate {candidate_id} license classification should be {classification}")
        for key in ("print_files", "source_files", "documentation"):
            entries = candidate.get(key, [])
            require(isinstance(entries, list), f"candidate.{key} must be a list")
            for entry in entries:
                require(isinstance(entry, dict), f"candidate.{key} item must be an object")
                string(entry.get("name"), f"candidate.{key}.name")
                url(entry.get("url"), f"candidate.{key}.url")
        string(candidate.get("manufacturing"), "candidate.manufacturing")
        evidence = candidate.get("evidence", [])
        require(isinstance(evidence, list), "candidate.evidence must be a list")
        for item in evidence:
            require(isinstance(item, dict), "candidate.evidence item must be an object")
            string(item.get("claim"), "candidate.evidence.claim")
            url(item.get("url"), "candidate.evidence.url")

    selected_id = data.get("selected_candidate_id")
    if selected_id is not None:
        require(selected_id in seen, "selected_candidate_id must identify a candidate")
    evaluation = data.get("evaluation")
    require(isinstance(evaluation, dict), "evaluation must be an object")
    for key in ("matches", "mismatches", "unknowns"):
        text_list(evaluation.get(key), f"evaluation.{key}")
    string(evaluation.get("reason"), "evaluation.reason")
    if status in {"FOUND", "ADAPTABLE"}:
        require(selected_id is not None, f"{status} requires a selected candidate")
        chosen = next(c for c in candidates if c["id"] == selected_id)
        require(chosen["license"]["classification"] == "OPEN_SOURCE_CONFIRMED",
                f"{status} requires a confirmed open-source license")
        require(bool(chosen.get("print_files") or chosen.get("source_files")),
                f"{status} requires a linked design file")
    if status == "FOUND":
        require(not evaluation["mismatches"] and not evaluation["unknowns"],
                "FOUND cannot have mismatches or unknowns")
        require(not data.get("design_required"), "FOUND cannot request design work")
    if status == "ADAPTABLE":
        require(bool(evaluation["mismatches"]), "ADAPTABLE needs an evidenced mismatch")
    if status == "NOT_FOUND":
        require(selected_id is None, "NOT_FOUND cannot select a candidate")
    return data


def design_required(data: dict[str, Any]) -> dict[str, str] | None:
    if data["status"] == "FOUND":
        return None
    return {
        "event": "DesignRequired",
        "request_id": data["request_id"],
        "research_status": data["status"],
        "object": data["request"]["object"],
        "manufacturing": data["request"]["requirements"].get("manufacturing", "unspecified"),
        "reason": ("EXISTING_DESIGN_REQUIRES_MODIFICATION" if data["status"] == "ADAPTABLE"
                   else "NO_SUITABLE_OPEN_SOURCE_DESIGN"),
        "research_artifact": data["request_id"],
    }


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def to_yaml(value: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            return "{}\n"
        lines = []
        for key, item in value.items():
            require(bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", str(key))), "YAML keys must be simple identifiers")
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{pad}{key}:\n{to_yaml(item, indent + 2)}")
            else:
                lines.append(f"{pad}{key}: {to_yaml(item, indent + 2).strip()}\n")
        return "".join(lines)
    if isinstance(value, list):
        if not value:
            return "[]\n"
        lines = []
        for item in value:
            if isinstance(item, (dict, list)) and item:
                nested = to_yaml(item, indent + 2).splitlines()
                lines.append(f"{pad}- {nested[0].strip()}\n")
                lines.extend(line + "\n" for line in nested[1:])
            else:
                lines.append(f"{pad}- {to_yaml(item, indent + 2).strip()}\n")
        return "".join(lines)
    return yaml_scalar(value) + "\n"


def engineering_order(data: dict[str, Any]) -> dict[str, Any] | None:
    event = design_required(data)
    if event is None:
        return None
    selected = next((c for c in data["candidates"] if c["id"] == data.get("selected_candidate_id")), None)
    return {
        "type": "EngineeringWorkOrder",
        "request_id": data["request_id"],
        "status": "OPEN",
        "team": "engineering",
        "downstream_application": "ClawCAD",
        "research_status": data["status"],
        "requested_action": ("REVIEW_ADAPTATION" if selected else "EVALUATE_NEW_DESIGN"),
        "object": data["request"]["object"],
        "requirements": data["request"]["requirements"],
        "reason": data["evaluation"]["reason"],
        "closest_candidate": ({
            "name": selected["name"],
            "url": selected["source"]["url"],
            "license": selected["license"],
            "source_files": selected.get("source_files", []),
        } if selected else None),
        "unknowns": data["evaluation"]["unknowns"],
        "research_artifact": f"{data['request_id']}/research.yaml",
        "design_required_event": f"{data['request_id']}/design-required.json",
    }


def write_artifacts(data: dict[str, Any], root: Path) -> Path:
    validate(data)
    research_yaml = to_yaml(data)
    event = design_required(data)
    order = engineering_order(data) if event else None
    directory = root / data["request_id"]
    require(not directory.exists(), "request ID already exists; use a new ID to preserve evidence")
    directory.mkdir(parents=True)
    (directory / "research.yaml").write_text(research_yaml, encoding="utf-8")
    if event:
        (directory / "design-required.json").write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
        (directory / "engineering-order.json").write_text(json.dumps(order, indent=2) + "\n", encoding="utf-8")
    return directory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="research JSON prepared by OpenClaw")
    parser.add_argument("--out", type=Path, default=Path("/var/lib/plow/research"))
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    directory = write_artifacts(data, args.out)
    print(directory)


if __name__ == "__main__":
    main()
