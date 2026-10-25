"""Application boundary; policy and retrieval are intentionally not implemented."""

from .contracts import parse_query_request
from .fixtures import load_fixtures


class ReferenceService:
    def __init__(self):
        self.personas, self.documents = load_fixtures()

    def health(self):
        return {"status": "ok", "mode": "local-fake-data"}

    def submit_query(self, payload):
        request = parse_query_request(payload)
        if request.persona_id not in self.personas:
            from .contracts import RequestValidationError

            raise RequestValidationError("Unknown demo persona.")

        # This is only the request/response seam. A later issue adds policy
        # decisions and filtered retrieval before any source enters a context.
        return {
            "status": "accepted",
            "persona_id": request.persona_id,
            "question": request.question,
            "answer": None,
            "sources": [],
            "note": "Skeleton only: no policy enforcement or retrieval is active.",
        }
