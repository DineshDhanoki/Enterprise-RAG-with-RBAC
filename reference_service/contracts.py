"""Input and output contracts for the local query endpoint."""

from dataclasses import dataclass


@dataclass(frozen=True)
class QueryRequest:
    persona_id: str
    question: str


class RequestValidationError(ValueError):
    """Raised when a query request does not match the public contract."""


def parse_query_request(payload):
    if not isinstance(payload, dict):
        raise RequestValidationError("Request body must be a JSON object.")

    persona_id = payload.get("persona_id")
    question = payload.get("question")

    if not isinstance(persona_id, str) or not persona_id.strip():
        raise RequestValidationError("persona_id must be a non-empty string.")
    if not isinstance(question, str) or not question.strip():
        raise RequestValidationError("question must be a non-empty string.")
    if len(question) > 2000:
        raise RequestValidationError("question must be at most 2000 characters.")

    return QueryRequest(persona_id=persona_id.strip(), question=question.strip())
