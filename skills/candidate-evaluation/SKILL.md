---
name: candidate-evaluation
description: Classify PartRadar research as FOUND, ADAPTABLE, or NOT_FOUND using explicit fit and license evidence.
---
# Candidate evaluation

Classify every candidate license as `OPEN_SOURCE_CONFIRMED`, `OPEN_SOURCE_UNCLEAR`, `NO_LICENSE_FOUND`, or `RESTRICTED`. A confirmed license needs its actual license page and a recognizable open license. Commercial, no-derivatives, personal-use, or absent terms cannot support a reuse recommendation. Report the original license name and URL. This is research, not legal advice.

Choose exactly one primary state after a reasonable search:

- `FOUND`: an openly licensed design has a linked printable or editable file; evidence supports all material fit requirements without modification. No material fit unknown remains.
- `ADAPTABLE`: an openly licensed design has a linked file and a documented mismatch that needs mechanical modification. Describe the mismatch; never design the change.
- `NOT_FOUND`: no sufficiently suitable confirmed openly licensed design survived evaluation. Include search scope and explain whether promising results lacked fit evidence, source files, or usable license terms.

Do not turn an unverified camera dimension into a claimed mismatch. If an exact fit remains uncertain, report uncertainty and request the missing drawing or product link before declaring `FOUND`. A distinct camera model in a source design can justify `ADAPTABLE` when the sources actually identify both models; note that physical fit still requires ClawCAD verification.

Use concise evidence-linked reasoning, not a numeric confidence score. `FOUND` has no work order. The other states use `engineering-work-order`.
