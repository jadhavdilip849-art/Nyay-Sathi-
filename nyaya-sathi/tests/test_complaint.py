"""
Unit tests for Complaint Drafting Engine.
Verifies multi-format output, truthful fact retention, evidence checklists,
and anti-fabrication constraints.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.complaints.complaint_generator import ComplaintGenerator

class TestComplaintGenerator(unittest.TestCase):

    def setUp(self):
        self.gen = ComplaintGenerator()

    def test_complaint_generation_unpaid_wages(self):
        result = self.gen.generate_complaint(
            complainant_name="रुपेश तुकाराम पाटील",
            complainant_address="भोसरी, पुणे",
            complainant_phone="9822001122",
            opposite_party_name="सनशाईन मॅन्युफॅक्चरिंग प्रा. लि.",
            opposite_party_address="एमआयडीसी भोसरी",
            matter_type="unpaid_wages",
            dates_involved="ऑगस्ट व सप्टेंबर २०२६",
            factual_summary="दोन महिन्यांचे एकूण ४५,००० रुपये वेतन थकीत आहे.",
            prior_action_taken="तोंडी विचारणा केली पण उत्तर मिळाले नाही.",
            requested_relief="थकीत वेतन त्वरित बँक खात्यात जमा करावे.",
            language="mr-IN"
        )

        self.assertIn("रुपेश तुकाराम पाटील", result["formal_letter_mr"])
        self.assertIn("सनशाईन मॅन्युफॅक्चरिंग", result["formal_letter_mr"])
        self.assertIn("४५,०००", result["formal_letter_mr"])
        self.assertIn("रुपेश तुकाराम पाटील", result["formal_letter_en"])
        self.assertTrue(len(result["short_portal_version_mr"]) <= 500)
        self.assertTrue(len(result["supporting_documents_checklist"]) >= 3)
        self.assertIn("समाधान", result["submission_channel"]["channel_mr"])

    def test_no_arbitrary_hallucinated_sections(self):
        # Ensure no randomly injected penal sections appear when user did not supply them
        result = self.gen.generate_complaint(
            complainant_name="A",
            complainant_address="B",
            complainant_phone="123",
            opposite_party_name="C",
            opposite_party_address="D",
            matter_type="general",
            dates_involved="Yesterday",
            factual_summary="Simple dispute without fraud.",
            prior_action_taken="",
            requested_relief="Resolution"
        )
        # Should not falsely accuse under IPC 420 or BNS criminal sections without facts
        self.assertNotIn("420", result["formal_letter_mr"])

if __name__ == "__main__":
    unittest.main()
