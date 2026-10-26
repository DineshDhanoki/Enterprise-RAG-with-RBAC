"""Minimal privacy-aware JSONL audit event writer for the local slice."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
from threading import Lock
from uuid import UUID

SCHEMA_VERSION = 1
MAX_TEXT_LENGTH = 240
MAX_SOURCE_IDS = 100
REDACTIONS = (
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"), "[REDACTED_TOKEN]"),
    (re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"), r"\1=[REDACTED]"),
    (re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"), "[REDACTED_EMAIL]"),
    (re.compile(r"(?<!\d)(?:\+?\d[\d .()/-]{7,}\d)(?!\d)"), "[REDACTED_PHONE]"),
)
ALLOWED_ACTIONS = {"search", "policy_decision", "citation", "sync", "failure", "answer"}
ALLOWED_OUTCOMES = {"allowed", "denied", "success", "failure", "filtered", "partial"}
ALLOWED_POLICY_REASONS = {
    "audience_mismatch",
    "not_authorized",
    "no_matching_policy",
    "source_filtered",
    "upstream_error",
    "validation_error",
    "internal_error",
}
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


def _safe_text(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    value = _CONTROL_CHARS.sub(" ", value)
    for pattern, replacement in REDACTIONS:
        value = pattern.sub(replacement, value)
    return " ".join(value.split())[:MAX_TEXT_LENGTH]


def _opaque_id(value: object, field: str) -> str:
    result = _safe_text(value, field)
    if not result or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}", result):
        raise ValueError(f"{field} must be a non-empty opaque identifier")
    return result


def _policy_reason(value: object) -> str:
    if value == "":
        return ""
    if not isinstance(value, str) or value not in ALLOWED_POLICY_REASONS:
        raise ValueError("policy_reason must be a known opaque code")
    return value


def build_event(*, request_id: str, actor_id: str, action: str, outcome: str,
                source_ids=(), policy_reason: str = "", collection_id: str = "") -> dict:
    """Build an allowlisted event. Caller must use opaque identifiers and codes."""
    try:
        normalized_request_id = str(UUID(str(request_id)))
    except (ValueError, TypeError, AttributeError) as error:
        raise ValueError("request_id must be a UUID") from error
    if action not in ALLOWED_ACTIONS:
        raise ValueError("unsupported audit action")
    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError("unsupported audit outcome")
    if isinstance(source_ids, (str, bytes)):
        raise ValueError("source_ids must be a sequence of opaque IDs")
    ids = [_opaque_id(item, "source_id") for item in source_ids]
    if len(ids) > MAX_SOURCE_IDS:
        raise ValueError("too many source IDs")
    return {
        "schema_version": SCHEMA_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "request_id": normalized_request_id,
        "actor_id": _opaque_id(actor_id, "actor_id"),
        "action": action,
        "outcome": outcome,
        "source_ids": ids,
        "policy_reason": _policy_reason(policy_reason),
        "collection_id": _opaque_id(collection_id, "collection_id") if collection_id else "",
    }


class JsonlAuditLog:
    """Append-only-at-the-API JSONL writer; filesystem owners can still alter it."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._lock = Lock()

    def append(self, event: dict) -> dict:
        clean = build_event(
            request_id=event.get("request_id"),
            actor_id=event.get("actor_id"),
            action=event.get("action"),
            outcome=event.get("outcome"),
            source_ids=event.get("source_ids", ()),
            policy_reason=event.get("policy_reason", ""),
            collection_id=event.get("collection_id", ""),
        )
        line = json.dumps(clean, ensure_ascii=True, separators=(",", ":")) + "\n"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(line)
                stream.flush()
        return clean

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        events = []
        with self.path.open("r", encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                item = json.loads(line)
                if isinstance(item, dict):
                    events.append(item)
        return events
