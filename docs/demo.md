# Demo: search before design

The planned video is a live OpenClaw conversation. Show the user texting PartRadar: “We need an FDM-printable enclosure for a Raspberry Pi Zero and RPIZ CAM 5MP 120.” Show PartRadar searching source pages, inspecting an actual license and design files, and explaining why the closest project needs engineering review. Show its `ADAPTABLE` reply, research YAML, `DesignRequired` JSON, and the locally persisted `engineering-order.json` with `status: OPEN`. The engineering team can inspect the order through the agent or its Plow state volume. Any later CAD change, simulation, human gate, and manufacturing footage belongs to ClawCAD, not to PartRadar.

The checked demo candidate is [Optocam Zero](https://github.com/dorukkumkumoglu/optocamzero/tree/d9772fbc432eae7b8a84007a5d435ba0c5c10b62). Its [BOM](https://github.com/dorukkumkumoglu/optocamzero/blob/d9772fbc432eae7b8a84007a5d435ba0c5c10b62/hardware/BOM.md) specifies Raspberry Pi Zero 2 W and Camera Module 3. Its [hardware folder](https://github.com/dorukkumkumoglu/optocamzero/tree/d9772fbc432eae7b8a84007a5d435ba0c5c10b62/hardware) includes STL, 3MF, and STEP files, and its [license](https://github.com/dorukkumkumoglu/optocamzero/blob/d9772fbc432eae7b8a84007a5d435ba0c5c10b62/LICENSE) explicitly allows adaptation under CC BY-SA 4.0. Those named hardware differences support `ADAPTABLE`. The exact RPIZ camera identity and physical dimensions were not verified, so the handoff asks ClawCAD to verify fit rather than claiming a measured incompatibility.

The [research input fixture](../examples/pi-zero-camera-research.json) can regenerate the [demo outputs](../examples/demo-output/REQ-0042/research.yaml) without network access. These files are evidence-backed examples of the artifact contract. They are not a captured OpenClaw run or proof of engineering-team acceptance.

## Release capture checklist

Capture a **real** conversation screenshot showing the user request, PartRadar's `ADAPTABLE` result, the candidate URL, license, editable source, and `DesignRequired`/engineering order. Frame it so a viewer understands the search-before-design result without reading the README. Save a redacted capture under `docs/assets/` and publish it at a stable HTTPS URL. The architecture diagram and the fixture above are supporting material, not substitutes for this screenshot.

Record a 60–90 second video from the working agent:

| Time | Show |
| --- | --- |
| 0–10s | The need: “We need a printable enclosure.” |
| 10–25s | PartRadar checks whether an existing design can be reused. |
| 25–45s | Actual source, license, and editable-file research. |
| 45–60s | The real `ADAPTABLE` result and camera mismatch. |
| 60–75s | `DesignRequired` and the local `OPEN` engineering order. |
| 75–90s | Show the local work order prepared for ClawCAD engineering review; close with “PartRadar searches. ClawCAD designs.” |

If the live result differs from the fixture, show the live result honestly. ClawCAD footage is optional and must be clearly identified as a separate application. Remove personal phone numbers, tokens, and private account details from the recording. Publish the video before registering its URL.

Once the real media is public, register it with the current Plow CLI:

```sh
plow-agents image set partradar --screenshot https://PUBLIC_URL/partradar-demo.png
plow-agents image set partradar --video '{"provider":"youtube","id":"VIDEO_ID","title":"PartRadar demo"}'
```

Replace the placeholders with the actual public image URL and YouTube ID. Do not run these commands with placeholders.
