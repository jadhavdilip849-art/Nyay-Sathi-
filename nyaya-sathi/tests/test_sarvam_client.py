"""
Unit tests for Sarvam AI Client and Fallback Mechanism.
Tests graceful degradation when API key is missing or invalid.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.voice.sarvam_client import SarvamAIClient

class TestSarvamClient(unittest.TestCase):

    def setUp(self):
        # Client without real API key to test fallback
        self.fallback_client = SarvamAIClient(api_key="")

    def test_stt_fallback_to_browser(self):
        result = self.fallback_client.speech_to_text(b"fake_audio_bytes")
        self.assertFalse(result["success"])
        self.assertEqual(result["provider"], "fallback_browser")

    def test_tts_fallback_to_browser_synthesis(self):
        result = self.fallback_client.text_to_speech("कामगारांचे हक्क", target_language_code="mr-IN")
        self.assertFalse(result["success"])
        self.assertEqual(result["provider"], "fallback_browser")
        self.assertEqual(result["language_code"], "mr-IN")

    def test_translation_offline_dictionary_fallback(self):
        result = self.fallback_client.translate_text(
            "my employer has not paid my wages for two months. what can i do?",
            source_lang="en-IN",
            target_lang="mr-IN"
        )
        self.assertTrue(result["success"])
        self.assertIn("माझ्या मालकाने", result["translated_text"])

if __name__ == "__main__":
    unittest.main()
