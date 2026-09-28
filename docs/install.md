# Install and local smoke test

This is the install/tutorial page intended for the future Agent Index listing. Requirements: Docker with Compose 2.24+, Python 3.11+, Git, a phone able to text a Plow line, and the current [`plow-agents` CLI](https://github.com/plow-pbc/plow-agents). The owner needs a Plow account. For web research, connect a supported browser/search capability to OpenClaw, such as the owner's Mac through Latch. The engineering work order needs no external messaging configuration.

## Local Build on Plow flow

Install the CLI as its README documents, then work from the PartRadar repository root:

```sh
plow-agents login
plow-agents lines
cp .env.example .env
# Edit .env: replace YOUR_AGENT_SLUG with the owner-selected Agent Index slug.
plow-agents deploy --local --line ln_xxx
docker compose logs -f agent
```

`login` asks the owner to text an activation code. Choose a free `ln_xxx` from `lines`. The current CLI's `deploy --local` command mints `./plow-credentials` and runs `docker compose up --build -d`; a second `up` is not required. `.env` is read by Compose and passes `AGENT_ID` to the running container and build. `plow-credentials` contains a live scoped token and is ignored by Git and Docker build context. Never paste it into a ticket, commit, or image.

Check runtime state without exposing credentials:

```sh
docker compose ps
docker compose exec agent printenv AGENT_ID
docker compose exec agent test -f /opt/plow/prompt/AGENTS.md
docker compose exec agent test -f /opt/plow/skills/part-research/SKILL.md
docker compose exec agent test -f /opt/plow/agent-index-client.py
docker compose exec agent sh -lc 'find /var/lib/plow/agents -name openclaw-agent.sqlite -print'
docker compose exec agent sh -lc 'HOME=/var/lib/plow OPENCLAW_STATE_DIR=/var/lib/plow python3 /opt/plow/agent-index-client.py status'
docker compose exec agent sh -lc 'HOME=/var/lib/plow OPENCLAW_STATE_DIR=/var/lib/plow python3 /opt/plow/agent-index-client.py --dry-run'
```

Now **text the PartRadar phone number** shown by `plow-agents lines` and confirm that PartRadar replies. Ask: “Find an FDM-printable enclosure for a Raspberry Pi Zero with an RPIZ CAM 5MP 120 camera. Check license and editable source before suggesting design.” Inspect the response for a cited `FOUND`, `ADAPTABLE`, or `NOT_FOUND`, an honest account of unknown dimensions, and an artifact ID. A live investigation needs working research access. If the result requires design, inspect the persisted `DesignRequired` and engineering order:

```sh
docker compose exec agent sh -lc 'find /var/lib/plow/research -name engineering-order.json -print'
docker compose exec agent cat /var/lib/plow/research/REQ-NNNN/engineering-order.json
```

The order's `OPEN` status means it is ready for engineering review; it does not mean the team has accepted it. Restart the container and confirm the same files still exist in the named `state` volume.

After the text, verify an OpenClaw session database exists and run the client `--dry-run` above to see nonzero usage. Wait one reporting interval (about five minutes), inspect `docker compose logs agent` for reporter errors, then confirm activity on the [Agent Index](https://aiworthusing.com/agent-index). `AGENT_ID` must be the real chosen slug, and the container needs a reachable Plow and Index service. An empty slug disables upstream reporting. Keep the Compose `state` volume across restarts; `docker compose down -v` deletes research and Index installation identity.

To stop the local agent after testing, use `plow-agents revoke` and `docker compose down`. Keep the named volume if you expect to restart the same installation.

## Cloud deployment

The cloud host starts the image without this Compose file, so `AGENT_ID` must be baked into the variant image. The final slug is owner supplied. Build explicitly with Docker's build argument, then use the CLI to push the already built image:

```sh
docker build --platform linux/amd64 --build-arg AGENT_ID=YOUR_AGENT_SLUG -t ghcr.io/YOUR_ACCOUNT/partradar:v1 .
docker run --rm --entrypoint printenv ghcr.io/YOUR_ACCOUNT/partradar:v1 AGENT_ID
docker login ghcr.io -u YOUR_GITHUB_USERNAME
plow-agents image push ghcr.io/YOUR_ACCOUNT/partradar:v1
# Record the repository@sha256:... reference printed by push.
plow-agents deploy ghcr.io/YOUR_ACCOUNT/partradar@sha256:IMAGE_DIGEST --line ln_xxx
plow-agents agents
```

The current `plow-agents image build` command does not accept build arguments, so use `docker build --build-arg` for the release image. Confirm that the printed `AGENT_ID` is the owner-selected slug before push; rebuild without cache if it is not. A GitHub classic PAT with `write:packages` is needed for GHCR push; Docker prompts for it. Make the package public in GitHub settings before Plow pulls it. Use the immutable push digest for deployment. Check `plow-agents agents` until running, then text the line and repeat the usage test. Do not commit registry credentials. Publication and one-click admission are covered in [publishing.md](publishing.md).
