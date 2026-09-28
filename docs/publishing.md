# Agent Index and hackathon release

PartRadar follows [Build on Plow](https://aiworthusing.com/agent-index/publish). The project is MIT licensed; the pinned upstream Plow image is inherited under its own license and remains maintained upstream. Complete the [install smoke test](install.md) before publishing. The MVP's engineering order stays local in OpenClaw state. Discord appears below only for the hackathon's human admin and verification process.

## Registration and metadata

The owner chooses the final slug (`AGENT_ID`) and publishes the repository at `https://github.com/edge-robot/partradar`. From this checkout, after `plow-agents login`:

```sh
plow-agents image set YOUR_AGENT_SLUG --name "PartRadar" --blurb "Search first. Design only when necessary." --repo https://github.com/edge-robot/partradar
plow-agents image set YOUR_AGENT_SLUG --link https://github.com/edge-robot/partradar/blob/main/docs/install.md
plow-agents image set YOUR_AGENT_SLUG --screenshot https://YOUR_PUBLIC_HOST/partradar-real-screenshot.png
plow-agents image set YOUR_AGENT_SLUG --video '{"provider":"youtube","id":"VIDEO_ID","title":"PartRadar demo"}'
plow-agents image show YOUR_AGENT_SLUG
```

Only issue the screenshot and video commands after real media exists at stable public URLs. `--link` is the installation/tutorial URL in the current CLI; `--screenshot` may be repeated to replace the list. The current `image set` flow claims or edits Index metadata. `AGENT_RUNTIME=OpenClaw` and the name/blurb are present in the image and local Compose environment for inherited first-boot registration. Use the same slug in the image, local `.env`, and Index listing. If the runtime registered the listing first, `image set` updates it for the owner.

## Public image and one-click admission

Use the [cloud build commands](install.md) to bake the owner slug into the variant image and push it. Record the immutable `ghcr.io/YOUR_ACCOUNT/partradar@sha256:...` reference printed by `plow-agents image push`. In GHCR settings, make the package public and verify anonymous pull. Then run:

```sh
plow-agents profile --show
plow-agents image show YOUR_AGENT_SLUG
```

The profile shows the owner UID. Post the UID, final slug, and immutable image reference in the AI Worth Using / Plow Discord so an admin can perform the initial admission. The current admin operation is `plow-agents image promote YOUR_AGENT_SLUG ghcr.io/YOUR_ACCOUNT/partradar@sha256:IMAGE_DIGEST --owner OWNER_UID`; the participant does not run that privileged action. An existing Index listing is required first. After admission, future releases use:

```sh
plow-agents image push ghcr.io/YOUR_ACCOUNT/partradar:v2 --promote YOUR_AGENT_SLUG
```

This promotes the exact pushed digest for new installations; existing running agents keep their image. Recheck the current CLI before a future release.

For hackathon verification, the human owner posts the public repository URL, release commit hash, and Agent Index ID in the [AI Worth Using verification thread](https://discord.com/channels/1519035948191449268/1549100840583700481). Confirm the verified badge and working one-click deployment afterward. The [publish guide](https://aiworthusing.com/agent-index/publish) requires MIT license, reporting usage, and verification for prizes; the product release also requires install instructions, real media, a public repository, and a public image.

## Release checklist

- [ ] PartRadar works through a live OpenClaw text conversation
- [x] MIT `LICENSE` exists
- [ ] Repository is public at its actual PartRadar URL
- [ ] Owner-selected `AGENT_ID` is configured in the release image
- [ ] Agent Index listing is registered with name, blurb, repository, and runtime
- [ ] OpenClaw usage and inherited five-minute reporting are verified live
- [ ] Public image is pushed and anonymously pullable
- [ ] Immutable image digest is recorded
- [x] README and install guide are available in the repository
- [ ] Demo video is linked
- [ ] At least one real image or screenshot is linked
- [ ] One-click deploy is requested and enabled by an admin
- [ ] Verification is requested with repository URL, commit, and Index ID
- [ ] Verified status is confirmed
