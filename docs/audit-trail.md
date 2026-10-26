# Privacy-safe audit trail (local reference)

This module records metadata about local reference-slice activity. It is not a tamper-proof or production audit service.

## Event contract

Each JSONL event has a schema version, a writer-generated UTC timestamp, request ID, actor, action, outcome, source IDs, an opaque policy-reason code, and optional collection. The event payload intentionally has no prompt, answer, snippet, token, password, or raw personal-data field. Unknown input fields are discarded. Policy reasons use a bounded code list rather than free text; other metadata is redacted for common email, phone, bearer-token, and secret-like patterns, and control characters are normalized to prevent log-line injection.

Use stable fake actor IDs and opaque source IDs. Do not place document titles, contents, user-entered text, credentials, or real personal identifiers in actor IDs, source IDs, collection names, or policy reasons. Policy reasons must be one of the documented opaque codes: `audience_mismatch`, `not_authorized`, `no_matching_policy`, `source_filtered`, `upstream_error`, `validation_error`, or `internal_error`. Redaction is a defense-in-depth filter, not a guarantee that arbitrary personal data can be detected.

## Run and inspect

From the repository root:

```bash
python3.12 -m unittest discover -s tests -v
python3.12 -m reference_service.audit_viewer --file .local/audit.jsonl
```

The viewer binds to `127.0.0.1:8010` and provides filters for actor, outcome, collection, and request ID. It is local-only and read-only.

## Correlation and denied access

Use the same caller-generated request ID for all events produced by one request. For example, a search event and a denied policy decision can be correlated without storing the question. A denied event records the opaque candidate source IDs and a short policy reason; it must not record snippets or document text.

## Append-only behavior and limitations

The JSONL writer opens in append mode, serializes one event per line, and never exposes an update/delete method. This is append-only at the application interface, not immutable storage: a process with filesystem access can edit or remove the file. Production deployments need protected storage, access controls, integrity verification, backups, and operational monitoring.

## Privacy, retention, export, and deletion

The default is data minimization: no prompts, answers, snippets, tokens, or raw request bodies are written. Configure a local file path outside the repository for real deployments; never commit generated logs. Decide and publish a retention period based on legal, contractual, and operational requirements before collecting real data. Apply deletion/expiry at the storage layer, including backups and exports. Restrict exports, encrypt them in transit and at rest, record export access, and remove temporary copies after use. This local reference does not implement scheduled retention or deletion.

## Short threat model

- **Log injection:** attacker-controlled newlines and control characters could forge extra records or corrupt the viewer. The writer replaces control characters and stores each event as one JSON object per line.
- **Accidental content disclosure:** callers may pass prompts, snippets, credentials, or PII in arbitrary fields. The schema allowlists fields, drops unknown keys, and redacts common sensitive patterns in supported strings. Callers must still pass opaque IDs and non-sensitive policy codes; do not treat regex redaction as complete PII detection.
- **Unauthorized log access or tampering:** local file permissions and process access are outside this module. Keep the file local and restricted; this sample is not tamper-proof or production hardened.
- **Denial of service:** cap event fields and bound viewer responses; production systems also need quotas, rotation, and monitoring.
