"""Read-only local viewer for the JSONL audit reference."""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html import escape
from urllib.parse import parse_qs, urlparse

from .audit import JsonlAuditLog

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>NexusVault local audit viewer</title>
<style>
body{font:15px system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#172033;background:#f7f8fa}
h1{font-size:1.6rem}form{display:flex;flex-wrap:wrap;gap:.6rem;margin:1rem 0}
input,button{padding:.65rem;border:1px solid #ccd2dc;border-radius:6px}button{cursor:pointer}
table{border-collapse:collapse;width:100%;background:white}th,td{text-align:left;padding:.6rem;border-bottom:1px solid #e1e5eb;vertical-align:top}
.muted{color:#5b6472}
</style></head><body><h1>NexusVault audit events</h1>
<p class="muted">Local, read-only metadata view. No prompts, answers, or snippets should be present.</p>
<form method="get">
<input name="actor" placeholder="Actor ID" value="{actor}">
<input name="outcome" placeholder="Outcome" value="{outcome}">
<input name="collection" placeholder="Collection ID" value="{collection}">
<input name="request_id" placeholder="Request ID" value="{request_id}">
<button type="submit">Filter</button><a href="/">Clear</a></form>
<p>{count} event(s)</p><table><thead><tr><th>Time</th><th>Request</th><th>Actor</th><th>Action / outcome</th><th>Collection</th><th>Sources</th><th>Policy reason</th></tr></thead><tbody>{rows}</tbody></table>
</body></html>"""


class AuditViewerHandler(BaseHTTPRequestHandler):
    audit_path = None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/":
            self.send_error(404)
            return
        filters = {key: parse_qs(parsed.query).get(key, [""])[0][:128]
                   for key in ("actor", "outcome", "collection", "request_id")}
        try:
            events = JsonlAuditLog(self.audit_path).read()
        except (OSError, ValueError):
            self.send_error(500, "Unable to read audit file")
            return
        filtered = [
            item for item in events
            if (not filters["actor"] or item.get("actor_id") == filters["actor"])
            and (not filters["outcome"] or item.get("outcome") == filters["outcome"])
            and (not filters["collection"] or item.get("collection_id") == filters["collection"])
            and (not filters["request_id"] or item.get("request_id") == filters["request_id"])
        ]
        rows = []
        for item in reversed(filtered[-500:]):
            cells = [
                item.get("timestamp", ""), item.get("request_id", ""),
                item.get("actor_id", ""), f'{item.get("action", "")} / {item.get("outcome", "")}',
                item.get("collection_id", ""), ", ".join(item.get("source_ids", [])),
                item.get("policy_reason", ""),
            ]
            rows.append("<tr>" + "".join(f"<td>{escape(str(value))}</td>" for value in cells) + "</tr>")
        page = PAGE
        values = {**filters, "count": str(len(filtered)), "rows": "".join(rows)}
        for key, value in values.items():
            page = page.replace("{" + key + "}", escape(str(value)))
        body = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format_string, *args):
        super().log_message("%s", self.path.split("?", 1)[0])


def main():
    parser = argparse.ArgumentParser(description="Serve a local read-only audit viewer.")
    parser.add_argument("--file", default=".local/audit.jsonl", help="Path to JSONL event file")
    parser.add_argument("--port", type=int, default=8010)
    args = parser.parse_args()
    AuditViewerHandler.audit_path = args.file
    server = ThreadingHTTPServer(("127.0.0.1", args.port), AuditViewerHandler)
    print(f"Local audit viewer: http://127.0.0.1:{args.port} (file: {args.file})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping audit viewer.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
