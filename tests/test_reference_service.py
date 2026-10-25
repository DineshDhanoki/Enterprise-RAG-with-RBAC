"""Unit tests for fake fixture loading and the request contract."""

import unittest

from reference_service.contracts import RequestValidationError, parse_query_request
from reference_service.fixtures import load_fixtures
from reference_service.service import ReferenceService


class FixtureTests(unittest.TestCase):
    def test_three_fake_personas_and_documents_are_available(self):
        personas, documents = load_fixtures()
        self.assertEqual({"engineering", "finance", "people_ops"}, set(personas))
        self.assertGreaterEqual(len(documents), 3)
        for persona_id in personas:
            allowed = [doc for doc in documents if persona_id in doc["audience"]]
            denied = [doc for doc in documents if persona_id not in doc["audience"]]
            self.assertTrue(allowed, f"{persona_id} needs an allowed fixture")
            self.assertTrue(denied, f"{persona_id} needs a denied fixture")

    def test_fixture_results_are_independent_copies(self):
        first_personas, first_documents = load_fixtures()
        first_personas.clear()
        first_documents[0]["audience"].append("unexpected")
        second_personas, second_documents = load_fixtures()
        self.assertIn("engineering", second_personas)
        self.assertNotIn("unexpected", second_documents[0]["audience"])


class RequestContractTests(unittest.TestCase):
    def test_valid_request_is_normalized(self):
        request = parse_query_request(
            {"persona_id": " engineering ", "question": "  What changed?  "}
        )
        self.assertEqual("engineering", request.persona_id)
        self.assertEqual("What changed?", request.question)

    def test_rejects_non_object_payload(self):
        with self.assertRaises(RequestValidationError):
            parse_query_request([])

    def test_rejects_missing_or_blank_fields(self):
        for payload in (
            {},
            {"persona_id": "engineering"},
            {"persona_id": " ", "question": "hello"},
            {"persona_id": "engineering", "question": " "},
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(RequestValidationError):
                    parse_query_request(payload)

    def test_rejects_oversized_question(self):
        with self.assertRaises(RequestValidationError):
            parse_query_request(
                {"persona_id": "engineering", "question": "x" * 2001}
            )

    def test_service_rejects_unknown_fake_persona(self):
        service = ReferenceService()
        with self.assertRaises(RequestValidationError):
            service.submit_query({"persona_id": "unknown", "question": "hello"})

    def test_service_returns_empty_skeleton_response(self):
        service = ReferenceService()
        result = service.submit_query(
            {"persona_id": "engineering", "question": "What changed?"}
        )
        self.assertEqual("accepted", result["status"])
        self.assertIsNone(result["answer"])
        self.assertEqual([], result["sources"])


if __name__ == "__main__":
    unittest.main()
