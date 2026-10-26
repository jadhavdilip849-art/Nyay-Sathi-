"""
Mock Socket / In-Memory Integration Tests for NyayaSathiHandler.
Tests actual HTTP request parsing, routing, JSON generation, and error handling
completely in-memory without requiring OS TCP port bindings.
"""

import unittest
import io
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.server import NyayaSathiHandler

class DummyServer:
    def __init__(self):
        self.server_name = "localhost"
        self.server_port = 8080

class MockSocket:
    def __init__(self, request_bytes):
        self.rfile = io.BytesIO(request_bytes)
        self.output_buffer = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if 'r' in mode:
            return self.rfile
        return self.output_buffer

    def sendall(self, b):
        self.output_buffer.write(b)

    def send(self, b):
        self.output_buffer.write(b)
        return len(b)

class TestHandlerInMemory(unittest.TestCase):

    def _execute_request(self, raw_http: str) -> (int, dict, str):
        raw_bytes = raw_http.replace("\n", "\r\n").encode("utf-8")
        sock = MockSocket(raw_bytes)
        handler = NyayaSathiHandler(sock, ("127.0.0.1", 12345), DummyServer())
        
        response_bytes = sock.output_buffer.getvalue()
        # Parse status line and headers
        headers_part, _, body_part = response_bytes.partition(b"\r\n\r\n")
        header_lines = headers_part.decode("utf-8", errors="replace").split("\r\n")
        status_code = int(header_lines[0].split(" ")[1])
        
        headers = {}
        for line in header_lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()

        body_str = body_part.decode("utf-8", errors="replace")
        return status_code, headers, body_str

    def test_health_api(self):
        req = "GET /api/health HTTP/1.1\nHost: localhost\n\n"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers["content-type"])
        data = json.loads(body)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["app"], "Nyaya Sathi")

    def test_rights_categories_api(self):
        req = "GET /api/rights/categories HTTP/1.1\nHost: localhost\n\n"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertTrue(len(data["categories"]) >= 8)

    def test_rights_query_post(self):
        payload = json.dumps({"query": "माझा पगार दिला नाही", "language": "mr-IN"})
        req = f"POST /api/rights/query HTTP/1.1\nHost: localhost\nContent-Type: application/json\nContent-Length: {len(payload.encode('utf-8'))}\n\n{payload}"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertEqual(data["domain_id"], "unpaid_wages")
        self.assertIn("official_citation", data)

    def test_document_explain_post(self):
        payload = json.dumps({"sample_id": "MUNICIPAL_SHOW_CAUSE", "language": "mr-IN"})
        req = f"POST /api/document/explain HTTP/1.1\nHost: localhost\nContent-Type: application/json\nContent-Length: {len(payload.encode('utf-8'))}\n\n{payload}"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("Municipal", data["apparent_document_type"])

    def test_complaint_draft_post(self):
        payload = json.dumps({
            "complainant_name": "रुपेश पाटील",
            "factual_summary": "वेतन मिळालेले नाही",
            "matter_type": "unpaid_wages"
        })
        req = f"POST /api/complaint/draft HTTP/1.1\nHost: localhost\nContent-Type: application/json\nContent-Length: {len(payload.encode('utf-8'))}\n\n{payload}"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("formal_letter_mr", data)

    def test_legalaid_eligibility_post(self):
        payload = json.dumps({"category": "woman", "state": "Maharashtra"})
        req = f"POST /api/legalaid/eligibility HTTP/1.1\nHost: localhost\nContent-Type: application/json\nContent-Length: {len(payload.encode('utf-8'))}\n\n{payload}"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertTrue(data["is_eligible"])

    def test_legalaid_directory_get(self):
        req = "GET /api/legalaid/directory?state=Maharashtra&district=pune HTTP/1.1\nHost: localhost\n\n"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("district_authority", data)

    def test_static_index_html(self):
        req = "GET / HTTP/1.1\nHost: localhost\n\n"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        self.assertIn("text/html", headers["content-type"])
        self.assertIn("न्याय साथी (Nyaya Sathi)", body)

    def test_static_css(self):
        req = "GET /css/style.css HTTP/1.1\nHost: localhost\n\n"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        self.assertIn("text/css", headers["content-type"])

    def test_static_js(self):
        req = "GET /js/app.js HTTP/1.1\nHost: localhost\n\n"
        status, headers, body = self._execute_request(req)
        self.assertEqual(status, 200)
        self.assertIn("javascript", headers["content-type"])

if __name__ == "__main__":
    unittest.main()
