FROM public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-e0217de7c4fc5d8b7655aa4a1aaac8ed9f79cdf7@sha256:8696c41d26305fa28e825fb72531fade37e9dd2ad52df2fdb395f68681523243

# The final slug is supplied by the owner at build time. An empty ID leaves
# upstream reporting dormant during development; cloud deployments must set it.
ARG AGENT_ID=""
ENV AGENT_ID=${AGENT_ID} \
    AGENT_NAME=PartRadar \
    AGENT_BLURB="Search first. Design only when necessary." \
    AGENT_RUNTIME=OpenClaw

COPY --chown=node:node prompt/AGENTS.md /opt/plow/prompt/AGENTS.md
COPY --chown=node:node skills/ /opt/plow/skills/
COPY --chown=node:node tools/part_radar.py /opt/plow/part-radar/part_radar.py
