"""
Unit tests for Legal Aid Service.
Tests Section 12 statutory eligibility criteria (women, industrial workman, SC/ST, low income)
and DLSA directory lookups.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.legal_aid.legal_aid_service import LegalAidService

class TestLegalAidService(unittest.TestCase):

    def setUp(self):
        self.service = LegalAidService()

    def test_woman_automatic_eligibility(self):
        result = self.service.evaluate_eligibility(category="woman", state="Maharashtra")
        self.assertTrue(result["is_eligible"])
        self.assertEqual(result["statutory_clause"], "Section 12(c)")

    def test_industrial_workman_eligibility(self):
        result = self.service.evaluate_eligibility(category="industrial_workman", state="Maharashtra")
        self.assertTrue(result["is_eligible"])
        self.assertEqual(result["statutory_clause"], "Section 12(e)")

    def test_low_income_within_threshold(self):
        result = self.service.evaluate_eligibility(category="low_income", annual_income=180000, state="Maharashtra")
        self.assertTrue(result["is_eligible"])
        self.assertIn("Section 12(h)", result["statutory_clause"])

    def test_high_income_exceeds_threshold(self):
        result = self.service.evaluate_eligibility(category="low_income", annual_income=800000, state="Maharashtra")
        self.assertFalse(result["is_eligible"])

    def test_pune_dlsa_directory_lookup(self):
        contacts = self.service.get_contacts(state="Maharashtra", district="pune")
        self.assertEqual(contacts["emergency_legal_helpline"], "15100")
        self.assertIn("Shivajinagar", contacts["district_authority"]["address"])
        self.assertEqual(contacts["district_authority"]["phone"], "020-25537550")

if __name__ == "__main__":
    unittest.main()
