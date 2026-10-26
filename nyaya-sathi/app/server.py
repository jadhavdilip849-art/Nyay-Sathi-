"""
Nyaya Sathi HTTP REST and Static Application Server.
Built with Python 3.12 standard library: ThreadingHTTPServer, json, and urllib.
Provides RESTful APIs for all 5 core modules, voice integrations, and static asset serving.
"""

import os
import json
import mimetypes
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
from typing import Dict, List, Any, Optional

from .config import HOST, PORT, BASE_DIR, SARVAM_API_KEY, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
from .legal_kb.rag_engine import LegalRAGEngine
from .legal_kb.sources_catalog import AUTHORITATIVE_SOURCES
from .legal_aid.legal_aid_service import LegalAidService
from .authorities.authority_service import AuthorityRecommendationService
from .complaints.complaint_generator import ComplaintGenerator
from .document_explainer.doc_analyzer import DocumentAnalyzer
from .document_explainer.sample_notices import SAMPLE_NOTICES
from .guardrails.safety_checker import SafetyGuardrailEngine
from .voice.sarvam_client import SarvamAIClient

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multi-threaded HTTP server for handling concurrent browser and API requests."""
    daemon_threads = True

class NyayaSathiHandler(BaseHTTPRequestHandler):
    """Main request handler for Nyaya Sathi APIs and frontend."""

    rag_engine = LegalRAGEngine()
    legal_aid_service = LegalAidService()
    authority_service = AuthorityRecommendationService()
    complaint_gen = ComplaintGenerator()
    doc_analyzer = DocumentAnalyzer()
    safety_checker = SafetyGuardrailEngine()
    sarvam_client = SarvamAIClient()

    def log_message(self, format, *args):
        """Custom privacy-preserving logger that hides query strings and personal data."""
        # Suppress noisy standard logs, only print method and path prefix
        print(f"[{self.command}] {self.path.split('?')[0]} - {args[1] if len(args) > 1 else ''}")

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, api-subscription-key")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def _send_json(self, data: Any, status: int = 200):
        response_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(response_bytes)

    def _read_json_body(self) -> Dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body_bytes = self.rfile.read(content_length)
        return json.loads(body_bytes.decode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        try:
            # 1. API Health Check
            if path == "/api/health":
                self._send_json({
                    "status": "healthy",
                    "app": "Nyaya Sathi",
                    "tagline": "Know Your Rights. Understand the Law. Take the Next Step.",
                    "version": "1.0.0-hackathon-prototype",
                    "sarvam_ai_configured": self.sarvam_client.is_configured(),
                    "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
                    "features": [
                        "understand_my_rights",
                        "explain_my_document",
                        "help_me_write_complaint",
                        "find_free_legal_help",
                        "find_the_right_authority",
                        "voice_assistant"
                    ]
                })
                return

            # 2. Legal Categories List
            if path == "/api/rights/categories":
                categories_list = [
                    {
                        "id": key,
                        "name_mr": data["domain_name_mr"],
                        "name_hi": data["domain_name_hi"],
                        "name_en": data["domain_name_en"],
                        "sample_query_mr": data["keywords"][0],
                        "sample_query_hi": data["keywords"][7] if len(data["keywords"]) > 7 else data["keywords"][0]
                    }
                    for key, data in self.rag_engine.domains.items()
                ]
                self._send_json({"categories": categories_list})
                return

            # 3. Document Explainer Sample Notices
            if path == "/api/document/samples":
                self._send_json({"samples": list(SAMPLE_NOTICES.values())})
                return

            # 4. Legal Aid Directory Lookup
            if path == "/api/legalaid/directory":
                state = query_params.get("state", ["Maharashtra"])[0]
                district = query_params.get("district", ["Pune"])[0]
                directory_info = self.legal_aid_service.get_contacts(state=state, district=district)
                self._send_json(directory_info)
                return

            # 5. Hackathon Demonstration Scenarios
            if path == "/api/demo/scenarios":
                scenarios = {
                    "demo_a": {
                        "id": "demo_a",
                        "title": "DEMO A: Unpaid Wages (Marathi / मराठी)",
                        "language": "mr-IN",
                        "user_persona": "रुपेश पाटील (कारखाना कामगार / Industrial Worker)",
                        "user_speech_input": "मी गेल्या दोन महिन्यांपासून एका कारखान्यात काम करत आहे, पण मालकाने अजूनही माझा पगार दिलेला नाही. मी काय करू शकतो?",
                        "facts": {
                            "complainant_name": "रुपेश तुकाराम पाटील",
                            "complainant_address": "घर क्र. १२, भोसरी एमआयडीसी, पुणे - ४११०२६",
                            "complainant_phone": "९८२२००११२२",
                            "opposite_party_name": "सनशाईन मॅन्युफॅक्चरिंग प्रा. लि.",
                            "opposite_party_address": "प्लॉट क्र. ५२, सेक्टर बी, एमआयडीसी भोसरी, पुणे",
                            "matter_type": "unpaid_wages",
                            "dates_involved": "१ ऑगस्ट २०२६ ते ३० सप्टेंबर २०२६ (दोन महिने)",
                            "factual_summary": "मी सनशाईन मॅन्युफॅक्चरिंगमध्ये असेंब्ली ऑपरेटर म्हणून काम करतो. माझे मासिक वेतन रु. २२,५०० आहे. ऑगस्ट आणि सप्टेंबर २०२६ या दोन महिन्यांचे एकूण रु. ४५,००० वेतन मालकाने अद्याप दिलेले नाही.",
                            "prior_action_taken": "मी पर्यवेक्षक आणि व्यवस्थापनाला तोंडी विचारणा केली आणि व्हॉट्सॲपवर विनंती केली, पण टाळाटाळ करण्यात आली.",
                            "requested_relief": "माझे थकीत ४५,००० रुपये तात्काळ बँकेत जमा करण्यात यावेत."
                        }
                    },
                    "demo_b": {
                        "id": "demo_b",
                        "title": "DEMO B: Understanding a Government Notice (Show Cause)",
                        "language": "mr-IN",
                        "document_id": "MUNICIPAL_SHOW_CAUSE",
                        "sample_doc": SAMPLE_NOTICES["MUNICIPAL_SHOW_CAUSE"]
                    },
                    "demo_c": {
                        "id": "demo_c",
                        "title": "DEMO C: Finding Free Legal Aid (Section 12 Eligibility)",
                        "language": "mr-IN",
                        "user_persona": "सुनीता कांबळे (पुणे, गृहिणी/महिला)",
                        "eligibility_check": {
                            "category": "woman",
                            "state": "Maharashtra",
                            "district": "Pune"
                        }
                    }
                }
                self._send_json({"scenarios": scenarios})
                return

            # Static File Serving (SPA Frontend)
            static_dir = os.path.join(BASE_DIR, "static")
            if path == "/" or path == "":
                filepath = os.path.join(static_dir, "index.html")
            else:
                # Remove leading slash and normalize
                clean_path = path.lstrip("/")
                filepath = os.path.join(static_dir, clean_path)

            # Security: ensure requested path is within static_dir
            if not os.path.abspath(filepath).startswith(os.path.abspath(static_dir)):
                self.send_error(403, "Access Denied")
                return

            if os.path.exists(filepath) and os.path.isfile(filepath):
                mime_type, _ = mimetypes.guess_type(filepath)
                mime_type = mime_type or "application/octet-stream"

                with open(filepath, "rb") as f:
                    content = f.read()

                self.send_response(200)
                self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if "text" in mime_type or "javascript" in mime_type else mime_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                # Fallback to index.html for client-side routing
                index_path = os.path.join(static_dir, "index.html")
                if os.path.exists(index_path):
                    with open(index_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(content)))
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(content)
                    return

            self.send_error(404, f"File Not Found: {path}")

        except Exception as e:
            traceback.print_exc()
            self._send_json({"error": True, "message": str(e)}, status=500)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            body = self._read_json_body()

            # 1. Understand My Rights & Conversational Query
            if path == "/api/rights/query":
                query = body.get("query", "").strip()
                category = body.get("category")
                lang = body.get("language", DEFAULT_LANGUAGE)

                if not query:
                    self._send_json({"error": True, "message": "Query text cannot be empty."}, status=400)
                    return

                # Check safety & emergency guardrails first
                safety_report = self.safety_checker.check_query_safety(query)
                
                # Retrieve legal information through RAG
                rag_result = self.rag_engine.retrieve(query=query, explicit_category=category)

                # Combine safety escalation if urgent
                rag_result["safety"] = safety_report

                self._send_json(rag_result)
                return

            # 2. Document Explainer
            if path == "/api/document/explain":
                doc_text = body.get("text", "")
                sample_id = body.get("sample_id")
                lang = body.get("language", DEFAULT_LANGUAGE)

                if sample_id and sample_id in SAMPLE_NOTICES:
                    doc_text = SAMPLE_NOTICES[sample_id]["raw_text"]

                analysis = self.doc_analyzer.analyze_document(text=doc_text, user_language=lang)
                self._send_json(analysis)
                return

            # 3. Factual Complaint Drafting
            if path == "/api/complaint/draft":
                complaint_data = self.complaint_gen.generate_complaint(
                    complainant_name=body.get("complainant_name", ""),
                    complainant_address=body.get("complainant_address", ""),
                    complainant_phone=body.get("complainant_phone", ""),
                    opposite_party_name=body.get("opposite_party_name", ""),
                    opposite_party_address=body.get("opposite_party_address", ""),
                    matter_type=body.get("matter_type", "unpaid_wages"),
                    dates_involved=body.get("dates_involved", ""),
                    factual_summary=body.get("factual_summary", ""),
                    prior_action_taken=body.get("prior_action_taken", ""),
                    requested_relief=body.get("requested_relief", ""),
                    language=body.get("language", DEFAULT_LANGUAGE)
                )
                self._send_json(complaint_data)
                return

            # 4. Legal Aid Statutory Eligibility Check
            if path == "/api/legalaid/eligibility":
                category = body.get("category", "woman")
                income = body.get("annual_income")
                state = body.get("state", "Maharashtra")
                result = self.legal_aid_service.evaluate_eligibility(category=category, annual_income=income, state=state)
                self._send_json(result)
                return

            # 5. Authority Recommendation
            if path == "/api/authority/recommend":
                domain_key = body.get("domain", "unpaid_wages")
                state = body.get("state", "Maharashtra")
                amount = body.get("dispute_amount")
                result = self.authority_service.recommend_authority(domain_key=domain_key, state=state, dispute_amount=amount)
                self._send_json(result)
                return

            # 6. Sarvam AI Text-to-Speech Endpoint
            if path == "/api/voice/tts":
                text = body.get("text", "")
                target_lang = body.get("language", DEFAULT_LANGUAGE)
                tts_result = self.sarvam_client.text_to_speech(text=text, target_language_code=target_lang)
                self._send_json(tts_result)
                return

            # 7. Sarvam AI Translation Endpoint
            if path == "/api/voice/translate":
                text = body.get("text", "")
                source_lang = body.get("source_language", "en-IN")
                target_lang = body.get("target_language", "mr-IN")
                trans_result = self.sarvam_client.translate_text(text=text, source_lang=source_lang, target_lang=target_lang)
                self._send_json(trans_result)
                return

            self.send_error(404, f"API Endpoint Not Found: {path}")

        except Exception as e:
            traceback.print_exc()
            self._send_json({"error": True, "message": str(e)}, status=500)

def run_server(host: str = HOST, port: int = PORT):
    """Starts the multi-threaded HTTP server."""
    server_address = (host, port)
    httpd = ThreadedHTTPServer(server_address, NyayaSathiHandler)
    print(f"============================================================")
    print(f"  NYAYA SATHI - Multilingual AI Legal Assistant Prototype   ")
    print(f"  Know Your Rights. Understand the Law. Take the Next Step.  ")
    print(f"============================================================")
    print(f"  Server listening on http://{host}:{port}")
    print(f"  Sarvam AI API Active: {NyayaSathiHandler.sarvam_client.is_configured()}")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server cleanly...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
