"""
Safety, Ethics, and Guardrails Module for Nyaya Sathi.
Enforces safety rules, emergency escalations, anti-fabrication constraints,
and privacy filters.
"""

import re
from typing import Dict, List, Any, Optional
from ..config import LEGAL_DISCLAIMER, PRIVACY_WARNING

EMERGENCY_HOTLINES = [
    {
        "name": "राष्ट्रीय आणीबाणी सेवा / National Emergency Response Support System (ERSS)",
        "number": "112",
        "description": "पोलीस, रुग्णवाहिका, अग्निशामक दलासाठी २४ तास उपलब्ध",
        "type": "Police / Life Safety"
    },
    {
        "name": "महिला हेल्पलाईन / Women Helpline (Domestic Violence / Distress)",
        "number": "181",
        "description": "कौटुंबिक हिंसाचार किंवा संकटात सापडलेल्या महिलांसाठी तात्काळ मदत",
        "type": "Women Safety"
    },
    {
        "name": "सायबर आर्थिक फसवणूक हेल्पलाइन / Cyber Fraud Helpline",
        "number": "1930",
        "description": "ऑनलाइन बँक किंवा यूपीआय फसवणूक झाल्यास खाते गोठवण्यासाठी त्वरित कॉल करा",
        "type": "Financial Cybercrime"
    },
    {
        "name": "राष्ट्रीय विधी सेवा प्राधिकरण (NALSA) मोफत कायदेशीर मदत",
        "number": "15100",
        "description": "मोफत सरकारी वकील व कायदेशीर सल्ल्यासाठी टोल-फ्री क्रमांक",
        "type": "Legal Aid"
    },
    {
        "name": "बाल हेल्पलाइन / Childline Helpline",
        "number": "1098",
        "description": "संकटात सापडलेल्या मुलांच्या मदतीसाठी",
        "type": "Child Safety"
    },
    {
        "name": "एल्डर लाईन (ज्येष्ठ नागरिक हेल्पलाइन) / Elder Line",
        "number": "14567",
        "description": "ज्येष्ठ नागरिकांच्या समस्या व संरक्षणासाठी",
        "type": "Senior Citizens"
    }
]

EMERGENCY_TRIGGER_WORDS = [
    "मारहाण चालू आहे", "जीवाला धोका", "आत्महत्या", "खून", "पळवून नेले", "बलात्कार", "अत्याचार", "मारून टाकेन",
    "जान को खतरा", "आत्महत्या", "मर्डर", "अपहरण", "मारपीट हो रही है", "जान से मारने की धमकी",
    "life in danger", "suicide", "murder", "assault in progress", "kidnapped", "domestic violence right now", "rape"
]

SENSITIVE_DATA_PATTERNS = [
    (r'\b\d{4}\s?\d{4}\s?\d{4}\b', "Aadhaar Card Number"),
    (r'\b\d{6}\b', "Potential OTP / PIN"),
    (r'\b\d{16}\b', "Credit/Debit Card Number"),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', "Email Address")
]

class SafetyGuardrailEngine:
    """Enforces ethical boundaries, urgent escalations, and data minimization."""

    def check_query_safety(self, text: str) -> Dict[str, Any]:
        """Scans input for life safety emergencies, sensitive data leaks, and malicious prompts."""
        text_lower = text.lower()
        is_emergency = False
        emergency_matches = []

        for trigger in EMERGENCY_TRIGGER_WORDS:
            if trigger in text_lower:
                is_emergency = True
                emergency_matches.append(trigger)

        # Check for accidental sensitive data entry
        found_sensitive = []
        for pattern, label in SENSITIVE_DATA_PATTERNS:
            if re.search(pattern, text):
                found_sensitive.append(label)

        # Check for unethical instructions (fabricate evidence, hide documents)
        unethical_advice_requested = False
        if any(w in text_lower for w in ["खोटा पुरावा", "दस्तावेज नष्ट", "पुरावा लपवा", "झूठे सबूत", "कागजात छुपाना", "fake evidence", "destroy proof", "hide document"]):
            unethical_advice_requested = True

        return {
            "is_emergency": is_emergency,
            "emergency_triggers": emergency_matches,
            "contains_sensitive_data": len(found_sensitive) > 0,
            "sensitive_types": found_sensitive,
            "unethical_request": unethical_advice_requested,
            "emergency_hotlines": EMERGENCY_HOTLINES if is_emergency else [],
            "escalation_message": (
                "⚠️ तातडीची सुरक्षा सूचना: जर आपला किंवा कोणाचा जीव धोक्यात असेल, तर कृपया चॅट बॉटवर वेळ न घालवता ताबडतोब ११२ (पोलीस) किंवा १८१ (महिला हेल्पलाईन) वर कॉल करा!"
                if is_emergency else None
            ),
            "unethical_warning": (
                "कायदेशीर सूचना: न्याय साथी कधीही खोटे पुरावे तयार करणे, कागदपत्रे लपवणे किंवा खोटी साक्ष देण्यास सहाय्य करत नाही. असे कृत्य भारतीय न्याय संहिता (BNS) अंतर्गत गंभीर दखलपात्र गुन्हा आहे."
                if unethical_advice_requested else None
            ),
            "privacy_reminder": PRIVACY_WARNING if found_sensitive else None,
            "standard_disclaimer": LEGAL_DISCLAIMER
        }
