# Local reference service

This is a deliberately small Python 3.12 service using only the standard library. It is a local contract and fixture boundary for future policy and retrieval work—not a production backend.

## Run

From the repository root:

```bash
python3.12 -m unittest discover -s tests -v
python3.12 -m reference_service.server
```

The server binds only to `127.0.0.1:8001`. Stop it with Ctrl+C.

## Endpoints

- `GET /healthz` returns a local health response.
- `POST /v1/query` accepts a JSON object with `persona_id` and `question`.

Example:

```bash
curl -sS http://127.0.0.1:8001/v1/query \\
  -H 'Content-Type: application/json' \\
  -d '{"persona_id":"engineering","question":"What changed?"}'
```

The response is intentionally a skeleton: `answer` is null and `sources` is empty. Unknown personas and invalid requests receive a 400 response. There is no retrieval or authorization decision in this issue; the next slice must put policy enforcement before retrieval.

## Module boundaries

- `fixtures.py`: deterministic, fictional personas and documents with audience metadata.
- `contracts.py`: validated request data contract.
- `service.py`: application boundary that later policy and retrieval components will implement behind.
- `server.py`: standard-library HTTP adapter; it does not make authorization decisions.

The three personas—Engineering, Finance, and People Ops—are fake local test identities. Document audience metadata exists to make allowed/denied fixture cases explicit for tests; it is not enforced by this skeleton.

## Trust boundary and limitations

The service trusts neither the public demo nor a browser role as a production identity. However, this slice itself has no authentication, session management, authorization enforcement, tenant isolation, audit trail, persistent storage, rate limiting, or hardened deployment configuration. Anyone able to reach the local process can submit a fake persona ID. Do not expose it to a network, use real documents, or rely on it to protect data. The public GitHub Pages UI remains a simulated design demo and is not connected to this service.
