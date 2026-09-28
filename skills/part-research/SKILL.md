---
name: part-research
description: Research an existing open-source 3D-printable design for a requested physical part before any new mechanical work.
---
# Part research

Extract the object, exact hardware identifiers, intended manufacturing method, dimensions or mounting needs, and any explicit constraints. Ask only for missing details that could change the search result. Preserve the user's wording when an identifier is ambiguous.

Search several relevant places using available OpenClaw web/browser tools or the connected owner's Mac through Latch. Useful places include GitHub, Printables, Thingiverse, MakerWorld, GrabCAD, manufacturer documentation, and general search. Follow source pages to actual files and license text. Never infer a file, license, or dimension from a search snippet alone. Do not build a scraper or promise an integration that is not available.

Record the search terms, pages actually visited, candidates considered, and evidence URLs. For each candidate, inspect where available: board/camera compatibility, dimensions, mounting, STL/3MF, editable CAD such as STEP/FCStd/SCAD, manufacturing method, documentation, and project activity. Mark unavailable facts as unknown.

Store research as JSON input for `/opt/plow/part-radar/part_radar.py`. The helper writes `research.yaml` into `/var/lib/plow/research/REQ-NNNN/`; see [artifact contract](/opt/plow/skills/part-research/references/artifact-contract.md). The helper validates and renders; it does not search. Use a fresh request ID and do not overwrite prior evidence.
