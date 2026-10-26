"""
Unit tests for Legal Document Explainer.
Tests extraction of explicit dates vs inferred deadlines, legal terms decoding,
and lawyer question generation.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.document_explainer.doc_analyzer import DocumentAnalyzer
from app.document_explainer.sample_notices import SAMPLE_NOTICES

class TestDocumentAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DocumentAnalyzer()

    def test_municipal_show_cause_notice_analysis(self):
        raw_text = SAMPLE_NOTICES["MUNICIPAL_SHOW_CAUSE"]["raw_text"]
        result = self.analyzer.analyze_document(raw_text, user_language="mr-IN")

        self.assertIn("Municipal", result["apparent_document_type"])
        self.assertTrue(len(result["explicit_dates_found"]) > 0)
        self.assertIn("15/10/2026", result["explicit_dates_found"])
        
        # Check deadline separation
        deadlines = result["deadlines_analysis"]
        self.assertTrue(len(deadlines["explicitly_printed_deadlines"]) > 0)
        self.assertTrue(len(deadlines["inferred_legal_rule"]) > 0)

        # Check legal glossary decoded
        terms_found = [t["term"] for t in result["legal_terms_explained"]]
        self.assertTrue(any("Show Cause" in t for t in terms_found))
        self.assertTrue(any("Ex-Parte" in t for t in terms_found))

        # Check lawyer questions
        self.assertTrue(len(result["questions_for_lawyer"]) >= 2)

    def test_short_or_empty_text_error(self):
        result = self.analyzer.analyze_document("short", user_language="mr-IN")
        self.assertTrue(result.get("error"))

if __name__ == "__main__":
    unittest.main()
