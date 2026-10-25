"""Tests for privacy-safe, correlatable local audit events."""

import json
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from reference_service.audit import JsonlAuditLog, build_event


class AuditEventTests(unittest.TestCase):
    def test_event_has_correlation_metadata_without_prompt_fields(self):
        request_id = str(uuid4())
        event = build_event(
            request_id=request_id, actor_id="persona:engineering",
            action="policy_decision", outcome="denied",
            source_ids=["doc-finance-forecast"], policy_reason="audience_mismatch",
        )
        self.assertEqual(request_id, event["request_id"])
        self.assertEqual(["doc-finance-forecast"], event["source_ids"])
        self.assertEqual("denied", event["outcome"])
        self.assertNotIn("prompt", event)
        self.assertNotIn("snippet", event)
        self.assertNotIn("answer", event)

    def test_two_events_correlate_by_request_id(self):
        request_id = str(uuid4())
        first = build_event(request_id=request_id, actor_id="persona:engineering",
                            action="search", outcome="success")
        second = build_event(request_id=request_id, actor_id="persona:engineering",
                             action="policy_decision", outcome="denied",
                             source_ids=["doc-finance-forecast"], policy_reason="audience_mismatch")
        self.assertEqual(first["request_id"], second["request_id"])

    def test_sensitive_values_are_redacted_and_control_chars_removed(self):
        event = build_event(
            request_id=str(uuid4()), actor_id="persona:engineering",
            action="failure", outcome="failure",
            policy_reason="contact user@example.com\nBearer abc.def.ghi password=hunter2",
        )
        serialized = json.dumps(event)
        self.assertNotIn("user@example.com", serialized)
        self.assertNotIn("abc.def.ghi", serialized)
        self.assertNotIn("hunter2", serialized)
        self.assertNotIn("\n", event["policy_reason"])
        self.assertIn("[REDACTED_EMAIL]", event["policy_reason"])
        self.assertIn("[REDACTED_TOKEN]", event["policy_reason"])

    def test_unknown_fields_are_not_persisted(self):
        with tempfile.TemporaryDirectory() as directory:
            log = JsonlAuditLog(Path(directory) / "events.jsonl")
            event = build_event(request_id=str(uuid4()), actor_id="actor-1",
                                action="search", outcome="success")
            event["prompt"] = "confidential prompt text"
            saved = log.append(event)
            self.assertNotIn("prompt", saved)
            self.assertNotIn("confidential prompt text", log.path.read_text())

    def test_jsonl_is_append_only_and_round_trips(self):
        with tempfile.TemporaryDirectory() as directory:
            log = JsonlAuditLog(Path(directory) / "events.jsonl")
            first = build_event(request_id=str(uuid4()), actor_id="actor-1",
                                action="search", outcome="success")
            second = build_event(request_id=first["request_id"], actor_id="actor-1",
                                 action="policy_decision", outcome="denied",
                                 source_ids=["doc-restricted"], policy_reason="not_authorized")
            log.append(first)
            log.append(second)
            rows = log.read()
            self.assertEqual(2, len(rows))
            self.assertEqual(first["request_id"], rows[1]["request_id"])
            self.assertEqual(2, len(log.path.read_text(encoding="utf-8").splitlines()))

    def test_rejects_non_uuid_request_id_and_unsupported_action(self):
        with self.assertRaises(ValueError):
            build_event(request_id="not-a-uuid", actor_id="actor-1",
                        action="search", outcome="success")
        with self.assertRaises(ValueError):
            build_event(request_id=str(uuid4()), actor_id="actor-1",
                        action="unknown", outcome="success")

    def test_rejects_multiline_and_invalid_ids(self):
        with self.assertRaises(ValueError):
            build_event(request_id=str(uuid4()), actor_id="actor\nspoof",
                        action="search", outcome="success")
        with self.assertRaises(ValueError):
            build_event(request_id=str(uuid4()), actor_id="actor-1",
                        action="search", outcome="success", source_ids=["../secret"])


if __name__ == "__main__":
    unittest.main()
