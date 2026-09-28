# Research input contract

Write one JSON object with these fields, then call `part_radar.py`:

```json
{
  "request_id": "REQ-0042",
  "status": "ADAPTABLE",
  "request": {"object": "camera-enclosure", "requirements": {"board": "Raspberry Pi Zero", "camera": "RPIZ CAM 5MP 120", "manufacturing": "FDM"}},
  "search": {"queries": ["Pi Zero camera enclosure OpenSCAD license"], "sources": ["https://github.com/example/case"]},
  "candidates": [{
    "id": "candidate-1", "name": "Case", "description": "Pi Zero case with a different camera",
    "source": {"provider": "github", "url": "https://github.com/example/case"},
    "license": {"name": "MIT", "url": "https://github.com/example/case/blob/main/LICENSE", "classification": "OPEN_SOURCE_CONFIRMED"},
    "print_files": [{"name": "case.stl", "url": "https://github.com/example/case/blob/main/case.stl"}],
    "source_files": [{"name": "case.scad", "url": "https://github.com/example/case/blob/main/case.scad"}],
    "documentation": [{"name": "README", "url": "https://github.com/example/case/blob/main/README.md"}],
    "manufacturing": "FDM",
    "evidence": [{"claim": "Source explicitly names a different camera", "url": "https://github.com/example/case/blob/main/README.md"}]
  }],
  "selected_candidate_id": "candidate-1",
  "evaluation": {"matches": ["Pi Zero board"], "mismatches": ["Source names a different camera"], "unknowns": ["Exact requested camera dimensions"], "reason": "Existing source requires camera compatibility review and likely modification"}
}
```

Replace every example URL and claim with a source actually checked. `selected_candidate_id` is `null` for `NOT_FOUND`; `candidates` may still contain rejected candidates. `FOUND` needs no mismatches or unknowns. The helper computes the `DesignRequired` event and local engineering work order for the two design states. It does not send the order externally.

The `license.classification` must agree with the helper's conservative license mapping. Familiar SPDX names without a license URL remain `OPEN_SOURCE_UNCLEAR`; absent license is `NO_LICENSE_FOUND`. Noncommercial and no-derivatives terms are `RESTRICTED`. Ask for manual review if the license is unfamiliar.
