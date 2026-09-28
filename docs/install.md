# Install and local smoke test

This is the install/tutorial page intended for the future Agent Index listing. Local requirements: Podman with `podman compose`/`podman-compose`, Python 3.11+, Git, a phone able to text a Plow line, and the current [`plow-agents` CLI](https://github.com/plow-pbc/plow-agents). The owner needs a Plow account. For web research, connect a supported browser/search capability to OpenClaw, such as the owner's Mac through Latch. The engineering work order needs no external messaging configuration.

## Local Build on Plow flow

Install the CLI as its README documents, then work from the PartRadar repository root:

```sh
plow-agents login
plow-agents lines
cp .env.example .env
# Edit .env: replace YOUR_AGENT_SLUG with the owner-selected Agent Index slug.
plow-agents deploy --local --line ln_xxx
podman compose up --build -d
podman compose ps
podman compose logs -f agent
```

`login` asks the owner to text an activation code. Choose a free `ln_xxx` from `lines`. The current CLI's `deploy --local` command mints `./plow-credentials`, binds the agent to the line, and then tries `docker compose up --build -d`. On a Podman-only machine, that last step fails with `docker` not found; the credential and line-bound agent already exist. Run `podman compose up --build -d` next. If `plow-credentials` already exists for this line, skip the provisioning command and start Compose directly; do not mint a second agent. `.env` passes `AGENT_ID` to the running container and build. `plow-credentials` contains a live scoped token and is ignored by Git and the build context. Never paste it into a ticket, commit, or image.

The local dashboard is `http://localhost:3001`. Compose publishes only `127.0.0.1:3001` and starts a `dev-dashboard` Caddy proxy sharing the agent's network namespace. This follows the current Plow OpenClaw development setup and keeps OpenClaw port 3000 private. The local Podman network on this development machine could not resolve `api.plow.co` through its embedded DNS server; the agent service uses `1.1.1.1` and `8.8.8.8` for local external DNS. If your Plow API uses a private hostname, replace those with reachable resolvers appropriate for your network.

Normal stop/restart commands keep the named state volume:

```sh
podman compose ps
podman compose logs -f agent
podman compose restart
podman compose down
```

Do not use `podman compose down -v` during normal testing: the volume holds OpenClaw sessions, PartRadar research, and Agent Index installation identity.

Check runtime state without exposing credentials:

```sh
podman compose ps
podman compose logs --tail=200 agent
podman compose exec agent printenv AGENT_ID
podman compose exec agent sh -lc 'test -n "$PLOW_AGENT_TOKEN" && echo PLOW_AGENT_TOKEN=set || echo PLOW_AGENT_TOKEN=missing'
podman compose exec agent sh -lc 'test -n "$PLOW_API_BASE" && echo PLOW_API_BASE=set || echo PLOW_API_BASE=missing'
podman compose exec agent test -f /opt/plow/prompt/AGENTS.md
podman compose exec agent test -f /opt/plow/skills/part-research/SKILL.md
podman compose exec agent test -f /opt/plow/agent-index-client.py
podman compose exec agent sh -lc 'find /var/lib/plow/agents -name openclaw-agent.sqlite -print'
podman compose exec agent sh -lc 'HOME=/var/lib/plow OPENCLAW_STATE_DIR=/var/lib/plow python3 /opt/plow/agent-index-client.py status'
podman compose exec agent sh -lc 'HOME=/var/lib/plow OPENCLAW_STATE_DIR=/var/lib/plow python3 /opt/plow/agent-index-client.py --dry-run'
```

The upstream boot writes diagnostics to `/var/lib/plow/boot.log`. A container that appears `Up` can still be parked before OpenClaw starts. Look for `plow-boot: identity resolved to ln_xxx`, gateway startup, and `connected account=chat` in the agent logs. `Identity request failed after 10 attempts` means the boot process could not reach the Plow API; inspect DNS and connectivity from inside the container before investigating SMS routing. Check that `PLOW_API_BASE` names the API root without `/v1`. Never print `PLOW_AGENT_TOKEN`, credential-file contents, or gateway passwords.

Now **text the PartRadar phone number** shown by `plow-agents lines`: “Hello PartRadar. Reply with your name and one sentence explaining what you do.” Confirm the inbound turn and outbound SMS before a longer investigation. Then ask: “Find an FDM-printable enclosure for a Raspberry Pi Zero with an RPIZ CAM 5MP 120 camera. Check license and editable source before suggesting design.” Inspect the response for a cited `FOUND`, `ADAPTABLE`, or `NOT_FOUND`, an honest account of unknown dimensions, and an artifact ID. A live investigation needs working research access. If the result requires design, inspect the persisted `DesignRequired` and engineering order:

```sh
podman compose exec agent sh -lc 'find /var/lib/plow/research -name engineering-order.json -print'
podman compose exec agent cat /var/lib/plow/research/REQ-NNNN/engineering-order.json
```

The order's `OPEN` status means it is ready for engineering review; it does not mean the team has accepted it. Restart the container and confirm the same files still exist in the named `state` volume.

After the text, verify an OpenClaw session database exists and run the client `--dry-run` above to see nonzero usage. Wait one reporting interval (about five minutes), inspect `podman compose logs agent` for reporter errors, then confirm activity on the [Agent Index](https://aiworthusing.com/agent-index). `AGENT_ID` must be the real chosen slug, and the container needs a reachable Plow and Index service. An empty slug disables upstream reporting.

To pause local testing, use `podman compose down` and keep the named volume. Revoke the Plow agent only when intentionally retiring its line-bound credential.

## Release image with Podman

The cloud host starts the image without this Compose file, so `AGENT_ID` must be baked into the variant image. Build in Docker image format to preserve the inherited image metadata; Podman's default OCI format can warn that Docker `HEALTHCHECK` metadata is ignored. This warning does not explain the local SMS failure, but the release image should use the explicit format:

```sh
podman build --format docker --platform linux/amd64 --build-arg AGENT_ID=partradar -t ghcr.io/edge-robot/partradar:v1 .
podman run --rm --entrypoint printenv ghcr.io/edge-robot/partradar:v1 AGENT_ID
podman login ghcr.io -u YOUR_GITHUB_USERNAME
podman push --digestfile partradar-image.digest ghcr.io/edge-robot/partradar:v1
# Use ghcr.io/edge-robot/partradar@sha256:IMAGE_DIGEST after making the package public.
plow-agents deploy ghcr.io/edge-robot/partradar@sha256:IMAGE_DIGEST --line ln_xxx
plow-agents agents
```

The current `plow-agents image build` command does not accept build arguments, and its `image push` command invokes Docker; use Podman directly on this machine. Confirm that the printed `AGENT_ID` is `partradar` before push; rebuild without cache if it is not. A GitHub classic PAT with `write:packages` is needed for GHCR push. Make the package public in GitHub settings before Plow pulls it. Record the immutable push digest, keep `partradar-image.digest` out of Git, and deploy by digest. Check `plow-agents agents` until running, then text the line and repeat the usage test. Do not commit registry credentials. Publication and one-click admission are covered in [publishing.md](publishing.md).
