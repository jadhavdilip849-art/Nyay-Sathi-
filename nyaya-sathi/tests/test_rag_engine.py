"""
Unit tests for Legal RAG Engine.
Tests Marathi and Hindi query retrieval, domain mapping, official citations,
clarifying questions, and practical next steps.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.legal_kb.rag_engine import LegalRAGEngine

class TestLegalRAGEngine(unittest.TestCase):

    def setUp(self):
        self.engine = LegalRAGEngine()

    def test_marathi_unpaid_wages_query(self):
        query = "माझ्या मालकाने गेल्या दोन महिन्यांपासून माझा पगार दिलेला नाही. मी काय करू शकतो?"
        result = self.engine.retrieve(query)

        self.assertEqual(result["detected_language"], "mr-IN")
        self.assertEqual(result["domain_id"], "unpaid_wages")
        self.assertIn("Payment of Wages Act", result["official_citation"]["title"])
        self.assertIn("कामगार", result["plain_language_summary"])
        self.assertTrue(len(result["clarifying_questions"]) > 0)
        self.assertTrue(len(result["action_steps"]) > 0)
        self.assertIn("samadhan.labour.gov.in", result["official_citation"]["portal_url"])

    def test_hindi_consumer_complaint_query(self):
        query = "दुकानदार ने मुझे खराब सामान दिया और अब वारंटी देने से मना कर रहा है।"
        result = self.engine.retrieve(query)

        self.assertEqual(result["detected_language"], "hi-IN")
        self.assertEqual(result["domain_id"], "consumer_complaints")
        self.assertIn("Consumer Protection Act", result["official_citation"]["title"])
        self.assertIn("1915", result["official_citation"]["helpline"])

    def test_cybercrime_financial_fraud_query(self):
        query = "माझ्या बँक खात्यातून ऑनलाइन फसवणुकीद्वारे ५० हजार रुपये कापले गेले आहेत."
        result = self.engine.retrieve(query)

        self.assertEqual(result["domain_id"], "cybercrime")
        self.assertIn("1930", result["official_citation"]["helpline"])
        self.assertIn("cybercrime.gov.in", result["official_citation"]["portal_url"])

    def test_non_guarantee_and_uncertainties_present(self):
        query = "Can I guarantee a win against my employer?"
        result = self.engine.retrieve(query)

        self.assertIn("important_uncertainty", result)
        self.assertIn("disclaimer", result)

if __name__ == "__main__":
    unittest.main()
