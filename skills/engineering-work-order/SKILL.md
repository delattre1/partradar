---
name: engineering-work-order
description: Persist a local engineering work order and DesignRequired event for ADAPTABLE or NOT_FOUND PartRadar results.
---
# Engineering work order

After evaluation, write the research input JSON to `/var/lib/plow/research-input-REQ-NNNN.json`. Run:

```sh
python3 /opt/plow/part-radar/part_radar.py /var/lib/plow/research-input-REQ-NNNN.json
```

The helper creates `research.yaml` in `/var/lib/plow/research/REQ-NNNN/`. For `ADAPTABLE` or `NOT_FOUND`, it also creates `design-required.json` and `engineering-order.json` there. The work order has `status: OPEN`, names the engineering team, references the research evidence, and records the requested review. `FOUND` creates only `research.yaml`.

Read the generated order and tell the user its request ID and persistent path. The local order is ready for the engineering team to review through the agent or the shared Plow state volume. This MVP does not send it externally or claim that the team has seen it. If validation fails, correct the evidence rather than bypassing the helper. Never design the modification or invoke ClawCAD source code.
