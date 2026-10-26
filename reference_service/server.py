"""Run the dependency-free local HTTP service with Python 3.12."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .audit import JsonlAuditLog, build_event
from .contracts import RequestValidationError
from .service import ReferenceService


class RequestHandler(BaseHTTPRequestHandler):
    service = ReferenceService()
    audit_log = JsonlAuditLog('.local/audit.jsonl')

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


    def _record_query_event(self, result):
        request_id = self.headers.get("X-Request-ID")
        if not request_id:
            return
        try:
            event = build_event(
                request_id=request_id,
                actor_id=result["persona_id"],
                action="search",
                outcome="success",
            )
            self.audit_log.append(event)
        except ValueError:
            # Invalid correlation metadata must not affect the query response.
            return

    def do_GET(self):
        if self.path == "/healthz":
            self._send_json(200, self.service.health())
        else:
            self._send_json(404, {"error": "Not found."})

    def do_POST(self):
        if self.path != "/v1/query":
            self._send_json(404, {"error": "Not found."})
            return
        try:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError as error:
                raise RequestValidationError(
                    "Content-Length must be an integer."
                ) from error
            if length <= 0 or length > 16384:
                raise RequestValidationError("Body must be between 1 and 16384 bytes.")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            result = self.service.submit_query(payload)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(400, {"error": "Body must contain valid UTF-8 JSON."})
        except RequestValidationError as error:
            self._send_json(400, {"error": str(error)})
        else:
            self._record_query_event(result)
            self._send_json(200, result)

    def log_message(self, format_string, *args):
        # Keep local demo logs free of request bodies and query contents.
        super().log_message(format_string, *args)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8001), RequestHandler)
    print("NexusVault fake reference service: http://127.0.0.1:8001")
    print("Local demo only; no production authentication or authorization.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping local reference service.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
