# SAE QNX Assurance Bridge — Cloudflare STAGE

## Identity and registration
Cloudflare Access protects the app with One-time PIN. The existing policy is restricted to the owner and Cloudflare account members. First authenticated access creates a profile in the dedicated KV registry. Additional users require an Access allow-policy entry and owner approval. This is invite-controlled registration, not public signup.

## Architecture
- Cloudflare Worker: dashboard and API.
- Cloudflare Access: one-time PIN identity boundary.
- Dedicated EU Workers KV: profiles, pairing codes, agent token hashes, jobs and audit records.
- Dedicated R2 bucket: execution evidence JSON, source reports and build logs uploaded by the agent.
- Public agent Worker: isolated pairing and token-authenticated job polling; the dashboard remains behind Cloudflare Access.
- Local Python agent: five fixed actions only; subprocess uses shell=False.

D1 creation was attempted but the account reached its system limit of ten D1 databases. The application does not reuse another project's D1 database. KV is a key-value registry, not a relational database.

## Pair Windows host
1. Sign in to the dashboard and click Generate pairing code.
2. From the repository root run: python agent/sae_qnx_agent.py pair --url https://qnx-agent.profmanuelgago.pw --code YOUR_CODE
3. Start: python agent/sae_qnx_agent.py run
4. Keep the agent running while submitting diagnostics in the dashboard.

The agent token is stored under ~/.sae-qnx-assurance/agent.json. Protect it.

## Allowlisted actions
inspect SDK, CLI self-test, Python unit tests, AArch64 cross-build, x86_64 cross-build. No arbitrary shell, remote script, destructive command, credential extraction or SDK redistribution.

## Evidence semantics
Successful compilation proves cross-compilation and ELF validation only. It does not prove target runtime. AArch64 runtime is unverified. No ISO 26262, IEC 61508, cybersecurity or production-safety certification is claimed.

## Cost
No paid external AI API, email vendor, payment gateway or proprietary SDK is integrated. Cloudflare quotas and pricing can change; usage above free quotas may incur charges. QNX SDK/images remain subject to QNX licensing.


## Deployment record and operational constraints

The dashboard Worker and the separate agent Worker are deployed on Workers.dev. The dashboard is protected by the existing Cloudflare Access application; the agent endpoint is public at the network edge but requires a one-time pairing code and a bearer token for all subsequent calls. Pairing codes are 128-bit random values and expire after 10 minutes. Newly issued agent tokens expire after 90 days. The initial machine token predates that expiry setting and remains active until explicitly rotated.

The KV namespace is created with EU jurisdiction. The R2 bucket was created with a WEUR location hint but its jurisdiction is the default jurisdiction; do not represent it as EU-jurisdiction storage. The account has no available D1 database slot because it has reached the system maximum of ten databases.

The agent polls the KV job registry. KV is eventually consistent, so this STAGE queue is intended for one local agent and low-volume diagnostic jobs, not concurrent high-throughput scheduling. The agent runs only the fixed allowlist and sends result JSON and relevant evidence files to R2.


## Connectivity repair — 2026-11-26
The agent API is now attached to the custom Worker domain `https://qnx-agent.profmanuelgago.pw` rather than relying on the `workers.dev` hostname. The local agent sends the descriptive User-Agent `SAE-QNX-Assurance-Agent/0.3 (+https://qnx.profmanuelgago.pw)`; it does not impersonate a browser. Cloudflare Browser Integrity Check is disabled only for requests matching the exact host `qnx-agent.profmanuelgago.pw` and paths beginning `/api/agent/`. The zone-wide Browser Integrity Check remains enabled. The agent returned HTTP 401 for an unauthenticated API request (expected), and authenticated heartbeat traffic was observed in the dedicated KV registry.

Live end-to-end job verification: `self-test` and `unit-tests` were accepted by the local agent, both exited 0, and their result JSON files were uploaded to the dedicated R2 bucket:
- `jobs/live-selftest-20261126-0129/result.json`
- `jobs/live-unit-tests-20261126-0129/result.json`
The unit-test evidence records 5/5 passing tests. This proves agent-to-Worker communication, allowlisted execution, and R2 result upload. It does not complete Cloudflare Access first-login validation, token rotation, AArch64 runtime validation, or production certification.

Updated endpoints:
- Dashboard: `https://qnx.profmanuelgago.pw` (Cloudflare Access protected)
- Agent API: `https://qnx-agent.profmanuelgago.pw` (public edge, bearer-token protected)
- Original `workers.dev` hostnames are retained as deployment endpoints but are not the configured endpoint for the local agent.
